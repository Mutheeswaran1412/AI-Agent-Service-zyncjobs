import re
import math
from collections import Counter


class TfidfVectorizer:
    def __init__(self):
        self._doc_freq: dict[str, int] = {}
        self._num_docs: int = 0
        self._fitted: bool = False

    def fit(self, documents: list[str]):
        self._num_docs = len(documents)
        self._doc_freq = {}
        for doc in documents:
            terms = set(self._tokenize(doc))
            for term in terms:
                self._doc_freq[term] = self._doc_freq.get(term, 0) + 1
        self._fitted = True

    def transform(self, text: str) -> dict[str, float]:
        if not self._fitted:
            return {}
        terms = self._tokenize(text)
        term_counts = Counter(terms)
        max_count = max(term_counts.values()) if term_counts else 1
        result = {}
        for term, count in term_counts.items():
            tf = count / max_count
            idf = math.log((self._num_docs + 1) / (self._doc_freq.get(term, 1) + 1)) + 1
            result[term] = tf * idf
        return result

    def _tokenize(self, text: str) -> list[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z]{2,}\b', text)
        stop_words = {
            "the", "a", "an", "and", "or", "in", "of", "to", "for", "is",
            "are", "was", "were", "be", "been", "being", "have", "has", "had",
            "do", "does", "did", "will", "would", "could", "should", "may",
            "might", "shall", "can", "need", "dare", "ought", "used",
            "this", "that", "these", "those", "i", "me", "my", "we", "our",
            "you", "your", "he", "him", "his", "she", "her", "it", "its",
            "they", "them", "their", "what", "which", "who", "whom",
            "when", "where", "why", "how", "all", "each", "every", "both",
            "few", "more", "most", "other", "some", "such", "no", "nor",
            "not", "only", "own", "same", "so", "than", "too", "very",
        }
        return [t for t in tokens if t not in stop_words]

    def cosine_similarity(self, vec1: dict[str, float], vec2: dict[str, float]) -> float:
        all_terms = set(vec1) | set(vec2)
        dot = sum(vec1.get(t, 0) * vec2.get(t, 0) for t in all_terms)
        norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)
