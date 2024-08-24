from fastapi import APIRouter, Depends, HTTPException
from app.schema.order import CreateOrder, OrderResponse, OrderResult, CancelResponse
from app.dependencies import get_trader
from app.crud.order import create_order, get_order_results, cancel_order


router = APIRouter()


@router.post("/order", response_model=OrderResponse)
def create_order_endpoint(order: CreateOrder, trader=Depends(get_trader)):
    try:
        res = create_order(trader, order)
    except ValueError as e:
        return HTTPException(status_code=501, detail=str(e))
    return res


@router.get("/orders", response_model=list[OrderResult])
def get_orders_endpoint(trader=Depends(get_trader)):
    try:
        res = get_order_results(trader)
    except ValueError as e:
        return HTTPException(status_code=501, detail=str(e))
    return res


@router.delete("/order/{ord_no}", response_model=CancelResponse)
def delete_order_endpoint(ord_no: str, trader=Depends(get_trader)):
    try:
        res = cancel_order(trader, ord_no)
    except ValueError as e:
        return HTTPException(status_code=501, detail=str(e))
    return res
