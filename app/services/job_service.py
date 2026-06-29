from typing import Optional
from app.agents.job_match_agent import JobMatchAgent
from app.utils.logger import logger

job_match_agent = JobMatchAgent()


async def handle(query: str, user_id: Optional[str] = None, **kwargs) -> dict:
    logger.info("JobService.handle")
    result = await job_match_agent.execute(
        query=query, user_id=user_id,
        resume_text=kwargs.get("resume_text", ""),
        job_description=kwargs.get("job_description", ""),
    )
    return {
        "match_score": result.get("match_score", 0),
        "matching_skills": result.get("matching_skills", []),
        "missing_skills": result.get("missing_skills", []),
        "suggestions": result.get("suggestions", ""),
    }


async def match_resume_to_job(resume_text: str, job_description: str):
    return await handle(
        query="Match resume to job description",
        resume_text=resume_text,
        job_description=job_description,
    )
