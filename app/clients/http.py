from httpx import AsyncClient, Response


class HTTPClient:
    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        self._client = AsyncClient(
            base_url=base_url,
            timeout=timeout,
        )

    async def get(self, url: str, **kwargs) -> Response:
        return await self._client.get(url, **kwargs)

    async def post(self, url: str, **kwargs) -> Response:
        return await self._client.post(url, **kwargs)

    async def close(self) -> None:
        await self._client.aclose()