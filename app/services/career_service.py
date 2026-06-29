from typing import Optional
from app.agents.career_agent import CareerAgent
from app.utils.logger import logger

career_agent = CareerAgent()


async def handle(query: str, user_id: Optional[str] = None, **kwargs) -> dict:
    logger.info("CareerService.handle")
    result = await career_agent.execute(
        query=query, user_id=user_id,
        current_role=kwargs.get("current_role", ""),
        target_role=kwargs.get("target_role", ""),
        skills=kwargs.get("skills", []),
    )
    return {"advice": result.get("advice", "")}


async def get_career_advice(current_role: str, target_role: str, skills: list[str] = None):
    return await handle(
        query=f"I am a {current_role} transitioning to {target_role}",
        current_role=current_role,
        target_role=target_role,
        skills=skills or [],
    )
