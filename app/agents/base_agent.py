from abc import ABC, abstractmethod
from typing import Optional
from app.llm.router import router as llm_router
from app.utils.logger import logger


class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.llm = llm_router

    @abstractmethod
    def system_prompt(self) -> str:
        pass

    async def run(self, query: str, user_id: Optional[str] = None, **kwargs) -> dict:
        logger.info(f"Agent {self.name} processing query")
        result = await self.execute(query, user_id=user_id, **kwargs)
        return result

    @abstractmethod
    async def execute(self, query: str, user_id: Optional[str] = None, **kwargs) -> dict:
        pass

    def generate(self, prompt: str, system: Optional[str] = None, **kwargs) -> str:
        return self.llm.generate(prompt, system=system or self.system_prompt(), **kwargs)
