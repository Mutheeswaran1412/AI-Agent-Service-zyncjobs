import time
from typing import Optional
from .service_registry import service_registry
from .service_locator import service_locator
from .intent_classifier import IntentClassifier
from app.middleware.request_context import set_request_context, format_context, get_request_id
from app.metrics.collector import metrics_collector
from app.utils.logger import logger
from app.exceptions import ServiceException


class ApiGateway:
    def __init__(self):
        self.classifier = IntentClassifier()

    async def route(self, query: str, user_id: Optional[str] = None, **kwargs) -> dict:
        start = time.time()
        intent = self.classifier.classify(query, kwargs)

        service = service_registry.route(intent)
        if not service:
            raise ServiceException(f"No service for intent: {intent}", code="ROUTE_ERROR")

        service_name = type(service).__name__
        set_request_context(user_id=user_id or "", intent=intent, service=service_name)

        ctx = format_context()
        logger.info(f"{ctx} routing query={query[:80]}")

        error = False
        try:
            result = await service.handle(query, user_id=user_id, intent=intent, **kwargs)
            elapsed = round((time.time() - start) * 1000, 2)
            metrics_collector.record_service(service_name, elapsed, error=False)
            logger.info(f"{ctx} completed {elapsed}ms")
            return {"intent": intent, **result}
        except Exception as e:
            elapsed = round((time.time() - start) * 1000, 2)
            metrics_collector.record_service(service_name, elapsed, error=True)
            logger.error(f"{ctx} failed {elapsed}ms | error={str(e)}")
            raise


gateway = ApiGateway()
