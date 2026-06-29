from fastapi import APIRouter
from pydantic import BaseModel
from app.gateway.api_gateway import gateway
from app.utils.logger import logger

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    user_id: str = "anonymous"


class ChatResponse(BaseModel):
    reply: str
    agent: str
    intent: str


@router.post("")
async def chat(request: ChatRequest):
    logger.info(f"Chat request | user_id={request.user_id}")
    result = await gateway.route(
        query=request.message,
        user_id=request.user_id,
    )
    reply = (
        result.get("reply")
        or result.get("improved_resume")
        or result.get("advice")
        or result.get("job_description")
        or result.get("questions")
        or result.get("suggestions")
        or str(result)
    )
    return ChatResponse(
        reply=reply,
        agent=result.get("intent", "general"),
        intent=result.get("intent", "general"),
    )
