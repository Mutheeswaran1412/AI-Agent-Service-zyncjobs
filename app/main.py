from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx
from app.config.settings import settings
from app.api.chat import router as chat_router
from app.api.resume import router as resume_router
from app.api.career import router as career_router
from app.api.recruiter import router as recruiter_router
from app.api.interview import router as interview_router
from app.api.job import router as job_router
from app.api.knowledge import router as knowledge_router
from app.gateway.service_registry import service_registry
from app.services import resume_service, career_service, interview_service, recruiter_service, job_service, chat_service
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.error_handler import register_error_handlers
from app.knowledge.knowledge_base import knowledge_base
from app.memory.memory_manager import memory
from app.memory.cache import prompt_cache
from app.metrics.collector import metrics_collector
from app.utils.logger import logger


def _count_agents() -> int:
    try:
        from app.agents import resume_agent, career_agent, interview_agent
        from app.agents import recruiter_agent, job_match_agent, chat_agent
        return 6
    except Exception:
        return 0


def _count_tools() -> int:
    try:
        from app.tools import base_tool, resume_parser, ats_tool, grammar_tool
        from app.tools import skill_extractor, summary_tool, keyword_tool, pdf_tool, database_tool
        return 8
    except Exception:
        return 0


@asynccontextmanager
async def lifespan(app: FastAPI):
    service_registry.register(
        name="resume_service",
        service=resume_service,
        version="v1",
        description="Resume AI Services",
    )
    service_registry.register(
        name="career_service",
        service=career_service,
        version="v1",
        description="Career AI Services",
    )
    service_registry.register(
        name="interview_service",
        service=interview_service,
        version="v1",
        description="Interview AI Services",
    )
    service_registry.register(
        name="recruiter_service",
        service=recruiter_service,
        version="v1",
        description="Recruiter AI Services",
    )
    service_registry.register(
        name="job_service",
        service=job_service,
        version="v1",
        description="Job Match AI Services",
    )
    service_registry.register(
        name="chat_service",
        service=chat_service,
        version="v1",
        description="Conversational AI Services",
    )

    agent_count = _count_agents()
    tool_count = _count_tools()

    BANNER = f"""
{'='*50}
  {settings.APP_NAME}
{'='*50}
  Version      : {settings.APP_VERSION}
  LLM          : Ollama ({settings.OLLAMA_MODEL})
  Agents       : {agent_count} registered
  Services     : {len(service_registry.list())} registered
  Tools        : {tool_count} loaded
  Knowledge    : {knowledge_base.document_count} documents
  Memory       : Loaded
  Cache        : {prompt_cache.size} entries
  Metrics      : Active
  Gateway      : Ready
{'='*50}
"""
    logger.info(BANNER)
    yield
    logger.info(f"Shutting down {settings.APP_NAME}")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

register_error_handlers(app)
app.add_middleware(LoggingMiddleware)

app.include_router(chat_router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(resume_router, prefix="/api/v1/resume", tags=["Resume"])
app.include_router(career_router, prefix="/api/v1/career", tags=["Career"])
app.include_router(recruiter_router, prefix="/api/v1/recruiter", tags=["Recruiter"])
app.include_router(interview_router, prefix="/api/v1/interview", tags=["Interview"])
app.include_router(job_router, prefix="/api/v1/job", tags=["Job"])
app.include_router(knowledge_router, prefix="/api/v1/knowledge", tags=["Knowledge"])


@app.get("/health")
async def health():
    ollama_status = "unknown"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=3)
            ollama_status = "connected" if resp.status_code == 200 else "error"
    except Exception:
        ollama_status = "unreachable"

    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "ollama": ollama_status,
        "model": settings.OLLAMA_MODEL,
        "memory": "ok" if memory else "error",
        "knowledge": f"{knowledge_base.document_count} docs loaded" if knowledge_base.document_count else "empty",
        "services": len(service_registry.list()),
        "agents": _count_agents(),
        "tools": _count_tools(),
        "cache": prompt_cache.size,
    }


@app.get("/version")
def version():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "llm": "ollama",
        "model": settings.OLLAMA_MODEL,
        "services": service_registry.list_with_info(),
    }


@app.get("/metrics")
def metrics():
    return metrics_collector.summary()
