from pydantic import BaseModel


class OllamaStatus(BaseModel):
    reachable: bool
    base_url: str


class HealthResponse(BaseModel):
    status: str  # "ok" | "degraded"
    ollama: OllamaStatus