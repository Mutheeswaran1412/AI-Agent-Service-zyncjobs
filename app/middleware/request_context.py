import uuid
import time
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id", default="")
user_id_var: ContextVar[str] = ContextVar("user_id", default="")
intent_var: ContextVar[str] = ContextVar("intent", default="")
service_var: ContextVar[str] = ContextVar("service", default="")
agent_var: ContextVar[str] = ContextVar("agent", default="")


def get_request_id() -> str:
    return request_id_var.get()


def get_user_id() -> str:
    return user_id_var.get()


def get_intent() -> str:
    return intent_var.get()


def get_service() -> str:
    return service_var.get()


def get_agent() -> str:
    return agent_var.get()


def set_request_context(user_id: str = "", intent: str = "", service: str = "", agent: str = ""):
    if not request_id_var.get():
        request_id_var.set(f"REQ-{uuid.uuid4().hex[:8].upper()}")
    if user_id:
        user_id_var.set(user_id)
    if intent:
        intent_var.set(intent)
    if service:
        service_var.set(service)
    if agent:
        agent_var.set(agent)


def format_context() -> str:
    parts = []
    rid = request_id_var.get()
    if rid:
        parts.append(f"[{rid}]")
    uid = user_id_var.get()
    if uid:
        parts.append(f"user={uid}")
    intent = intent_var.get()
    if intent:
        parts.append(f"intent={intent}")
    service = service_var.get()
    if service:
        parts.append(f"service={service}")
    agent = agent_var.get()
    if agent:
        parts.append(f"agent={agent}")
    return " ".join(parts) if parts else ""
