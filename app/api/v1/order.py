from fastapi import APIRouter, Depends, HTTPException
from app.schema.order import CreateOrder, OrderResponse
from app.dependencies import get_trader
from app.crud.order import create_order


router = APIRouter()

@router.post("/order", response_model=OrderResponse)
def create_order_endpoint(
    order: CreateOrder,
    trader = Depends(get_trader)
):
    try:
        res = create_order(trader, order)
    except ValueError as e:
        return HTTPException(status_code=501, detail=str(e))
    return res

@router.delete("/order/{:id}")
def delete_order_endpoint():
    pass

