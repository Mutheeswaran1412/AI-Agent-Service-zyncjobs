from datetime import datetime, timezone


class UserMemory:
    def __init__(self):
        self._store: dict[str, dict] = {}

    def save_profile(self, user_id: str, data: dict):
        if user_id not in self._store:
            self._store[user_id] = {}
        self._store[user_id]["profile"] = {
            **self._store[user_id].get("profile", {}),
            **data,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_profile(self, user_id: str) -> dict:
        return self._store.get(user_id, {}).get("profile", {})

    def save_resume(self, user_id: str, resume_data: dict):
        if user_id not in self._store:
            self._store[user_id] = {}
        self._store[user_id]["resume"] = {
            **resume_data,
            "saved_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_resume(self, user_id: str) -> dict:
        return self._store.get(user_id, {}).get("resume", {})

    def save_skills(self, user_id: str, skills: list[str]):
        if user_id not in self._store:
            self._store[user_id] = {}
        existing = self._store[user_id].get("skills", [])
        merged = list(dict.fromkeys(existing + skills))
        self._store[user_id]["skills"] = merged

    def get_skills(self, user_id: str) -> list[str]:
        return self._store.get(user_id, {}).get("skills", [])

    def save_goal(self, user_id: str, goal: str):
        if user_id not in self._store:
            self._store[user_id] = {}
        self._store[user_id]["career_goal"] = {
            "goal": goal,
            "set_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_goal(self, user_id: str) -> str:
        return self._store.get(user_id, {}).get("career_goal", {}).get("goal", "")

    def remember(self, user_id: str, key: str, value):
        if user_id not in self._store:
            self._store[user_id] = {}
        self._store[user_id][key] = value

    def recall(self, user_id: str, key: str):
        return self._store.get(user_id, {}).get(key)

    def clear(self, user_id: str):
        self._store.pop(user_id, None)
