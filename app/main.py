from fastapi import FastAPI
from app.api.v1 import order

app = FastAPI()

app.include_router(order.router, prefix="/api/v1", tags=["Order"])

@app.get("/api/v1/ping", tags=["System"])
def ping():
    return {"result": "pong"}

