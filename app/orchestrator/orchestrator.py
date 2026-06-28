import re
from typing import Optional
from app.agents.base_agent import BaseAgent
from app.utils.logger import logger


class AgentOrchestrator:
    def __init__(self):
        self._agents: dict[str, BaseAgent] = {}

    def register(self, name: str, agent: BaseAgent):
        self._agents[name] = agent

    def route(self, query: str) -> tuple[str, BaseAgent]:
        query_lower = query.lower()

        keywords = {
            "resume": "resume",
            "ats": "resume",
            "cover letter": "resume",
            "cv": "resume",
            "career": "career",
            "job match": "job_match",
            "job description": "recruiter",
            "jd": "recruiter",
            "recruiter": "recruiter",
            "interview": "interview",
            "interview question": "interview",
            "skill": "career",
        }

        for keyword, agent_name in keywords.items():
            if re.search(keyword, query_lower):
                if agent_name in self._agents:
                    return agent_name, self._agents[agent_name]

        # fallback to first registered agent
        fallback = next(iter(self._agents.items()), (None, None))
        if fallback[1]:
            return fallback
        raise ValueError("No agents registered")

    async def handle(self, query: str, user_id: Optional[str] = None, **kwargs):
        agent_name, agent = self.route(query)
        logger.info("Orchestrator", agent=agent_name, query=query[:100])
        result = await agent.run(query, user_id=user_id, **kwargs)
        return {"agent": agent_name, **result}


orchestrator = AgentOrchestrator()
