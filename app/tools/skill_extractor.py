import re
from .base_tool import BaseTool


SKILL_KEYWORDS = {
    "python", "java", "javascript", "typescript", "golang", "rust", "c++", "c#",
    "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "sql",
    "react", "angular", "vue", "node", "django", "flask", "fastapi", "spring",
    "docker", "kubernetes", "aws", "gcp", "azure", "terraform", "ansible",
    "git", "ci/cd", "jenkins", "github actions", "linux", "bash",
    "postgresql", "mongodb", "redis", "mysql", "elasticsearch",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
    "rest api", "graphql", "grpc", "websocket", "oauth", "jwt",
    "agile", "scrum", "jira", "confluence", "project management",
    "leadership", "communication", "teamwork", "mentoring",
}


class SkillExtractorTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="skill_extractor",
            description="Extracts known technical and soft skills from any text",
        )

    def run(self, text: str) -> list[str]:
        text_lower = text.lower()
        found = set()
        for skill in SKILL_KEYWORDS:
            if re.search(rf"\b{re.escape(skill)}\b", text_lower):
                found.add(skill)
        return sorted(found)

    def extract_from_resume(self, resume_sections: dict) -> list[str]:
        combined = " ".join(resume_sections.values())
        return self.run(combined)

    def suggest_missing(self, current: list[str], desired: list[str]) -> list[str]:
        current_set = set(s.lower() for s in current)
        return [s for s in desired if s.lower() not in current_set]
