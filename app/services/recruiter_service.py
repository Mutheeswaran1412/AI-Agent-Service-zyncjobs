from typing import Optional
from app.agents.recruiter_agent import RecruiterAgent
from app.utils.logger import logger

recruiter_agent = RecruiterAgent()


async def handle(query: str, user_id: Optional[str] = None, **kwargs) -> dict:
    logger.info("RecruiterService.handle")
    result = await recruiter_agent.execute(
        query=query, user_id=user_id,
        title=kwargs.get("title", ""),
        experience_level=kwargs.get("experience_level", ""),
        skills=kwargs.get("skills", []),
    )
    return {"job_description": result.get("job_description", "")}


async def generate_jd(title: str, experience_level: str = "", skills: list[str] = None):
    return await handle(
        query=f"Generate job description for {title}",
        title=title,
        experience_level=experience_level,
        skills=skills or [],
    )
