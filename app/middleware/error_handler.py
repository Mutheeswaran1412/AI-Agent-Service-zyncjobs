from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.logger import logger
from app.exceptions import AIException
from app.middleware.request_context import format_context


def register_error_handlers(app):
    @app.exception_handler(AIException)
    async def ai_exception_handler(request: Request, exc: AIException):
        ctx = format_context()
        logger.error(f"{ctx} AIException | code={exc.code} | {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": exc.code, "message": str(exc)},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        ctx = format_context()
        logger.error(f"{ctx} Unhandled error | {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Internal server error"},
        )
