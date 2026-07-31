from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
)
import logging

from app.core.exceptions import (
    OllamaConnectionError,
    OllamaTimeoutError,
    OllamaResponseError,
)
from app.core.logger import logger


def _is_retryable(exc: BaseException) -> bool:
    """Connection errors and timeouts are always retryable.
    Response errors are only retryable if the status is 5xx
    (server-side/upstream issue) — never retry 4xx (client's fault,
    e.g. model not found, bad request)."""
    if isinstance(exc, (OllamaConnectionError, OllamaTimeoutError)):
        return True
    if isinstance(exc, OllamaResponseError):
        return exc.status_code >= 500
    return False


# Reusable decorator: 3 attempts total, exponential backoff (1s, 2s, 4s capped)
ollama_retry = retry(
    retry=retry_if_exception(_is_retryable),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,  # after exhausting retries, raise the real exception (not tenacity's)
)