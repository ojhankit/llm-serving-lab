import httpx
from httpx import AsyncClient, Response


class HTTPClient:
    def __init__(
        self,
        base_url: str,
        connect_timeout: float = 5.0,
        read_timeout: float = 30.0,
    ) -> None:
        timeout = httpx.Timeout(
            connect=connect_timeout,  # time to establish connection
            read=read_timeout,        # time waiting for a response
            write=10.0,               # time to send the request body
            pool=5.0,                 # time waiting for a free connection
        )
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