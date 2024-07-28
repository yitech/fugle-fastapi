from fastapi import APIRouter, Depends
from app.schema import CreateOrder
from app.dependencies import get_trader
from app.crud.trade import create_order


router = APIRouter()

@router.post("/create_order", tags=["trade"])
async def create_order(
    order: CreateOrder,
    trader = Depends(get_trader)
):
    return create_order(trader, order)

