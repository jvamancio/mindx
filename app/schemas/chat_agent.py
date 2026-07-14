# app/schemas/chat_agent.py
from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str
    session_id: str

class AgentResponse(BaseModel):
    response: str
    agent_id: str