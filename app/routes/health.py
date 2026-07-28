from fastapi import APIRouter

from app.clients.ollama import ollama_client
from app.core.config import settings
from app.schemas.health import HealthResponse, OllamaStatus

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    ollama_alive = await ollama_client.is_alive()

    return HealthResponse(
        status="ok" if ollama_alive else "degraded",
        ollama=OllamaStatus(
            reachable=ollama_alive,
            base_url=settings.OLLAMA_BASE_URL,
        ),
    )