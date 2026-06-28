from typing import Optional
from .base_agent import BaseAgent
from app.prompts.job_prompt import INTERVIEW_SYSTEM_PROMPT


class InterviewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="interview_agent",
            description="Generates interview questions for any role",
        )

    def system_prompt(self) -> str:
        return INTERVIEW_SYSTEM_PROMPT

    async def execute(self, query: str, user_id: Optional[str] = None, **kwargs) -> dict:
        job_title = kwargs.get("job_title", "")
        skills = kwargs.get("skills", [])
        level = kwargs.get("experience_level", "mid")

        prompt = f"""
Generate interview questions for:
Role: {job_title}
Skills: {', '.join(skills)}
Level: {level}

Additional Context: {query}
"""
        questions = self.generate(prompt, system=INTERVIEW_SYSTEM_PROMPT)
        return {"questions": questions}
