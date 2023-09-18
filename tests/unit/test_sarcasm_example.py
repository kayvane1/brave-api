import json

import pandas as pd
import pytest

from apo import MessageTemplate
from apo.examples.sarcasm import predict_sarcarsm_with_llm
from apo.gradient_descent import edit_prompt_with_gradients
from apo.gradient_descent import evaluate_prompt
from apo.gradient_descent import generate_gradients


@pytest.fixture
def unclear_sarcasm_example():
    return "I love waking up at 4am on a Monday morning to prepare slides."


@pytest.fixture
def sarcasm_example():
    return "I love waking up at 4am on a Monday morning to prepare slides for a meeting no one will listen in. \
         It's literally my favorite thing to do...eye roll."


@pytest.fixture
def not_sarcasm_example():
    return "Thank you for the birthday present. I love it!"


@pytest.fixture
def sarcasm_batch():
    """
    Batch of examples with labels indicating whether they are sarcastic or not.

    source: https://huggingface.co/datasets/raquiba/Sarcasm_News_Headline/viewer/default/train?row=8
    """
    data = [
        {
            "is_sarcastic": 1,
            "headline": "thirtysomething scientists unveil doomsday clock of hair loss",
            "article_link": "https://www.theonion.com/thirtysomething-scientists-unveil-doomsday-clock-of-hai-1819586205",
        },
        {
            "is_sarcastic": 0,
            "headline": "dem rep. totally nails why congress is falling short on gender, racial equality",
            "article_link": "https://www.huffingtonpost.com/entry/donna-edwards-inequality_us_57455f7fe4b055bb1170b207",
        },
        {
            "is_sarcastic": 0,
            "headline": "eat your veggies: 9 deliciously different recipes",
            "article_link": "https://www.huffingtonpost.com/entry/eat-your-veggies-9-delici_b_8899742.html",
        },
        {
            "is_sarcastic": 1,
            "headline": "inclement weather prevents liar from getting to work",
            "article_link": "https://local.theonion.com/inclement-weather-prevents-liar-from-getting-to-work-1819576031",
        },
        {
            "is_sarcastic": 1,
            "headline": "mother comes pretty close to using word 'streaming' correctly",
            "article_link": "https://www.theonion.com/mother-comes-pretty-close-to-using-word-streaming-cor-1819575546",
        },
        {
            "is_sarcastic": 0,
            "headline": "my white inheritance",
            "article_link": "https://www.huffingtonpost.com/entry/my-white-inheritance_us_59230747e4b07617ae4cbe1a",
        },
        {
            "is_sarcastic": 0,
            "headline": "5 ways to file your taxes with less stress",
            "article_link": "https://www.huffingtonpost.com/entry/5-ways-to-file-your-taxes_b_6957316.html",
        },
        {
            "is_sarcastic": 1,
            "headline": "richard branson's global-warming donation nearly as much as cost of failed balloon trips",
            "article_link": "https://www.theonion.com/richard-bransons-global-warming-donation-nearly-as-much-1819568749",
        },
        {
            "is_sarcastic": 1,
            "headline": "shadow government getting too large to meet in marriott conference room b",
            "article_link": "https://politics.theonion.com/shadow-government-getting-too-large-to-meet-in-marriott-1819570731",
        },
        {
            "is_sarcastic": 0,
            "headline": "lots of parents know this scenario",
            "article_link": "https://www.huffingtonpost.comhttp://pubx.co/6IXxhm",
        },
    ]
    return pd.DataFrame(data)


@pytest.fixture(scope="module")
def shared_data():
    return {}


@pytest.mark.asyncio
async def test_sarcasm_example_true(sarcasm_example):
    """
    Test the sarcasm example
    """
    prediction = await predict_sarcarsm_with_llm(sarcasm_example)
    assert prediction == "Yes"


@pytest.mark.asyncio
async def test_sarcasm_example_false(not_sarcasm_example):
    """
    Test the sarcasm example
    """
    prediction = await predict_sarcarsm_with_llm(not_sarcasm_example)
    assert prediction == "No"


@pytest.mark.asyncio
async def test_generate_gradients(unclear_sarcasm_example, shared_data):
    """
    Test the generate gradients prompt
    """
    prediction = await predict_sarcarsm_with_llm(unclear_sarcasm_example)
    prompt = MessageTemplate.load("src/apo/prompts/example_base_prompts/sarcasm/user.json")
    assert prediction == "No"
    error_string = f"{unclear_sarcasm_example}. \n Expected: Yes. \n Actual: No"
    gradients = await generate_gradients(prompt=prompt.to_prompt(), error_str=error_string, num_feedbacks=3)
    assert len(gradients.split("\n"))

    # Cache the gradients for later use in shared_data fixture
    shared_data["cached_gradients"] = gradients
    shared_data["cached_error_string"] = error_string


@pytest.mark.asyncio
async def test_edit_prompt_with_gradients(unclear_sarcasm_example, shared_data):
    """
    Test the edit prompt with gradients prompt
    """
    # Use the cached gradients from the previous test
    gradients = shared_data["cached_gradients"]
    error_string = shared_data["cached_error_string"]

    prompt = MessageTemplate.load("src/apo/prompts/example_base_prompts/sarcasm/user.json")

    edited_prompt = await edit_prompt_with_gradients(
        prompt=prompt.to_prompt(),
        error_str=error_string,
        gradients=gradients,
        steps_per_gradient=3,
    )

    edited_prompts = json.loads(edited_prompt)["prompts"]

    assert len(edited_prompts) == 3


@pytest.mark.asyncio
async def test_evaluate_prompt(sarcasm_batch):

    # rename column headline to text and is_sarcastic to label
    sarcasm_batch = sarcasm_batch.rename(columns={"headline": "text", "is_sarcastic": "label"})
    # map label to string, 1 = Yes, 0 = No
    label_mapper = {"Yes": 1, "No": 0}

    # Load the prompt
    prompt = MessageTemplate.load("src/apo/prompts/example_base_prompts/sarcasm/user.json")

    # Evaluate the prompt
    predictions = await evaluate_prompt(
        prompt=prompt,
        data=sarcasm_batch,
        input_cols=["text"],
        label_col="label",
        concurrency=10,
        metric="accuracy",
        label_mapping=label_mapper,
    )
    assert isinstance(predictions["accuracy"], float)
