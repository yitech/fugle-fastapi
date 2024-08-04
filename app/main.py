from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.v1 import order
from app.dependencies.fugle import TraderSingleton

@asynccontextmanager
async def lifespan(app: FastAPI):
    # trader_singleton = TraderSingleton()
    TraderSingleton()
    yield
    # trader_singleton.trader.disconnect_websocket()
    
app = FastAPI(lifespan=lifespan)

app.include_router(order.router, prefix="/api/v1", tags=["Order"])

@app.get("/api/v1/ping", tags=["System"])
def ping():
    return {"result": "pong"}





