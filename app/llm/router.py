from typing import Optional
from .base_llm import BaseLLM
from .ollama import OllamaLLM


class LLMRouter:
    def __init__(self):
        self._providers: dict[str, BaseLLM] = {}
        self._default: str = "ollama"

    def register(self, name: str, provider: BaseLLM):
        self._providers[name] = provider

    def set_default(self, name: str):
        if name in self._providers:
            self._default = name

    def get_provider(self, name: Optional[str] = None) -> BaseLLM:
        key = name or self._default
        return self._providers.get(key)

    def generate(self, prompt: str, system: Optional[str] = None,
                 provider: Optional[str] = None, **kwargs) -> str:
        llm = self.get_provider(provider)
        if not llm:
            raise ValueError(f"LLM provider '{provider or self._default}' not registered")
        return llm.generate(prompt, system=system, **kwargs)

    def generate_stream(self, prompt: str, system: Optional[str] = None,
                        provider: Optional[str] = None, **kwargs):
        llm = self.get_provider(provider)
        if not llm:
            raise ValueError(f"LLM provider '{provider or self._default}' not registered")
        yield from llm.generate_stream(prompt, system=system, **kwargs)


router = LLMRouter()
router.register("ollama", OllamaLLM())
