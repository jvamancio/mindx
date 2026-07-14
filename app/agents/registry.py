# app/agents/registry.py
from enum import Enum
from functools import lru_cache
from typing import Callable, Any

from agents.teste_agent import agent_modelo


class AgentID(str, Enum):
    teste = "teste"


AGENT_FACTORIES: dict[AgentID, Callable[[], Any]] = {
    AgentID.teste: agent_modelo,
}

# Garante em tempo de import que AgentID e AGENT_FACTORIES nunca dessincronizam
assert set(AgentID) == set(AGENT_FACTORIES.keys()), \
    "AgentID e AGENT_FACTORIES fora de sincronia"


@lru_cache
def get_agent_instance(agent_id: AgentID) -> Any:
    factory = AGENT_FACTORIES[agent_id]
    return factory()