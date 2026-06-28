from datetime import datetime


class ConversationMemory:
    def __init__(self):
        self._store: dict[str, list[dict]] = {}

    def add(self, user_id: str, entry: dict):
        if user_id not in self._store:
            self._store[user_id] = []
        entry["timestamp"] = datetime.utcnow().isoformat()
        self._store[user_id].append(entry)

    def get_history(self, user_id: str, limit: int = 20) -> list[dict]:
        return self._store.get(user_id, [])[-limit:]

    def clear(self, user_id: str):
        self._store.pop(user_id, None)
