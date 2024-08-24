from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.v1 import marketdata, order
from app.dependencies.fugle import TraderSingleton
from app.dependencies.fuglemarket import MarketSingleton
from app.middleware.auth import middleware
import logging.config
from pathlib import Path
import json
import sys

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

log_config_path = Path("logging_config.json")
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)  # Ensure the logs directory exists
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
    MarketSingleton()
    yield
    # trader_singleton.trader.disconnect_websocket()
    logger.info("Shutting down the application")


app = FastAPI(lifespan=lifespan, middleware=middleware)

app.include_router(order.router, prefix="/api/v1", tags=["Order"])
app.include_router(marketdata.router, prefix="/api/v1", tags=["Market"])


@app.get("/api/v1/ping", tags=["System"])
def ping():
    return {"result": "pong"}
