from .base import Document
from .embedder import TfidfVectorizer


class VectorStore:
    def __init__(self):
        self._documents: list[Document] = []
        self._vectors: list[dict[str, float]] = []
        self._vectorizer = TfidfVectorizer()
        self._indexed: bool = False

    def add(self, doc: Document):
        self._documents.append(doc)
        self._indexed = False

    def add_many(self, docs: list[Document]):
        self._documents.extend(docs)
        self._indexed = False

    def remove(self, doc_id: str):
        self._documents = [d for d in self._documents if d.id != doc_id]
        self._indexed = False

    def clear(self):
        self._documents = []
        self._vectors = []
        self._indexed = False

    def search(self, query: str, top_k: int = 5) -> list[Document]:
        if not self._documents:
            return []

        self._ensure_indexed()
        query_vec = self._vectorizer.transform(query)

        scored = []
        for i, doc in enumerate(self._documents):
            if i < len(self._vectors):
                score = self._vectorizer.cosine_similarity(query_vec, self._vectors[i])
                doc.score = score
                scored.append(doc)

        scored.sort(key=lambda d: d.score, reverse=True)
        return scored[:top_k]

    def _ensure_indexed(self):
        if self._indexed:
            return
        texts = [d.text for d in self._documents]
        self._vectorizer.fit(texts)
        self._vectors = [self._vectorizer.transform(t) for t in texts]
        self._indexed = True

    @property
    def count(self) -> int:
        return len(self._documents)
