import os

import openai

from dotenv import load_dotenv

from apo import ChatGPT as llm
from apo import MessageTemplate


load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


async def evaluate_sarcasm_prompt(text: str, **openai_kwargs) -> str:
    """Asynchronously evaluate a sarcasm prompt and return the output"""
    evaluate_prompt = MessageTemplate.load("src/apo/prompts/example_base_prompts/sarcasm/user.json")
    evaluate_prompt.format_message(text=text)
    messages = [evaluate_prompt.to_prompt()]
    response = await llm.generate(messages=messages, **openai_kwargs)
    return response["content"]
