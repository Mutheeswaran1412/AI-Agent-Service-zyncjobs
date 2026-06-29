from .conversation import ConversationMemory
from .user_memory import UserMemory


class MemoryManager:
    def __init__(self):
        self.conversation = ConversationMemory()
        self.user = UserMemory()

    def store_message(self, user_id: str, role: str, content: str):
        self.conversation.add(user_id, {"role": role, "content": content})

    def get_history(self, user_id: str, limit: int = 20) -> list[dict]:
        return self.conversation.get_history(user_id, limit)

    def store_profile(self, user_id: str, data: dict):
        self.user.save_profile(user_id, data)

    def get_profile(self, user_id: str) -> dict:
        return self.user.get_profile(user_id)

    def store_resume(self, user_id: str, resume_data: dict):
        self.user.save_resume(user_id, resume_data)

    def get_resume(self, user_id: str) -> dict:
        return self.user.get_resume(user_id)

    def store_skills(self, user_id: str, skills: list[str]):
        self.user.save_skills(user_id, skills)

    def get_skills(self, user_id: str) -> list[str]:
        return self.user.get_skills(user_id)

    def store_goal(self, user_id: str, goal: str):
        self.user.save_goal(user_id, goal)

    def get_goal(self, user_id: str) -> str:
        return self.user.get_goal(user_id)

    def remember(self, user_id: str, key: str, value):
        self.user.remember(user_id, key, value)

    def recall(self, user_id: str, key: str):
        return self.user.recall(user_id, key)

    def clear(self, user_id: str):
        self.conversation.clear(user_id)
        self.user.clear(user_id)


memory = MemoryManager()
