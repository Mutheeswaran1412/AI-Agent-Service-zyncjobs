from typing import Optional
from .base_agent import BaseAgent
from app.prompts.resume_prompt import (
    IMPROVE_SYSTEM_PROMPT,
    ATS_SCORE_SYSTEM_PROMPT,
    SUMMARY_SYSTEM_PROMPT,
    SKILLS_SYSTEM_PROMPT,
    COVER_LETTER_SYSTEM_PROMPT,
)
from app.tools.resume_parser import ResumeParserTool
from app.tools.ats_tool import ATSTool
from app.tools.grammar_tool import GrammarTool
from app.utils.logger import logger


class ResumeAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="resume_agent",
            description="Handles resume improvement, ATS scoring, summaries, skill suggestions, and cover letters",
        )
        self.parser = ResumeParserTool()
        self.ats = ATSTool()
        self.grammar = GrammarTool()

    def system_prompt(self) -> str:
        return IMPROVE_SYSTEM_PROMPT

    async def execute(self, query: str, user_id: Optional[str] = None, **kwargs) -> dict:
        resume_text = kwargs.get("resume_text", "")
        job_description = kwargs.get("job_description", "")

        # 1. Parse resume
        parsed = self.parser.run(resume_text)
        logger.info("ResumeAgent parsed resume", sections=list(parsed.keys()))

        # 2. Grammar check
        grammar_issues = self.grammar.run(resume_text)

        # 3. ATS score if job description provided
        ats_result = {}
        if job_description:
            ats_result = self.ats.run(resume_text, job_description)
            logger.info("ResumeAgent ATS score", score=ats_result.get("score"))

        # 4. Generate improved resume
        improve_prompt = f"""
Original Resume:
{resume_text}

Parsed Sections: {parsed}
Grammar Issues: {grammar_issues}
"""
        if ats_result:
            improve_prompt += f"\nATS Score: {ats_result['score']}\nMissing Keywords: {ats_result.get('missing_keywords', [])}"

        improved = self.generate(improve_prompt, system=IMPROVE_SYSTEM_PROMPT)

        # 5. Generate summary
        summary = self.generate(
            f"Summarize this resume:\n{resume_text}",
            system=SUMMARY_SYSTEM_PROMPT,
        )

        # 6. Suggest skills
        skills_raw = self.generate(
            f"Suggest skills for this resume:\n{resume_text}",
            system=SKILLS_SYSTEM_PROMPT,
        )
        skills_list = [s.strip() for s in skills_raw.split(",") if s.strip()]

        return {
            "improved_resume": improved,
            "ats_score": ats_result.get("score", 0) if ats_result else None,
            "summary": summary,
            "skills_suggested": skills_list[:10],
            "grammar_issues": grammar_issues,
        }
