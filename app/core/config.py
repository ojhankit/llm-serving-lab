from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    API_TITLE: str = "LLM Serving API"
    API_VERSION: str = "1.0.0"

    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_TIMEOUT: float = 120.0

    LOG_LEVEL: str = "INFO"

def get_settings() -> Settings:
    return Settings()


settings = get_settings()