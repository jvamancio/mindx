from dotenv import load_dotenv
from pathlib import Path

from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver
from deepagents.backends import FilesystemBackend 
from agents.prompts.prompt_exemple import SYSTEM_PROMPT_EXEMPLE

# Carrega as variáveis do arquivo .env
load_dotenv()

root_dir = Path(__file__).parent
print(root_dir)
backend = FilesystemBackend(root_dir, virtual_mode=True)

def agent_modelo():
    system_prompt = SYSTEM_PROMPT_EXEMPLE
    # Instanciamos a memória da sessão
    memory_checkpointer = MemorySaver()

    # Inicializamos o agente
    agent = create_deep_agent(
        model="openai:gpt-4o",
        backend= backend,
        skills=["/skills"],
        system_prompt=system_prompt,
        checkpointer=memory_checkpointer,
    )
    return agent