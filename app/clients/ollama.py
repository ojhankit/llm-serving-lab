from app.clients.http import HTTPClient
from app.core.logger import logger


class OllamaClient(HTTPClient):
    def __init__(self) -> None:
        super().__init__(
            base_url="http://localhost:11434",
            timeout=120.0,
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

        response = await self.post("/api/chat", json=payload)

        #logger.info(f"Request URL: {response.request.url}")
        #logger.info(f"Status: {response.status_code}")
        #logger.info(f"Response: {response.text}")

        response.raise_for_status()

        return response.json()


ollama_client = OllamaClient()