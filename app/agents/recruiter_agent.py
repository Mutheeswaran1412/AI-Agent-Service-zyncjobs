from typing import Optional
from .base_agent import BaseAgent
from app.prompts.job_prompt import JD_SYSTEM_PROMPT


class RecruiterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="recruiter_agent",
            description="Generates job descriptions and helps recruiters",
        )

    def system_prompt(self) -> str:
        return JD_SYSTEM_PROMPT

    async def execute(self, query: str, user_id: Optional[str] = None, **kwargs) -> dict:
        title = kwargs.get("title", "")
        experience = kwargs.get("experience_level", "")
        skills = kwargs.get("skills", [])

        prompt = f"""
Generate a job description for:
Title: {title}
Experience Level: {experience}
Skills: {', '.join(skills)}

Additional Context: {query}
"""
        jd = self.generate(prompt, system=JD_SYSTEM_PROMPT)
        return {"job_description": jd}
