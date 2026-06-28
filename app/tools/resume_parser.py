import re
from .base_tool import BaseTool


class ResumeParserTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="resume_parser",
            description="Parses resume text into structured sections (contact, skills, experience, education)",
        )

    def run(self, resume_text: str) -> dict:
        sections = {
            "contact": self._extract_section(resume_text, "contact", "summary"),
            "summary": self._extract_section(resume_text, "summary", "experience"),
            "experience": self._extract_section(resume_text, "experience", "education"),
            "education": self._extract_section(resume_text, "education", "skills"),
            "skills": self._extract_section(resume_text, "skills", None),
        }
        return sections

    def _extract_section(self, text: str, section: str, next_section: str | None) -> str:
        pattern = rf"{section}[:\s]*(.*?)(?={next_section}[:\s]|$)" if next_section else rf"{section}[:\s]*(.*)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else ""
