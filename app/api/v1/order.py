from fastapi import APIRouter, Depends
from app.schema.order import CreateOrder
from app.dependencies import get_trader
from app.crud.order import create_order


router = APIRouter()

@router.post("/order", response_model=dict)
def create_order_endpoint(
    order: CreateOrder,
    trader = Depends(get_trader)
):
    res = create_order(trader, order)
    return res

@router.delete("/order/{:id}")
def delete_order_endpoint():
    pass

