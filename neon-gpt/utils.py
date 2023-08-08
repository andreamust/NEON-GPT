"""
Utilities for the neon-gpt package.
"""

import json

from pathlib import Path


def load_prompts(prompts_file: str | Path) -> list:
    """
    Load the prompts from the prompts file.
    :param prompts_file: The path to the prompts file.
    :return: A list of prompts.
    """
    if isinstance(prompts_file, str):
        prompts_file = Path(prompts_file)

    with prompts_file.open("r") as f:
        prompts = json.load(f)

    return prompts
