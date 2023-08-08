"""
NEON-based knowledge engineering workflow emulated using CharGPT APIs and
Large Language Models (LLMs) such as GPT-2, GPT-3, and GPT-J.
"""
from pathlib import Path
from utils import load_prompts
import credentials
import openai

openai.api_key = credentials.OPENAI_API_KEY


class NEONPrompting:
    """
    NEON-based knowledge engineering workflow emulated using CharGPT APIs and
    Large Language Models (LLMs) such as GPT-2, GPT-3, and GPT-J.
    """

    def __init__(self, prompts_file: str | Path, **parameters):
        """
        Constructor for NEONPrompting.
        :param parameters: parameters for the ChatGPT APIs.
        :type parameters: dict
        """
        self.parameters = parameters

        if isinstance(prompts_file, str):
            prompts_file = Path(prompts_file)
        self.prompts_file_path = prompts_file

        self.prompts = load_prompts(prompts_file)

    def prompt_chatgpt(self, prompt_index: int) -> str:
        """
        Get the prompt text for a given prompt name.
        :return: The prompt text.
        :rtype: str
        """
        engine = self.parameters.get("engine", "gpt-3.5-turbo-0613")
        temperature = self.parameters.get("temperature", 0.9)
        max_tokens = self.parameters.get("max_tokens", 1000)
        top_p = self.parameters.get("top_p", 1)
        frequency_penalty = self.parameters.get("frequency_penalty", 0.0)
        presence_penalty = self.parameters.get("presence_penalty", 0.0)
        stop = self.parameters.get("stop", ["\n"])

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
        {"content": "My name is NeOn. What's your name?", "role": "assistant"},
        {"content": "My name is John. What is your name?", "role": "user"},
    ]
    response = prompt_chatgpt(prompt_list, engine="gpt-3.5-turbo-0613")
    print(response)
