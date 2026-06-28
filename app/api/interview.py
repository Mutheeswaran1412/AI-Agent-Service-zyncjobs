from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class InterviewRequest(BaseModel):
    job_title: str
    skills: list[str]
    experience_level: str


@router.post("/questions")
def generate_questions(request: InterviewRequest):
    return {
        "questions": [
            "Explain polymorphism.",
            "Describe REST vs GraphQL.",
            "How do you handle errors in Python?",
        ],
        "categories": ["Technical", "Behavioral"],
    }
