# Automatic Prompt Optimization (APO)

## Overview
(Automatic Prompt Optimization with “Gradient Descent”
and Beam Search)[https://arxiv.org/pdf/2305.03495.pdf] is an optimisation technique that uses Gradient Descent and Beam Search to optimize the selection and design of prompts for Language Models (LLMs). The algorithm starts with an initial prompt and iteratively explores new prompt candidates by "expanding" the current prompt to generate variations. The most promising prompts are then "selected" based on specified metric functions. The entire process aims for incremental improvements, ultimately leading to an optimized prompt.

1. Initialization: Start with an initial prompt p0.
2. Gradient Descent with Prompts:
- Evaluate: Use the current prompt with a batch of data to create a local loss signal.
- Generate Gradient: A static LLM prompt called ∇ generates a natural language summary, serving as the gradient g, indicating the flaws in the current prompt.
- Edit Prompt: Another static LLM prompt called δ takes g and the current prompt to perform an edit in the opposite semantic direction of g.
3. Beam Search Over Prompts:
- Expand: For each prompt in the current beam, generate new candidate prompts.
- Select: Use a metric function m to select the best b prompts for the next iteration, where b is the beam width.
- Iterate: Repeat these steps for r search depth iterations.
Return Optimized Prompt: The algorithm ultimately returns an optimized prompt p^ that maximizes the given metric function m.



## Developing

Check the [CONTRIBUTING.md](/CONTRIBUTING.md) for information about how to develop on this project.
