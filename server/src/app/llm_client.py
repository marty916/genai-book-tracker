import os
from openai import OpenAI

class LLMClient:
    """
    Abstraction for OpenAI LLM client with model selection.
    """
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def chat(self, messages, max_tokens=256, temperature=0.7):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
