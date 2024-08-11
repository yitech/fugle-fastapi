from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.v1 import order
from app.dependencies.fugle import TraderSingleton
from app.middleware.auth import middleware
import logging.config
from pathlib import Path
import json

log_config_path = Path("logging_config.json")
if log_config_path.is_file():
    with open(log_config_path, "r") as f:
        log_config = json.load(f)  # Rename to log_config
    logging.config.dictConfig(log_config)  # Use the new name here
else:
    raise FileNotFoundError(f"Logging configuration file not found: {log_config_path}")

# Create a logger for your application
logger = logging.getLogger("fugle")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Logging the start of the application
    logger.info("Start up the application")
    TraderSingleton()
    yield
    # trader_singleton.trader.disconnect_websocket()
    logger.info("Shutting down the application")

    
app = FastAPI(lifespan=lifespan,
              middleware=middleware)

app.include_router(order.router, prefix="/api/v1", tags=["Order"])

@app.get("/api/v1/ping", tags=["System"])
def ping():
    return {"result": "pong"}





