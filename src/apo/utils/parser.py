from typing import Dict


def parse_responses(response: str) -> Dict:
    """Parse responses from the OpenAI API where the prompt uses the <START> and <END> tokens."""
    parsed_dict = {}
    start_tag = "<START>"
    end_tag = "<END>"
    while response.find(start_tag) != -1 and response.find(end_tag) != -1:
        start_index = response.find(start_tag) + len(start_tag)
        end_index = response.find(end_tag)
        key = response[start_index:end_index].strip()
        value = response[end_index + len(end_tag) :].strip()
        parsed_dict[key] = value
        response = response[end_index + len(end_tag) :]
    return parsed_dict
