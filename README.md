# Automatic Prompt Optimization (APO)

## Overview
[Automatic Prompt Optimization with “Gradient Descent” and Beam Search](https://arxiv.org/pdf/2305.03495.pdf) is an optimisation technique that uses Gradient Descent and Beam Search to optimize the selection and design of prompts for Language Models (LLMs). The algorithm starts with an initial prompt and iteratively explores new prompt candidates by "expanding" the current prompt to generate variations. The most promising prompts are then "selected" based on specified metric functions. The entire process aims for incremental improvements, ultimately leading to an optimized prompt.

1. **Initialization: Start with an initial prompt p0.**
2. **Gradient Descent with Prompts:**
- Evaluate: Use the current prompt with a batch of data to create a local loss signal.
- Generate Gradient: A static LLM prompt called `∇` generates a natural language summary, serving as the gradient `g`, indicating the flaws in the current prompt.
- Edit Prompt: Another static LLM prompt called `δ` takes `g` and the current prompt to perform an edit in the opposite semantic direction of `g`.
3. **Beam Search Over Prompts:**
- Expand: For each prompt in the current beam, generate new candidate prompts.
- Select: Use a metric function `m` to select the best `b` prompts for the next iteration, where `b` is the beam width.
- Iterate: Repeat these steps for `r` search depth iterations.
Return Optimized Prompt: The algorithm ultimately returns an optimized prompt `p^` that maximizes the given metric function `m`.

## Usage

Note: Only step 2 of the algorithm is implemented at the moment. Step 3 is still in development.

For an example input prompt and an example / series of examples the prompt can be optimised to improve performance:

*Original Prompt*
```
    ## Task
    Is this tweet sarcastic?

    # Output format
    Answer Yes or No as labels

    # Prediction
    Text: {text}
    Label:
```

Run the gradient generation and prompt editing steps:

```
    unclear_sarcasm_example = "I love waking up at 4am on a Monday morning to prepare slides."
    prediction = await evaluate_sarcasm_prompt(unclear_sarcasm_example)

    prompt = MessageTemplate.load("src/apo/prompts/example_base_prompts/sarcasm/user.json")

    error_string = f"{unclear_sarcasm_example}. \n Expected: Yes. \n Actual: No"
    gradients = await generate_gradients(prompt=prompt.to_prompt(), error_str=error_string, num_feedbacks=3)

    prompt = MessageTemplate.load("src/apo/prompts/example_base_prompts/sarcasm/user.json")

    edited_prompt = await edit_prompt_with_gradients(
        prompt=prompt.to_prompt(),
        error_str=error_string,
        gradients=gradients,
        steps_per_gradient=3,
    )

    edited_prompts = json.loads(edited_prompt)["prompts"]

    print(edited_prompts)

```

New Prompts generated:

```
[
    {'role': 'user',
    'content': "\n# Task\nIs this tweet sarcastic?\n\n# Output format\nAnswer Yes or No as labels\n\n# Prediction\nText: {text}\nLabel:\n\n# Examples\n- Text: I can't wait to spend my entire weekend doing laundry.\n  Label: Yes\n\n# Additional Instructions\nLook for phrases that express exaggerated enthusiasm or excitement, but are followed by a negative or undesirable action."},

    {'role': 'user', 'content': '\n# Task\nIs this tweet sarcastic?\n\n# Output format\nAnswer Yes or No as labels\n\n# Prediction\nText: {text}\nLabel:\n\n# Examples\n- Text: Wow, I just love getting stuck in traffic for hours!\n  Label: Yes\n\n# Additional Instructions\nPay attention to tweets that express positive emotions towards unpleasant or frustrating situations.'},

    {'role': 'user', 'content': '\n# Task\nIs this tweet sarcastic?\n\n# Output format\nAnswer Yes or No as labels\n\n# Prediction\nText: {text}\nLabel:\n\n# Examples\n- Text: Oh great, another meeting to discuss the color of the office walls.\n  Label: Yes\n\n# Additional Instructions\nIdentify tweets that convey a sense of annoyance or frustration towards mundane or trivial matters.'}
]
```


## Installation

This package uses Poetry for dependency management. To start developing here, you need to install Poetry

* Follow the instructions on the [official docs](https://python-poetry.org/docs/master/#installing-with-the-official-installer)

Once you have Poetry installed on your system simply run:

```bash
make init
```

## Developing

Check the [CONTRIBUTING.md](/CONTRIBUTING.md) for information about how to develop on this project.
