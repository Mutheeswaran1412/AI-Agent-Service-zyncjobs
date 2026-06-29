from typing import Optional
from app.agents.chat_agent import ChatAgent
from app.utils.logger import logger

chat_agent = ChatAgent()


async def handle(query: str, user_id: Optional[str] = None, **kwargs) -> dict:
    logger.info("ChatService.handle", query=query[:80])
    result = await chat_agent.execute(query=query, user_id=user_id)
    return {"reply": result.get("reply", "")}
