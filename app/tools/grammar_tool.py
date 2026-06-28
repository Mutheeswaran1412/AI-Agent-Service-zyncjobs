import re
from .base_tool import BaseTool


class GrammarTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="grammar_tool",
            description="Checks resume text for common grammar and spelling issues",
        )

    def run(self, text: str) -> list[str]:
        issues = []

        # check for double spaces
        if re.search(r'  ', text):
            issues.append("Double spaces found")

        # check for common typos
        typos = {
            "responsiblities": "responsibilities",
            "managment": "management",
            "experiance": "experience",
            "acheivement": "achievement",
            "recieved": "received",
            "tehnical": "technical",
            "developped": "developed",
        }
        for typo, correction in typos.items():
            if re.search(rf'\b{typo}\b', text, re.IGNORECASE):
                issues.append(f"'{typo}' should be '{correction}'")

        # check for passive voice indicators
        passive = re.findall(r'\b(was|were|been|being)\s+\w+ed\b', text, re.IGNORECASE)
        if passive:
            issues.append(f"Consider reducing passive voice ({len(passive)} instances)")

        return issues
