import logging

from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import openai

from openai.error import APIConnectionError
from openai.error import APIError
from openai.error import RateLimitError
from openai.error import ServiceUnavailableError
from openai.error import Timeout
from tenacity import before_sleep_log
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_exponential
from tiktoken import encoding_for_model

from apo import MessageTemplate


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


def get_embeddings(texts: List[str], model: str = "text-embedding-ada-002") -> list[list[float]]:
    """Return the embeddings for a list of text strings."""
    embeddings = openai.Embedding.create(input=texts, model=model)["data"]
    return [item.embedding for item in embeddings]


class MessageBuffer:
    """Class to prepare messages for the Chat Completion API."""

    @classmethod
    def __init__(cls, model_name: str = "gpt-3.5-turbo") -> None:
        """Initialise PrepareMessages."""
        cls.model_name = model_name
        cls.encoding = encoding_for_model(model_name)

    @classmethod
    def _count_tokens_from_string(cls, s: str) -> int:
        """Return the number of tokens in a text string."""
        num_tokens = len(cls.encoding.encode(s))
        return num_tokens

    @classmethod
    def _count_tokens_from_messages(cls, messages: List[Dict]) -> int:
        """Return the number of tokens in a list of messages."""
        num_tokens = 0

        # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_message = 3
        tokens_per_name = 1
        for message in messages:
            num_tokens += tokens_per_message
            for k, v in message.items():
                if isinstance(v, str):
                    num_tokens += cls._count_tokens_from_string(v)
                if k == "name":  # When role = function
                    num_tokens += tokens_per_name

        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens

    @classmethod
    def _truncate_messages(cls, messages: List[Dict], max_message_tokens: int) -> List[Dict]:
        """Prune messages that exceed the maximum token limit (token limit is applied to each message individually)"""

        num_tokens = 0
        tokens_per_message = 3

        for message in messages:
            num_tokens += tokens_per_message
            if message.get("content") is None:
                content = str(message.get("function_call", ""))
            else:
                content = message.get("content", "")
            encoded_content = cls.encoding.encode(content)
            num_tokens += len(encoded_content)

            if num_tokens > max_message_tokens:
                excess_tokens = num_tokens - max_message_tokens
                pruned_content_length = len(encoded_content) - excess_tokens
                logger.warning(
                    f"Pruned message to {pruned_content_length / len(encoded_content)} % of original tokens"
                )
                message["content"] = cls.encoding.decode(encoded_content[:pruned_content_length])

            num_tokens = 0

        return messages

    @staticmethod
    def _forget_messages(num_tokens: int, max_tokens: int) -> bool:
        """Return True if the number of tokens exceeds the maximum token limit across all messages."""
        if num_tokens > max_tokens:
            return True
        return False

    @classmethod
    def process(
        cls,
        messages: List[Dict],
        max_tokens: int = 4500,
        max_message_tokens: int = 2000,
        keep_system_message: bool = False,
        prune_messages: bool = True,
    ) -> List[Dict]:
        """
        Return the messages, ensuring they don't exceed the maximum token limit across all messages.

        Parameters:
        ------------
        messages:
            List of messages to buffer

        model_name:
            Model to use for token counting

        max_tokens:
            Maximum number of tokens allowed

        max_message_tokens:
            Maximum number of tokens allowed per message

        keep_system_message:
            Whether to force the system messages in the buffer

        truncate_messages:
            Whether to truncate messages that exceed the maximum token limit
            (token limit is applied to each message individually)

        TODO:
        - Refactor `messages.pop(0)`, do not modify the object.

        """
        num_tokens = 0
        buffer_messages = []

        if prune_messages:
            messages = cls._truncate_messages(messages, max_message_tokens)

        if keep_system_message:
            system_messages = [message for message in messages if message["role"] == "system"]
            messages = [message for message in messages if message["role"] != "system"]
            buffer_messages.extend(system_messages)
            num_tokens = cls._count_tokens_from_messages(system_messages)

        num_tokens += cls._count_tokens_from_messages(messages)

        if cls._forget_messages(num_tokens, max_tokens):
            messages.pop(0)
            buffer_messages.extend(messages)  # assumes system messages are first
            cls.process(
                messages,
                max_tokens=max_tokens,
                max_message_tokens=max_message_tokens,
                keep_system_message=keep_system_message,
                prune_messages=prune_messages,
            )
        else:
            buffer_messages.extend(messages)

        return buffer_messages


class ChatGPT:
    """
    OpenAI Wrapper for the Chat Completion API.

    Handles asynchronous requests to the OpenAI Chat Completion API, including:
    - Retrying failed requests
    - Handling rate limits, timeouts, exceptions
    - Truncating long messages

    Note: Base gpt-3.5-turbo model has a maximum token limit of 4096 tokens split across the prompt and response.
    You should cater the split of tokens to your use case.

    """

    @classmethod
    async def generate(
        cls,
        messages: List[Dict],
        message_kwargs: Optional[Dict] = None,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.0,
        **openai_kwargs,
    ) -> Dict:
        """
        Call OpenAI's chat completion API asynchronousely and await the response.

        Handles asynchronous requests to the OpenAI Chat Completion API, including:
        - Retrying failed requests
        - Handling rate limits, timeouts, exceptions
        - Truncating long messages

        Parameters
        ----------
        messages:
            List of messages to buffer

        message_kwargs:
            If passing in a MessageTemplate that needs formatting,
            the dictionary of keyword arguments to pass to the MessageTemplate

        model:
            Model to use for token counting and completion

        temperature:
            Temperature to use for completion

        openai_kwargs:
            Additional arguments to pass to the OpenAI Chat Completion API

        Usage:
        >>> messages = [
        >>>     {"role": "system", "name": "assistant", "content": "Tell the user a joke about it's topic of choice"},
        >>>     {"role": "user", "name": "user", "content": "Giraffes"},
        >>> ]
        >>> response = await ChatGPT.generate(messages, model="gpt-3.5-turbo", temperature=0.0)
        >>> print(response)
        >>> "Why don't giraffes use computers? Because their heads are always in the clouds!"
        """

        if not message_kwargs:
            message_kwargs = {}

        messages = [cls.prepare_message(message, **message_kwargs) for message in messages]

        response = await cls._call(messages=messages, model=model, temperature=temperature, **openai_kwargs)

        return response["choices"][0]["message"]

    @classmethod
    def prepare_message(cls, obj: Union[MessageTemplate, dict, str], **kwargs) -> Dict:
        """Process a message. TODO: Add FunctionTemplate"""
        if not kwargs and isinstance(obj, dict):  # the MessageTemplate has been pre-processed
            return obj
        elif isinstance(obj, MessageTemplate):
            obj.format_message(**kwargs)
            return obj.to_prompt()
        elif kwargs and not isinstance(obj, MessageTemplate):  # dictionary or serialised prompt, needs formatting
            prompt = MessageTemplate.load(obj)
            prompt.format_message(**kwargs)
            return prompt.to_prompt()
        else:
            logger.error("You must pass through either a MessageTemplate or a pre-formatted Message")

    @staticmethod
    @retry(
        retry(
            reraise=True,
            stop=stop_after_attempt(8),
            wait=wait_exponential(multiplier=1, min=1, max=60),
            retry=(
                retry_if_exception_type(Timeout)
                | retry_if_exception_type(APIError)
                | retry_if_exception_type(APIConnectionError)
                | retry_if_exception_type(RateLimitError)
                | retry_if_exception_type(ServiceUnavailableError)
            ),
            before_sleep=before_sleep_log(logger, logging.WARNING),
        )
    )
    async def _call(
        messages: List[Dict],
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.0,
        request_timeout: int = 30,
        **kwargs,
    ) -> Dict:
        """Private method to create an async OpenAI Call."""
        return await openai.ChatCompletion.acreate(
            model=model,
            messages=messages,
            temperature=temperature,
            request_timeout=request_timeout,
            **kwargs,
        )  # type:ignore
