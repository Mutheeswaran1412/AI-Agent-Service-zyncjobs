class VectorMemory:
    def __init__(self):
        # placeholder — will integrate pgvector or ChromaDB later
        self._store = {}

    def store(self, namespace: str, key: str, vector: list[float], metadata: dict):
        if namespace not in self._store:
            self._store[namespace] = {}
        self._store[namespace][key] = {"vector": vector, "metadata": metadata}

    def search(self, namespace: str, query_vector: list[float], top_k: int = 5) -> list[dict]:
        # placeholder
        return []
