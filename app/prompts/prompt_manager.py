from typing import Optional
from .system_prompt import (
    SYSTEM_PROMPT,
    RESUME_SYSTEM_PROMPT,
    SUMMARY_SYSTEM_PROMPT,
    SKILLS_SYSTEM_PROMPT,
    CAREER_SYSTEM_PROMPT,
    JD_SYSTEM_PROMPT,
    INTERVIEW_SYSTEM_PROMPT,
    JOB_MATCH_SYSTEM_PROMPT,
)


class PromptManager:
    def __init__(self):
        self._templates = {}

    def get_system_prompt(self, domain: str = "general") -> str:
        prompts = {
            "general": SYSTEM_PROMPT,
            "resume": RESUME_SYSTEM_PROMPT,
            "career": CAREER_SYSTEM_PROMPT,
            "recruiter": JD_SYSTEM_PROMPT,
            "interview": INTERVIEW_SYSTEM_PROMPT,
            "job_match": JOB_MATCH_SYSTEM_PROMPT,
        }
        return prompts.get(domain, SYSTEM_PROMPT)

    def build_resume_prompt(
        self, resume_text: str, parsed: dict, grammar_issues: list,
        ats_result: Optional[dict] = None, detected_skills: Optional[list] = None
    ) -> str:
        parts = [f"Original Resume:\n{resume_text}"]
        parts.append(f"Parsed Sections: {parsed}")
        parts.append(f"Grammar Issues: {grammar_issues}")
        if detected_skills:
            parts.append(f"Detected Skills: {detected_skills}")
        if ats_result:
            parts.append(f"ATS Score: {ats_result.get('score', 0)}")
            parts.append(f"Missing Keywords: {ats_result.get('missing_keywords', [])}")
        return "\n\n".join(parts)

    def build_summary_prompt(self, resume_text: str) -> str:
        return f"Summarize this resume:\n{resume_text}"

    def build_skills_prompt(self, resume_text: str, detected: Optional[list] = None) -> str:
        prompt = f"Suggest skills for this resume:\n{resume_text}"
        if detected:
            prompt += f"\nAlready detected: {detected}"
        return prompt

    def build_career_prompt(self, query: str, history: Optional[list] = None) -> str:
        parts = [f"User Query: {query}"]
        if history:
            parts.append(f"Previous Context: {history[-5:]}")
        else:
            parts.append("Previous Context: No previous context")
        return "\n\n".join(parts)

    def build_interview_prompt(self, job_title: str, skills: list, level: str, query: str = "") -> str:
        return f"""Generate interview questions for:
Role: {job_title}
Skills: {', '.join(skills)}
Level: {level}

Additional Context: {query}"""

    def build_jd_prompt(self, title: str, experience: str, skills: list, query: str = "") -> str:
        return f"""Generate a job description for:
Title: {title}
Experience Level: {experience}
Skills: {', '.join(skills)}

Additional Context: {query}"""

    def build_job_match_prompt(self, resume_text: str, job_description: str, ats_result: dict) -> str:
        return f"""Resume: {resume_text[:500]}
Job Description: {job_description[:500]}
ATS Score: {ats_result['score']}
Matching Keywords: {ats_result.get('matching_keywords', [])}
Missing Keywords: {ats_result.get('missing_keywords', [])}

Provide improvement suggestions."""


prompt_manager = PromptManager()
