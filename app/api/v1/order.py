from fastapi import APIRouter, Depends, HTTPException
from app.schema.order import CreateOrder, OrderResponse, CancelOrder
from app.dependencies import get_trader
from app.crud.order import create_order, get_order_results


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

@router.get("/orders")
def get_orders_endpoint(
    trader = Depends(get_trader)
):
    try:
        res = get_order_results(trader)
    except ValueError as e:
        return HTTPException(status_code=501, detail=str(e))
    return res

@router.delete("/order")
def delete_order_endpoint(
    order: CancelOrder,
    trader = Depends(get_trader)
):
    try:
        res = trader.cancel_order(order.ap_code, order.ord_no, order.stock_no)
    except ValueError as e:
        return HTTPException(status_code=501, detail=str(e))
    return res

