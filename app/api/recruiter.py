from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class JDRequest(BaseModel):
    title: str
    experience_level: str
    skills: list[str]


@router.post("/generate-jd")
def generate_job_description(request: JDRequest):
    return {
        "job_title": request.title,
        "description": "We are looking for...",
        "responsibilities": ["Build APIs", "Write tests"],
        "requirements": ["3+ years experience"],
    }
