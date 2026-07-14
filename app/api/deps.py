# app/api/deps.py
from services.agent_service import AgentService


def get_agent_service() -> AgentService:
    return AgentService()