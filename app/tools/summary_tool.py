from .base_tool import BaseTool


class SummaryTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="summary_tool",
            description="Generates a concise professional summary from resume sections",
        )

    def run(self, sections: dict, max_words: int = 60) -> str:
        experience = sections.get("experience", "")[:200]
        skills = sections.get("skills", "")[:200]
        summary = sections.get("summary", "")

        if summary:
            return self._truncate(summary, max_words)

        parts = [p for p in [experience, skills] if p]
        if not parts:
            return ""

        combined = " | ".join(parts)
        return self._truncate(combined, max_words)

    def _truncate(self, text: str, max_words: int) -> str:
        words = text.split()
        if len(words) <= max_words:
            return text
        return " ".join(words[:max_words]) + "..."
