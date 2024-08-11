from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.v1 import order
from app.dependencies.fugle import TraderSingleton
from app.middleware.auth import middleware
import logging
import sys

# Define your custom logging configuration
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s",
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "default",
        },
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,  # Prevent log message propagation to other loggers
        },
        "uvicorn": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,  # Prevent duplicate logs from uvicorn
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False,  # Prevent duplicate logs from uvicorn.error
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,  # Prevent duplicate logs from uvicorn.access
        },
    },
}

logging.config.dictConfig(logging_config)

# Create a logger for your application
logger = logging.getLogger(__name__)

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





