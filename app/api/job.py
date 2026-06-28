from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class MatchRequest(BaseModel):
    resume_text: str
    job_description: str


@router.post("/match")
def job_match(request: MatchRequest):
    return {
        "match_score": 82,
        "matching_skills": ["Python", "FastAPI"],
        "missing_skills": ["Docker"],
        "suggestions": "Add Docker to your skills section.",
    }
