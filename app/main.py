from fastapi import FastAPI
from app.api.v1 import trade

app = FastAPI()

app.include_router(trade.router, prefix="/api/v1/trade", tags=["Trade"])

@app.get("/api/v1/ping", tags=["System"])
def ping():
    return {"result": "pong"}

