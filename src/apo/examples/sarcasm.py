import asyncio
import json
import logging

from dotenv import load_dotenv

from apo import MessageTemplate
from apo.gradient_descent import APO
from apo.gradient_descent import ChatGPT


load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def predict_sarcarsm_with_llm(text: str, **openai_kwargs) -> str:
    """Asynchronously evaluate a sarcasm prompt and return the output"""
    llm = ChatGPT()
    evaluate_prompt = MessageTemplate.load("src/apo/prompts/example_base_prompts/sarcasm/user.json")
    evaluate_prompt.format_message(text=text)
    messages = [evaluate_prompt.to_prompt()]
    response = await llm._agenerate(messages=messages, **openai_kwargs)
    return response.content


async def run_sarcasm_single_example() -> None:
    """Run the sarcasm example"""

    unclear_sarcasm_example = "I love waking up at 4am on a Monday morning to prepare slides."
    prompt = MessageTemplate.load("src/apo/prompts/example_base_prompts/sarcasm/user.json")

    error_string = f"{unclear_sarcasm_example}. \n Expected: Yes. \n Actual: No"
    apo = APO(asynchronous=True)
    gradients = await apo.generate_gradients(prompt=prompt.to_prompt(), error_str=error_string, num_feedbacks=3)

    prompt = MessageTemplate.load("src/apo/prompts/example_base_prompts/sarcasm/user.json")

    edited_prompt = await apo.edit_prompt_with_gradients(
        prompt=prompt.to_prompt(),
        error_str=error_string,
        gradients=gradients,
        steps_per_gradient=3,
    )

    edited_prompts = json.loads(edited_prompt)["prompts"]

    logger.info(edited_prompts)


if __name__ == "__main__":
    asyncio.run(run_sarcasm_single_example())
