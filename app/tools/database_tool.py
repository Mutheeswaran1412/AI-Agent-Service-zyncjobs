from .base_tool import BaseTool


class DatabaseTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="database_tool",
            description="Stores and retrieves resume data, user profiles, and job matches from the database",
        )

    def save_resume(self, user_id: str, resume_data: dict) -> bool:
        # placeholder — will integrate PostgreSQL/Redis later
        return True

    def get_resume(self, user_id: str) -> dict:
        # placeholder
        return {}

    def save_job_match(self, user_id: str, match_data: dict) -> bool:
        return True
