"""
central registry for all supported models
"""

from app.core.exceptions import ModelNotFoundError

MODEL_MAP: dict[str, str] = {
    "qwen": "qwen:0.5b",
    # "llama": "llama3.2:1b",
}


def get_model(model_alias: str) -> str:
    """
    Return true model name for a given alias.

    Raises:
        ModelNotFoundError: if the alias isn't in MODEL_MAP.
    """
    try:
        return MODEL_MAP[model_alias]
    except KeyError:
        raise ModelNotFoundError(model_alias) from None


def list_models() -> list[str]:
    """
    Return the list of supported model aliases.
    """
    return list(MODEL_MAP.keys())