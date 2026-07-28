from fastapi import APIRouter

from app.clients.ollama import ollama_client
from app.core.models import list_models, MODEL_MAP
from app.schemas.models import ModelsResponse, ModelInfo

router = APIRouter(tags=["models"])


@router.get("/models", response_model=ModelsResponse)
async def get_models() -> ModelsResponse:
    pulled_models = await ollama_client.list_pulled_models()

    models = [
        ModelInfo(
            alias=alias,
            model_name=model_name,
            pulled=model_name in pulled_models,
        )
        for alias, model_name in MODEL_MAP.items()
    ]

    return ModelsResponse(models=models)