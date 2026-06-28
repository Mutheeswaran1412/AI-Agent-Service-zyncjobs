from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from app.config.settings import settings
from app.api.chat import router as chat_router
from app.api.resume import router as resume_router
from app.api.career import router as career_router
from app.api.recruiter import router as recruiter_router
from app.api.interview import router as interview_router
from app.api.job import router as job_router
from app.orchestrator.orchestrator import orchestrator
from app.agents.resume_agent import ResumeAgent
from app.agents.career_agent import CareerAgent
from app.agents.recruiter_agent import RecruiterAgent
from app.agents.interview_agent import InterviewAgent
from app.agents.job_match_agent import JobMatchAgent
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting ZyncJobs AI Service")
    orchestrator.register("resume", ResumeAgent())
    orchestrator.register("career", CareerAgent())
    orchestrator.register("recruiter", RecruiterAgent())
    orchestrator.register("interview", InterviewAgent())
    orchestrator.register("job_match", JobMatchAgent())
    logger.info("All agents registered", agents=list(orchestrator._agents.keys()))
    yield
    logger.info("Shutting down ZyncJobs AI Service")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.include_router(chat_router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(resume_router, prefix="/api/v1/resume", tags=["Resume"])
app.include_router(career_router, prefix="/api/v1/career", tags=["Career"])
app.include_router(recruiter_router, prefix="/api/v1/recruiter", tags=["Recruiter"])
app.include_router(interview_router, prefix="/api/v1/interview", tags=["Interview"])
app.include_router(job_router, prefix="/api/v1/job", tags=["Job"])


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.APP_NAME, "version": settings.APP_VERSION}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Request", method=request.method, path=request.url.path)
    response = await call_next(request)
    logger.info("Response", status=response.status_code, path=request.url.path)
    return response
