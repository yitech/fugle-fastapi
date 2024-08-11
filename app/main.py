from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.v1 import order
from app.dependencies.fugle import TraderSingleton
from app.middleware.auth import middleware
import logging
import sys

# Define your custom logging configuration
# Define the logging configuration
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s"
        },
        "json": {
            "format": "{\"level\": \"%(levelname)s\", \"time\": \"%(asctime)s\", \"filename\": \"%(filename)s\", \"lineno\": \"%(lineno)d\", \"message\": \"%(message)s\"}"
        }
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
            "formatter": "default"
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "json",
            "filename": "log/fugle-fastapi.log",  # Base file name
            "when": "midnight",  # Rotate at midnight
            "backupCount": 10,  # Keep 10 days of logs
            "encoding": "utf-8",
            "delay": False,
            "utc": False,
        },
    },
    "loggers": {
        "fugle": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.error": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.access": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}

logging.config.dictConfig(logging_config)

# Create a logger for your application
logger = logging.getLogger("fugle")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Logging the start of the application
    logger.info("This is an info message.")
    TraderSingleton()
    yield
    # trader_singleton.trader.disconnect_websocket()

    
app = FastAPI(lifespan=lifespan,
              middleware=middleware)

app.include_router(order.router, prefix="/api/v1", tags=["Order"])

@app.get("/api/v1/ping", tags=["System"])
def ping():
    return {"result": "pong"}





