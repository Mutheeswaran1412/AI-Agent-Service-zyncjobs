import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AgentMetrics:
    total_requests: int = 0
    total_errors: int = 0
    total_time_ms: float = 0.0
    last_request_time: Optional[float] = None

    @property
    def avg_time_ms(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return round(self.total_time_ms / self.total_requests, 2)

    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 100.0
        return round((1 - self.total_errors / self.total_requests) * 100, 1)


class MetricsCollector:
    def __init__(self):
        self._agents: dict[str, AgentMetrics] = defaultdict(AgentMetrics)
        self._services: dict[str, AgentMetrics] = defaultdict(AgentMetrics)

    def record_agent(self, agent: str, elapsed_ms: float, error: bool = False):
        m = self._agents[agent]
        m.total_requests += 1
        m.total_time_ms += elapsed_ms
        if error:
            m.total_errors += 1
        m.last_request_time = time.time()

    def record_service(self, service: str, elapsed_ms: float, error: bool = False):
        m = self._services[service]
        m.total_requests += 1
        m.total_time_ms += elapsed_ms
        if error:
            m.total_errors += 1
        m.last_request_time = time.time()

    def get_agent_metrics(self, agent: str) -> AgentMetrics:
        return self._agents.get(agent, AgentMetrics())

    def get_service_metrics(self, service: str) -> AgentMetrics:
        return self._services.get(service, AgentMetrics())

    def summary(self) -> dict:
        return {
            "agents": {
                name: {
                    "requests": m.total_requests,
                    "avg_time_ms": m.avg_time_ms,
                    "errors": m.total_errors,
                    "success_rate": m.success_rate,
                }
                for name, m in self._agents.items()
            },
            "services": {
                name: {
                    "requests": m.total_requests,
                    "avg_time_ms": m.avg_time_ms,
                    "errors": m.total_errors,
                    "success_rate": m.success_rate,
                }
                for name, m in self._services.items()
            },
        }


metrics_collector = MetricsCollector()
