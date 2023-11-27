import logging

from asyncio import Semaphore
from typing import Dict
from typing import List
from typing import Optional

from dotenv import load_dotenv
from openai import APIConnectionError
from openai import APIError
from openai import AsyncOpenAI
from openai import InternalServerError
from openai import OpenAI
from openai import RateLimitError
from openai import Timeout
from tenacity import before_sleep_log
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_exponential


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

load_dotenv()


class ChatGPT:
    """OpenAI ChatGPT thin wrapper to handle retries and asynchronous calls"""

    def __init__(self, asynchronous: bool = True, concurrency: int = 10, **kwargs) -> None:
        self.asynchronous = asynchronous
        self.client = AsyncOpenAI(**kwargs) if self.asynchronous else OpenAI(**kwargs)
        self.semaphore = Semaphore(concurrency) if self.asynchronous else None

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
                | retry_if_exception_type(InternalServerError)
            ),
            before_sleep=before_sleep_log(logger, logging.WARNING),
        )
    )
    async def _agenerate(
        self,
        messages: List[Dict],
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.0,
        seed: Optional[int] = 42,
        **openai_kwargs,
    ) -> Dict:
        """Generate text using the OpenAI API"""
        response = await self.client.chat.completions.create(
            messages=messages, model=model, temperature=temperature, seed=seed, **openai_kwargs
        )
        return response.choices[0].message

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
                | retry_if_exception_type(InternalServerError)
            ),
            before_sleep=before_sleep_log(logger, logging.WARNING),
        )
    )
    def _generate(
        self,
        messages: List[Dict],
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.0,
        seed: Optional[int] = 42,
        **openai_kwargs,
    ) -> Dict:
        """Generate text using the OpenAI API"""
        response = self.client.chat.completions.create(
            messages=messages, model=model, temperature=temperature, seed=seed, **openai_kwargs
        )
        return response.choices[0].message
