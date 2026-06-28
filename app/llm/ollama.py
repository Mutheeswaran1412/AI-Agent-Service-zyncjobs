from typing import Optional
import ollama

from app.config.settings import settings
from .base_llm import BaseLLM


class OllamaLLM(BaseLLM):
    def __init__(self, model: Optional[str] = None):
        self.model = model or settings.OLLAMA_MODEL
        self.client = ollama

    def generate(self, prompt: str, system: Optional[str] = None, **kwargs) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat(model=self.model, messages=messages, **kwargs)
        return response["message"]["content"]

    def generate_stream(self, prompt: str, system: Optional[str] = None, **kwargs):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        stream = self.client.chat(
            model=self.model, messages=messages, stream=True, **kwargs
        )
        for chunk in stream:
            yield chunk["message"]["content"]
