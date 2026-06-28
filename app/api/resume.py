from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ImproveRequest(BaseModel):
    resume_text: str
    job_description: str = ""


class ImproveResponse(BaseModel):
    improved_resume: str
    ats_score: int
    summary: str
    skills_suggested: list[str]


@router.post("/improve")
def improve_resume(request: ImproveRequest):
    return ImproveResponse(
        improved_resume="Improved resume content here...",
        ats_score=75,
        summary="Your resume is well structured.",
        skills_suggested=["Python", "FastAPI", "Machine Learning"],
    )


@router.post("/parse")
def parse_resume(resume_text: str):
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "skills": ["Python", "FastAPI"],
        "experience": [],
        "education": [],
    }


@router.post("/ats-score")
def ats_score(resume_text: str, job_description: str):
    return {"score": 75, "keywords_found": [], "keywords_missing": []}
