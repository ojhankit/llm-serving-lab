import httpx

from app.clients.http import HTTPClient
from app.core.logger import logger
from app.core.config import settings
from app.core.exceptions import (
    OllamaConnectionError,
    OllamaTimeoutError,
    OllamaResponseError,
)


class OllamaClient(HTTPClient):
    def __init__(self) -> None:
        super().__init__(
            base_url=settings.OLLAMA_BASE_URL,
            timeout=settings.OLLAMA_TIMEOUT,
        )

    async def chat(
        self,
        model: str,
        messages: list[dict],
        stream: bool = False,
    ) -> dict:
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
        }

        logger.debug(f"Ollama chat request -> model={model}, messages={len(messages)}")

        try:
            response = await self.post("/api/chat", json=payload)
            response.raise_for_status()

        except httpx.ConnectError as e:
            logger.error(f"Ollama connection failed: {e}")
            raise OllamaConnectionError(
                "Could not connect to Ollama server"
            ) from e

        except httpx.TimeoutException as e:
            logger.error(f"Ollama request timed out: {e}")
            raise OllamaTimeoutError(
                "Ollama request timed out"
            ) from e

        except httpx.HTTPStatusError as e:
            detail = self._extract_error_detail(e.response)
            logger.error(f"Ollama returned {e.response.status_code}: {detail}")
            raise OllamaResponseError(
                status_code=e.response.status_code,
                detail=detail,
            ) from e

        logger.debug(f"Ollama chat response received: status={response.status_code}")

        return response.json()

    @staticmethod
    def _extract_error_detail(response: httpx.Response) -> str:
        """Ollama typically returns {"error": "..."} on failure."""
        try:
            body = response.json()
            return body.get("error", response.text)
        except ValueError:
            return response.text


ollama_client = OllamaClient()