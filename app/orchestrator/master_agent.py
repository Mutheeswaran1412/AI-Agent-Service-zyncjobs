from typing import Optional
from app.agents.base_agent import BaseAgent
from app.orchestrator.intent_classifier import IntentClassifier
from app.utils.logger import logger


class MasterAgent:
    def __init__(self):
        self._agents: dict[str, BaseAgent] = {}
        self.classifier = IntentClassifier()

    def register(self, name: str, agent: BaseAgent):
        self._agents[name] = agent

    def get_agent(self, name: str) -> Optional[BaseAgent]:
        return self._agents.get(name)

    async def process(
        self, query: str, user_id: Optional[str] = None, **kwargs
    ) -> dict:
        intent = self.classifier.classify(query, kwargs)
        logger.info(f"MasterAgent routing | intent={intent} | query_length={len(query)}")

        agent = self._agents.get(intent)
        if not agent:
            agent = next(iter(self._agents.values()), None)
            intent = "general"

        if not agent:
            raise ValueError("No agents registered")

        result = await agent.run(query, user_id=user_id, **kwargs)
        return {"intent": intent, "agent": agent.name, **result}


master_agent = MasterAgent()
