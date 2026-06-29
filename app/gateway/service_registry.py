from typing import Optional, TypedDict, Any


class ServiceEntry(TypedDict, total=False):
    service: Any
    version: str
    description: str


class ServiceRegistry:
    def __init__(self):
        self._services: dict[str, ServiceEntry] = {}

    def register(self, name: str, service, version: str = "v1", description: str = ""):
        self._services[name] = {
            "service": service,
            "version": version,
            "description": description,
        }

    def get(self, name: str) -> Optional[Any]:
        entry = self._services.get(name)
        if entry is None:
            return None
        return entry["service"]

    def get_info(self, name: str) -> Optional[ServiceEntry]:
        return self._services.get(name)

    def list(self) -> list[str]:
        return list(self._services.keys())

    def list_with_info(self) -> dict[str, ServiceEntry]:
        return dict(self._services)

    def route(self, intent: str) -> Optional[Any]:
        service_map = {
            "resume": "resume_service",
            "career": "career_service",
            "recruiter": "recruiter_service",
            "interview": "interview_service",
            "job_match": "job_service",
            "general": "chat_service",
        }
        name = service_map.get(intent, "chat_service")
        entry = self._services.get(name)
        return entry["service"] if entry else None


service_registry = ServiceRegistry()
