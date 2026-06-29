from fastapi import APIRouter
from pydantic import BaseModel
from app.services import recruiter_service

router = APIRouter()


class JDRequest(BaseModel):
    title: str
    experience_level: str = ""
    skills: list[str] = []


@router.post("/generate-jd")
async def generate_job_description(request: JDRequest):
    return await recruiter_service.generate_jd(
        title=request.title,
        experience_level=request.experience_level,
        skills=request.skills,
    )
