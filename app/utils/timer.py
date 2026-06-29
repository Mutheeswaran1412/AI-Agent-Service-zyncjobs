import time
import functools
from app.utils.logger import logger


def measure_time(name: str = None):
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                elapsed = round((time.time() - start) * 1000, 2)
                label = name or func.__name__
                logger.info(f"[TIMER] {label} {elapsed}ms")
        return async_wrapper
    return decorator
