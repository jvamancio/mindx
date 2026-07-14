# app/services/agent_service.py
from typing import Any

from agents.registry import get_agent_instance


class AgentService:
    async def ask(self, agent_id: str, question: str, session_id: str) -> str:
        agent = get_agent_instance(agent_id)

        result = await agent.ainvoke(
            {"messages": [("user", question)]},
            config={"configurable": {"thread_id": session_id}},
        )

        last_message = result["messages"][-1]
        content = last_message.content

        return self._extract_text(content)

    @staticmethod
    def _extract_text(content: Any) -> str:
        if isinstance(content, list):
            return next(
                (b["text"] for b in content if isinstance(b, dict) and "text" in b),
                str(content),
            )
        return str(content)