from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import chat_service
from app.core.config import settings
from app.core.rate_limiter import RateLimiter


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    _ = Depends(RateLimiter(requests=settings.DEFAULT_CHAT_LIMIT, window_seconds=settings.DEFAULT_CHAT_WINDOW))
) -> ChatResponse:
    return await chat_service.chat(request)