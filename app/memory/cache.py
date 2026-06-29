import time
import hashlib
from typing import Optional


class PromptCache:
    def __init__(self, ttl_seconds: int = 300, max_size: int = 100):
        self._ttl = ttl_seconds
        self._max = max_size
        self._cache: dict[str, tuple[float, str]] = {}

    def _key(self, prompt: str, model: str = "") -> str:
        raw = f"{model}:{prompt}"
        return hashlib.md5(raw.encode()).hexdigest()

    def get(self, prompt: str, model: str = "") -> Optional[str]:
        key = self._key(prompt, model)
        entry = self._cache.get(key)
        if entry is None:
            return None
        ts, value = entry
        if time.time() - ts > self._ttl:
            del self._cache[key]
            return None
        return value

    def set(self, prompt: str, response: str, model: str = ""):
        if len(self._cache) >= self._max:
            oldest = min(self._cache.keys(), key=lambda k: self._cache[k][0])
            del self._cache[oldest]
        key = self._key(prompt, model)
        self._cache[key] = (time.time(), response)

    def clear(self):
        self._cache.clear()

    @property
    def size(self) -> int:
        return len(self._cache)


prompt_cache = PromptCache()
