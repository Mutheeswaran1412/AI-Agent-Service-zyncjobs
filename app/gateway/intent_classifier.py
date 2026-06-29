import re
from typing import Optional


_RULES = {
    "resume": ["resume", "cv", "cover letter", "ats", "improve resume"],
    "job_match": ["job match", "match resume", "job fit", "resume match", "ats score"],
    "interview": ["interview question", "mock interview", "interview"],
    "recruiter": ["generate job description", "create job description", "write jd", "recruiter", "post a job", "hire"],
    "career": ["career advice", "career", "skill gap", "learning path", "roadmap"],
}


class IntentClassifier:
    def classify(self, query: str, context: Optional[dict] = None) -> str:
        context = context or {}

        ctx_intent = self._from_context(context)
        if ctx_intent != "general":
            return ctx_intent

        query_lower = query.lower()
        scored = []
        for intent, keywords in _RULES.items():
            count = 0
            for kw in keywords:
                if re.search(rf"\b{re.escape(kw)}\b", query_lower):
                    count += 1
            if count:
                scored.append((count, intent))

        if not scored:
            return "general"

        scored.sort(key=lambda x: (-x[0], x[1]))
        return scored[0][1]

    def _from_context(self, ctx: dict) -> str:
        if ctx.get("resume_text") and ctx.get("job_description"):
            return "job_match"
        if ctx.get("resume_text"):
            return "resume"
        if ctx.get("job_title") and ctx.get("experience_level"):
            return "interview"
        if ctx.get("title"):
            return "recruiter"
        if ctx.get("current_role") and ctx.get("target_role"):
            return "career"
        return "general"
