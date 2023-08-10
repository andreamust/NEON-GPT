"""
Main entry point for the neon-gpt package.
"""
import json
from pathlib import Path

from neon_prompting import NEONPrompting

PROMPTS_PATH = Path("./prompts/neon_prompts.json")


def all_prompts():
    """
    Generate all prompts.
    """
    neon = NEONPrompting(PROMPTS_PATH)

    for prompt_index in range(len(neon.prompts)):
        abc = neon.prompt_chatgpt(prompt_index)

    # save the neon conversation
    with open("./output/neon_conversation.json", "w") as f:
        json.dump(neon.conversation, f, indent=4)

    return neon.conversation


if __name__ == '__main__':
    conversation = all_prompts()
    print(conversation)

