import re
from typing import Optional


class IntentClassifier:
    def __init__(self):
        self._rules = {
            "resume": ["resume", "cv", "cover letter", "ats"],
            "job_match": ["job match", "match resume", "job fit", "resume match", "ats score"],
            "interview": ["interview question", "mock interview", "interview"],
            "recruiter": ["generate job description", "create job description", "write jd", "recruiter", "post a job", "hire"],
            "career": ["career advice", "career", "skill gap", "learning path", "roadmap"],
        }

    def classify(self, query: str, context: Optional[dict] = None) -> str:
        context = context or {}
        query_lower = query.lower()

        query_intent = self._classify_by_query(query_lower)
        context_intent = self._classify_by_context(context)

        if query_intent != "general":
            return query_intent
        return context_intent

    def _classify_by_query(self, query_lower: str) -> str:
        scored = {}
        for intent, keywords in self._rules.items():
            match_count = 0
            for keyword in keywords:
                if re.search(rf"\b{re.escape(keyword)}\b", query_lower):
                    match_count += 1
            if match_count > 0:
                scored[intent] = match_count

        if not scored:
            return "general"

        best = max(scored, key=lambda k: (scored[k], len(k)))
        return best

    def _classify_by_context(self, context: dict) -> str:
        has_resume = bool(context.get("resume_text"))
        has_jd = bool(context.get("job_description"))
        has_title = bool(context.get("job_title") or context.get("title"))
        has_level = bool(context.get("experience_level"))
        has_current = bool(context.get("current_role"))
        has_target = bool(context.get("target_role"))

        if has_resume and has_jd:
            return "job_match"
        if has_resume:
            return "resume"
        if has_title and has_level:
            return "interview"
        if has_title:
            return "recruiter"
        if has_current and has_target:
            return "career"
        return "general"
