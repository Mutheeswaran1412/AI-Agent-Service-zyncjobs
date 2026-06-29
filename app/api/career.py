from fastapi import APIRouter
from pydantic import BaseModel
from app.services import career_service

router = APIRouter()


class CareerAdviceRequest(BaseModel):
    current_role: str
    target_role: str
    skills: list[str] = []


@router.post("/advice")
async def career_advice(request: CareerAdviceRequest):
    return await career_service.get_career_advice(
        current_role=request.current_role,
        target_role=request.target_role,
        skills=request.skills,
    )
