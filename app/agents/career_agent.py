from typing import Optional
from .base_agent import BaseAgent
from app.prompts.career_prompt import CAREER_SYSTEM_PROMPT
from app.memory.conversation import ConversationMemory


class CareerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="career_agent",
            description="Provides career advice, skill recommendations, and learning paths",
        )
        self.memory = ConversationMemory()

    def system_prompt(self) -> str:
        return CAREER_SYSTEM_PROMPT

    async def execute(self, query: str, user_id: Optional[str] = None, **kwargs) -> dict:
        history = self.memory.get_history(user_id) if user_id else []

        prompt = f"""
User Query: {query}

Previous Context: {history[-5:] if history else 'No previous context'}
"""
        response = self.generate(prompt, system=CAREER_SYSTEM_PROMPT)

        if user_id:
            self.memory.add(user_id, {"role": "user", "content": query})
            self.memory.add(user_id, {"role": "assistant", "content": response})

        return {"advice": response}
