from typing import Optional
from .base_agent import BaseAgent
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.memory.memory_manager import memory


class ChatAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="chat_agent",
            description="Handles general conversation, ZyncJobs help, and career queries",
        )

    def system_prompt(self) -> str:
        return SYSTEM_PROMPT

    async def execute(self, query: str, user_id: Optional[str] = None, **kwargs) -> dict:
        history = memory.get_history(user_id) if user_id else []
        context = ""
        if history:
            context = "Previous conversation:\n" + "\n".join(
                f"{m['role']}: {m['content'][:200]}" for m in history[-5:]
            )

        prompt = f"""{context}

User: {query}

Assistant:"""
        prompt = self.augment_with_context(prompt, query)
        response = await self.generate(prompt, system=self.system_prompt())

        if user_id:
            memory.store_message(user_id, "user", query)
            memory.store_message(user_id, "assistant", response)

        return {"reply": response}
