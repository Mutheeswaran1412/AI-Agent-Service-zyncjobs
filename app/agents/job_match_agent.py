from typing import Optional
from .base_agent import BaseAgent
from app.tools.ats_tool import ATSTool
from app.prompts.job_prompt import JOB_MATCH_SYSTEM_PROMPT


class JobMatchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="job_match_agent",
            description="Matches resumes to job descriptions and provides match scores",
        )
        self.ats = ATSTool()

    def system_prompt(self) -> str:
        return JOB_MATCH_SYSTEM_PROMPT

    async def execute(self, query: str, user_id: Optional[str] = None, **kwargs) -> dict:
        resume_text = kwargs.get("resume_text", "")
        job_description = kwargs.get("job_description", "")

        ats_result = self.ats.run(resume_text, job_description)

        prompt = f"""
Resume: {resume_text[:500]}
Job Description: {job_description[:500]}
ATS Score: {ats_result['score']}
Matching Keywords: {ats_result.get('matching_keywords', [])}
Missing Keywords: {ats_result.get('missing_keywords', [])}

Provide improvement suggestions.
"""
        suggestions = self.generate(prompt, system=JOB_MATCH_SYSTEM_PROMPT)

        return {
            "match_score": ats_result["score"],
            "matching_skills": ats_result.get("matching_keywords", []),
            "missing_skills": ats_result.get("missing_keywords", []),
            "suggestions": suggestions,
        }
