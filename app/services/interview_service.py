from typing import Optional
from app.agents.interview_agent import InterviewAgent
from app.utils.logger import logger

interview_agent = InterviewAgent()


async def handle(query: str, user_id: Optional[str] = None, **kwargs) -> dict:
    logger.info("InterviewService.handle")
    result = await interview_agent.execute(
        query=query, user_id=user_id,
        job_title=kwargs.get("job_title", ""),
        skills=kwargs.get("skills", []),
        experience_level=kwargs.get("experience_level", "mid"),
    )
    return {"questions": result.get("questions", "")}


async def generate_questions(job_title: str, skills: list[str] = None, experience_level: str = "mid"):
    return await handle(
        query=f"Generate interview questions for {job_title}",
        job_title=job_title,
        skills=skills or [],
        experience_level=experience_level,
    )
