from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  

from agents.teste_agent import agent_modelo

# Carrega as variáveis do arquivo .env
load_dotenv()

app = FastAPI(
    title="Teste Infra Mindx",
    description="API async para multiplos deep agents"
)

agent = agent_modelo()

class QuestionRequest(BaseModel):
    question: str
    session_id: str

class AgentResponse(BaseModel):
    response: str

@app.post("/ask", response_model=AgentResponse)
async def ask_agent(payload: QuestionRequest):
    try:
        # Executa o agente assincronamente com sintaxe simplificada de tupla
        result = await agent.ainvoke(
            {"messages": [("user", payload.question)]},
            config={"configurable": {"thread_id": payload.session_id}}
        )
        
        # Pega a última mensagem (resposta do agente)
        last_message = result["messages"][-1]
        content = last_message.content
        
        # Simplificação drástica:
        # 1. Se for string pura (comum), apenas converte (fallback seguro).
        # 2. Se for uma lista (ex: bloco multimodal), busca a chave "text" via generator.
        if isinstance(content, list):
            final_answer = next((b["text"] for b in content if isinstance(b, dict) and "text" in b), str(content))
        else:
            final_answer = str(content)
        
        return AgentResponse(response=final_answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)