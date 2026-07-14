# app/core/config.py
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Teste Infra Mindx"
    PROJECT_DESCRIPTION: str = "API async para multiplos deep agents"


settings = Settings()