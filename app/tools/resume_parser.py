import re
from .base_tool import BaseTool


_SECTION_PATTERNS = {
    "contact": r"(contact|phone|email|address|linkedin)[:\s]*(.*?)(?=\n\s*\n|\Z)",
    "summary": r"(summary|profile|objective|about me)[:\s]*(.*?)(?=\n\s*\n|\Z)",
    "experience": r"(experience|work history|employment|work experience)[:\s]*(.*?)(?=\n\s*(education|skills|projects|certifications)\b|\Z)",
    "education": r"(education|academic|qualification|degree)[:\s]*(.*?)(?=\n\s*(skills|projects|certifications|experience)\b|\Z)",
    "skills": r"(skills|technologies|competencies|expertise)[:\s]*(.*?)(?=\n\s*(projects|certifications|education|experience)\b|\Z)",
    "projects": r"(projects|portfolio)[:\s]*(.*?)(?=\n\s*(skills|education|certifications|experience)\b|\Z)",
    "certifications": r"(certifications|certificates|licenses)[:\s]*(.*?)(?=\n\s*\n|\Z)",
}


class ResumeParserTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="resume_parser",
            description="Parses resume text into structured sections (contact, skills, experience, education)",
        )

    def run(self, resume_text: str) -> dict:
        sections = {}
        for section, pattern in _SECTION_PATTERNS.items():
            match = re.search(pattern, resume_text, re.IGNORECASE | re.DOTALL)
            sections[section] = match.group(2).strip() if match else ""

        lines = [l for l in resume_text.split("\n") if l.strip()]
        if not sections["contact"]:
            sections["contact"] = lines[0] if lines else ""

        return sections
