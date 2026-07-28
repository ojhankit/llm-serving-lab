from typing import Literal
from pydantic import BaseModel, Field

class Message(BaseModel):
    role : Literal["system", "user", "assistant"]
    content : str = Field(..., min_length=1)

class ChatRequest(BaseModel):
    model : str = Field(..., description="Model alias to use")
    messages : list[Message] = Field(
        ...,
        min_length=1,
        description="conversation history"
    )
    stream : bool = False

class ChatResponse(BaseModel):
    model : str
    response : str