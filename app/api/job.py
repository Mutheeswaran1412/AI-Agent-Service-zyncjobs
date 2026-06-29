from fastapi import APIRouter
from pydantic import BaseModel
from app.services import job_service

router = APIRouter()


class MatchRequest(BaseModel):
    resume_text: str
    job_description: str


@router.post("/match")
async def job_match(request: MatchRequest):
    return await job_service.match_resume_to_job(
        resume_text=request.resume_text,
        job_description=request.job_description,
    )
