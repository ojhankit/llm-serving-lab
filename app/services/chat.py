from app.clients.ollama import ollama_client
from app.core.logger import logger
from app.core.models import get_model
from app.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    async def chat(self, request: ChatRequest) -> ChatResponse:
        model = get_model(request.model)

        logger.info(f"Processing chat request using model: {model}")

        response = await ollama_client.chat(
            model=model,
            messages=[message.model_dump() for message in request.messages],
            stream=request.stream,
        )

        assistant_response = response["message"]["content"]

        logger.success("Chat request completed successfully")

        return ChatResponse(
            model=model,
            response=assistant_response,
        )


chat_service = ChatService()