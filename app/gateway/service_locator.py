from .service_registry import service_registry


class ServiceLocator:
    def resolve(self, name: str):
        service = service_registry.get(name)
        if service is None:
            raise ValueError(f"Service '{name}' not found in registry")
        return service

    def resolve_by_intent(self, intent: str):
        service = service_registry.route(intent)
        if service is None:
            raise ValueError(f"No service for intent '{intent}'")
        return service

    def available(self) -> list[dict]:
        info = service_registry.list_with_info()
        return [
            {"name": name, "version": entry.get("version", ""), "description": entry.get("description", "")}
            for name, entry in info.items()
        ]


service_locator = ServiceLocator()
