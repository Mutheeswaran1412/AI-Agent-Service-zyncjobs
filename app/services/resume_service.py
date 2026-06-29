from typing import Optional
from app.agents.resume_agent import ResumeAgent
from app.tools.resume_parser import ResumeParserTool
from app.tools.ats_tool import ATSTool
from app.utils.logger import logger

resume_agent = ResumeAgent()
parser = ResumeParserTool()
ats_tool = ATSTool()


async def handle(query: str, user_id: Optional[str] = None, **kwargs) -> dict:
    logger.info("ResumeService.handle")
    resume_text = kwargs.get("resume_text", "")
    job_description = kwargs.get("job_description", "")
    result = await resume_agent.execute(
        query=query, user_id=user_id,
        resume_text=resume_text,
        job_description=job_description,
    )
    return {
        "improved_resume": result.get("improved_resume", ""),
        "ats_score": result.get("ats_score"),
        "summary": result.get("summary", ""),
        "skills_suggested": result.get("skills_suggested", []),
        "grammar_issues": result.get("grammar_issues", []),
    }


async def improve_resume(resume_text: str, job_description: str = ""):
    return await handle(
        query="Improve my resume",
        resume_text=resume_text,
        job_description=job_description,
    )


def parse_resume(resume_text: str):
    logger.info("ResumeService.parse_resume")
    sections = parser.run(resume_text)
    return {
        "contact": sections.get("contact", ""),
        "summary": sections.get("summary", ""),
        "experience": sections.get("experience", ""),
        "education": sections.get("education", ""),
        "skills": sections.get("skills", ""),
    }


def ats_score(resume_text: str, job_description: str):
    logger.info("ResumeService.ats_score")
    result = ats_tool.run(resume_text, job_description)
    return {
        "score": result.get("score", 0),
        "matching_keywords": result.get("matching_keywords", []),
        "missing_keywords": result.get("missing_keywords", []),
    }
