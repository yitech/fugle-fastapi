from fastapi import APIRouter, Depends
from app.schema.trade import CreateOrder
from app.dependencies import get_trader
from app.crud.trade import create_order


router = APIRouter()

@router.post("/create_order")
def create_order_endpoint(
    order: CreateOrder,
    trader = Depends(get_trader)
):
    res = create_order(trader, order)
    print(res)
    return res

