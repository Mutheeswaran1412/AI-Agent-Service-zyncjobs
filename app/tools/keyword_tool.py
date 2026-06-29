import re
from .base_tool import BaseTool


_STOP_WORDS = {
    "the", "a", "an", "and", "or", "in", "of", "to", "for",
    "with", "on", "at", "by", "is", "are", "be", "will", "we",
    "our", "your", "this", "that", "has", "have", "been",
}


class KeywordTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="keyword_tool",
            description="Extracts important keywords from any text, filtering stop words",
        )

    def run(self, text: str, max_keywords: int = 30) -> list[str]:
        text_lower = text.lower()
        words = re.findall(r'\b[a-z]{3,}\b', text_lower)
        filtered = [w for w in words if w not in _STOP_WORDS]

        freq = {}
        for w in filtered:
            freq[w] = freq.get(w, 0) + 1

        sorted_words = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
        return [w for w, _ in sorted_words[:max_keywords]]

    def extract_phrases(self, text: str, min_len: int = 2, max_len: int = 4) -> list[str]:
        words = text.lower().split()
        phrases = []
        for n in range(min_len, max_len + 1):
            for i in range(len(words) - n + 1):
                phrase = " ".join(words[i:i + n])
                if not any(w in _STOP_WORDS for w in phrase.split()):
                    phrases.append(phrase)
        return phrases[:20]
