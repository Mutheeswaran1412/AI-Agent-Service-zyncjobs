from fastapi import APIRouter
from pydantic import BaseModel
from app.orchestrator.orchestrator import orchestrator
from app.utils.logger import logger

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    user_id: str = "anonymous"


class ChatResponse(BaseModel):
    reply: str
    agent: str


@router.post("")
async def chat(request: ChatRequest):
    logger.info("Chat request", user_id=request.user_id, message=request.message[:100])
    result = await orchestrator.handle(
        query=request.message,
        user_id=request.user_id,
    )
    return ChatResponse(
        reply=result.get("improved_resume") or
               result.get("advice") or
               result.get("job_description") or
               result.get("questions") or
               str(result),
        agent=result.get("agent", "unknown"),
    )
