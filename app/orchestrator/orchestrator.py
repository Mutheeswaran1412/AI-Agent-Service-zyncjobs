from app.orchestrator.master_agent import master_agent
from typing import Optional
from app.utils.logger import logger


class AgentOrchestrator:
    async def handle(self, query: str, user_id: Optional[str] = None, **kwargs):
        logger.info("AgentOrchestrator.handle", query=query[:100])
        return await master_agent.process(query=query, user_id=user_id, **kwargs)

    def register(self, name: str, agent):
        master_agent.register(name, agent)


orchestrator = AgentOrchestrator()
