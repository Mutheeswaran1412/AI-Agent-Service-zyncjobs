import time
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import logger
from app.middleware.request_context import set_request_context, format_context


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        set_request_context()
        response = await call_next(request)
        elapsed = round((time.time() - start) * 1000, 2)
        ctx = format_context()
        if ctx:
            logger.info(f"{ctx} {request.method} {request.url.path} {response.status_code} {elapsed}ms")
        else:
            logger.info(f"{request.method} {request.url.path} {response.status_code} {elapsed}ms")
        return response
