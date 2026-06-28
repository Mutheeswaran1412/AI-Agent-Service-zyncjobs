from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class CareerAdviceRequest(BaseModel):
    current_role: str
    target_role: str
    skills: list[str]


@router.post("/advice")
def career_advice(request: CareerAdviceRequest):
    return {
        "recommended_skills": ["System Design", "Leadership"],
        "learning_path": ["Course A", "Course B"],
        "timeline": "6 months",
    }
