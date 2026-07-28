from pathlib import Path
from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

# Default extra so {extra[request_id]} doesn't KeyError outside request context
logger.configure(extra={"request_id": "-"})

# Console Logger
logger.add(
    sink=lambda message: print(message, end=''),
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss} </green>| "
        "<cyan>{file.name}</cyan>:<cyan>{line} </cyan>| "
        "<level>{level: <8} </level>| "
        "<magenta>{extra[request_id]}</magenta> | "
        "<level>{message}</level> | "
    )
)

logger.add(
    LOG_DIR / "{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="14 days",
    compression="zip",
    encoding="utf-8",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{file.name}:{line} | "
        "{level:<8} | "
        "{extra[request_id]} | "
        "{message}"
    ),
)

__all__ = ["logger"]