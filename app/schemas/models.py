from pydantic import BaseModel

class ModelInfo(BaseModel):
    alias: str
    model_name: str
    pulled: bool

class ModelsResponse(BaseModel):
    models: list[ModelInfo]