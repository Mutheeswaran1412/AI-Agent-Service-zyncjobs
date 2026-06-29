from fastapi import APIRouter
from pydantic import BaseModel
from app.services import interview_service

router = APIRouter()


class InterviewRequest(BaseModel):
    job_title: str
    skills: list[str] = []
    experience_level: str = "mid"


@router.post("/questions")
async def generate_questions(request: InterviewRequest):
    return await interview_service.generate_questions(
        job_title=request.job_title,
        skills=request.skills,
        experience_level=request.experience_level,
    )
