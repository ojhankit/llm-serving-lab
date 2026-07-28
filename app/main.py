from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.clients.ollama import ollama_client
from app.core.logger import logger
from app.core.handlers import register_exception_handlers
from app.routes import health, model


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting LLM Serving API")

    yield

    logger.info("Shutting down LLM Serving API")
    await ollama_client.close()


app = FastAPI(
    title="LLM Serving API",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(chat_router)
app.include_router(health.router)
app.include_router(model.router)

@app.get("/", tags=["root"])
async def root() -> dict:
    return {
        "message": "Backend working"
    }