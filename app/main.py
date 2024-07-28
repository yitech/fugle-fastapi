from fastapi import FastAPI
from app.api.endpoints import trade

app = FastAPI()

app.include_router(trade.router, prefix="/v1/trade", tags=["Trade"])

@app.get("/v1/ping", tags=["System"])
def ping():
    return {"result": "pong"}

