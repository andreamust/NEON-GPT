"""
NEON-based knowledge engineering workflow emulated using CharGPT APIs and
Large Language Models (LLMs) such as GPT-2, GPT-3, and GPT-J.
"""

import credentials
import openai

openai.api_key = credentials.OPENAI_API_KEY


def get_prompt(prompt: list, **parameters) -> str:
    """
    Get the prompt text for a given prompt name.
    :param prompt: The name of the prompt to retrieve.
    :type prompt: list
    :return: The prompt text.
    :rtype: str
    """
    if prompt is None:
        raise ValueError("No prompt provided")

    engine = parameters.get("engine", "gpt-3.5-turbo-0613")
    temperature = parameters.get("temperature", 0.9)
    max_tokens = parameters.get("max_tokens", 1000)
    top_p = parameters.get("top_p", 1)
    frequency_penalty = parameters.get("frequency_penalty", 0.0)
    presence_penalty = parameters.get("presence_penalty", 0.0)
    stop = parameters.get("stop", ["\n"])

    response = openai.ChatCompletion.create(
        model=engine,
        messages=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
    )
    return response.choices[0].message


if __name__ == "__main__":
    prompt_list = [
        {"role": "user", "content": "how're you doing?"},
        {
            "content": "As an AI, I don't have feelings, but I'm here to help "
            "you with any questions or tasks you have. How can I "
            "assist you today?",
            "role": "assistant",
        },
        {
            "content": "I'm doing well, thanks for asking. What's your name?",
            "role": "user",
        },
        {"content": "My name is Neon. What's your name?", "role": "assistant"},
        {"content": "My name is John. What is your name?", "role": "user"},
    ]
    response = get_prompt(prompt_list, engine="gpt-3.5-turbo-0613")
    print(response)
