from dotenv import load_dotenv
from pathlib import Path

from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver
from deepagents.backends import FilesystemBackend 

# Carrega as variáveis do arquivo .env
load_dotenv()

root_dir = Path(__file__).parent.parent
print(root_dir)
backend = FilesystemBackend(root_dir, virtual_mode=True)

def agent_modelo():
    SYSTEM_PROMPT = "Você é um assistente de dúvidas a respeito de engenharia de telecomunicações."

    # Instanciamos a memória da sessão
    memory_checkpointer = MemorySaver()

    # Inicializamos o agente
    agent = create_deep_agent(
        model="openai:gpt-4o",
        backend= backend,
        skills=["/skills"],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=memory_checkpointer,
    )
    return agent