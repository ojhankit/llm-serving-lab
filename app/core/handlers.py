from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    LLMServiceError, OllamaConnectionError, OllamaTimeoutError,
    ModelNotFoundError, OllamaResponseError, InvalidRequestError
)
import logging

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(OllamaConnectionError)
    async def ollama_connection_handler(request: Request, exc: OllamaConnectionError):
        logger.error(f"Ollama connection failed: {exc.message}")
        return JSONResponse(
            status_code=503,
            content={"error": "service_unavailable", "message": "Cannot reach Ollama server"}
        )

    @app.exception_handler(OllamaTimeoutError)
    async def ollama_timeout_handler(request: Request, exc: OllamaTimeoutError):
        return JSONResponse(
            status_code=504,
            content={"error": "gateway_timeout", "message": exc.message}
        )

    @app.exception_handler(ModelNotFoundError)
    async def model_not_found_handler(request: Request, exc: ModelNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"error": "model_not_found", "message": exc.message}
        )

    @app.exception_handler(InvalidRequestError)
    async def invalid_request_handler(request: Request, exc: InvalidRequestError):
        return JSONResponse(
            status_code=400,
            content={"error": "bad_request", "message": exc.message}
        )

    @app.exception_handler(OllamaResponseError)
    async def ollama_response_handler(request: Request, exc: OllamaResponseError):
        return JSONResponse(
            status_code=502,
            content={"error": "upstream_error", "message": exc.message, "detail": exc.detail}
        )

    # Catch-all for anything else deriving from our base
    @app.exception_handler(LLMServiceError)
    async def generic_llm_handler(request: Request, exc: LLMServiceError):
        logger.exception("Unhandled LLM service error")
        return JSONResponse(
            status_code=500,
            content={"error": "internal_error", "message": exc.message}
        )