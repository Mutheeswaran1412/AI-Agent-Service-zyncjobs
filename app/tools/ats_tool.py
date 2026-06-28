import re
from .base_tool import BaseTool


class ATSTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="ats_tool",
            description="Compares resume against job description to calculate ATS score and find matching/missing keywords",
        )

    def run(self, resume_text: str, job_description: str) -> dict:
        resume_lower = resume_text.lower()
        jd_lower = job_description.lower()

        # extract keywords from job description
        stop_words = {"the", "a", "an", "and", "or", "in", "of", "to", "for", "with", "on", "at", "by", "is", "are", "be", "will", "we", "our", "your", "this", "that"}
        words = re.findall(r'\b[a-z]{3,}\b', jd_lower)
        keywords = set(w for w in words if w not in stop_words)

        matching = [k for k in keywords if k in resume_lower]
        missing = [k for k in keywords if k not in resume_lower]

        score = int((len(matching) / max(len(keywords), 1)) * 100) if keywords else 0

        return {
            "score": score,
            "matching_keywords": sorted(matching)[:20],
            "missing_keywords": sorted(missing)[:20],
        }
