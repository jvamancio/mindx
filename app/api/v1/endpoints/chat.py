# app/api/v1/endpoints/chat.py
from fastapi import APIRouter, Depends, HTTPException

from schemas.chat_agent import QuestionRequest, AgentResponse
from services.agent_service import AgentService
from api.deps import get_agent_service
from agents.registry import AgentID

router = APIRouter(prefix="/ask", tags=["agent"])


@router.post("/{agent_id}", response_model=AgentResponse)
async def ask_agent(
    agent_id: AgentID,
    payload: QuestionRequest,
    service: AgentService = Depends(get_agent_service),
):
    try:
        answer = await service.ask(
            agent_id=agent_id.value,
            question=payload.question,
            session_id=payload.session_id,
        )
        return AgentResponse(response=answer, agent_id=agent_id.value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))