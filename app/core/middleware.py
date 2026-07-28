import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logger import logger


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Assigns a unique ID to every incoming request and binds it to
    loguru's context, so every log line emitted during this request
    (in routes, services, OllamaClient, etc.) automatically includes it.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        with logger.contextualize(request_id=request_id):
            start_time = time.perf_counter()

            response = await call_next(request)

            duration_ms = (time.perf_counter() - start_time) * 1000

            response.headers["X-Request-ID"] = request_id

            logger.info(
                f"{request.method} {request.url.path} "
                f"status={response.status_code} "
                f"duration={duration_ms:.1f}ms"
            )

        return response