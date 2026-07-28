"""
central registry fr all supported models
"""

MODEL_MAP : dict[str, str] = {
    "qwen" : "qwen:0.5b",
    #"llama" : "llama3.2:1b",
}

def get_model(model_alias: str) -> str:
    """
    return true model name
    """
    try:
        return MODEL_MAP[model_alias]
    except KeyError:
        raise ValueError(f"Unsupported model: {model_alias}") 

def list_models() -> list[str]:
    """
    Return the list of supported model aliases.
    """
    return list(MODEL_MAP.keys())