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
    OLLAMA_READ_TIMEOUT: float = 5.0
    OLLAMA_CONNECT_TIMEOUT: float = 60.0

    LOG_LEVEL: str = "INFO"

    # Rate Limiting Configuration
    RATE_LIMIT_BACKEND: str = "memory"  # "memory", "redis"
    REDIS_URL: str = "redis://localhost:6379/0"
    DEFAULT_CHAT_LIMIT: int = 5         # Requests
    DEFAULT_CHAT_WINDOW: int = 60       # Seconds

def get_settings() -> Settings:
    return Settings()


settings = get_settings()