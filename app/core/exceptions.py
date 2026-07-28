# core/exceptions.py
class LLMServiceError(Exception):
    """Base exception for all LLM service errors."""
    def __init__(self, message: str, detail: str | None = None):
        self.message = message
        self.detail = detail
        super().__init__(message)


class OllamaConnectionError(LLMServiceError):
    """Raised when we can't reach the Ollama server at all."""
    pass


class OllamaTimeoutError(LLMServiceError):
    """Raised when Ollama takes too long to respond."""
    pass


class ModelNotFoundError(LLMServiceError):
    """Raised when requested model isn't pulled/available in Ollama."""
    def __init__(self, model_name: str):
        self.model_name = model_name
        super().__init__(f"Model '{model_name}' not found or not loaded")


class OllamaResponseError(LLMServiceError):
    """Raised when Ollama returns a non-2xx or malformed response."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        super().__init__(f"Ollama returned error: {status_code}", detail)


class InvalidRequestError(LLMServiceError):
    """Raised for bad input from the client (e.g. empty prompt)."""
    pass