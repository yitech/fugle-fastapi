from fastapi import APIRouter, Depends, HTTPException
from app.schema.order import (
    CreateOrder, OrderResponse, OrderResult, CancelResponse, MarketStatusResponse
)
from app.dependencies import get_trader
from app.crud import (
    create_order, get_order_results, cancel_order, get_market_status
)
import logging
import requests

logger = logging.getLogger("fugle")

router = APIRouter()


@router.post("/order", response_model=OrderResponse)
def create_order_endpoint(order: CreateOrder, trader=Depends(get_trader)):
    try:
        res = create_order(trader, order)
        return res
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        return HTTPException(status_code=422, detail=f"Invalid input: {str(e)}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        return HTTPException(status_code=500, detail="Error connecting to the trading service.")
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/orders", response_model=list[OrderResult])
def get_orders_endpoint(trader=Depends(get_trader)):
    try:
        res = get_order_results(trader)
        return res
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTPError: {e}")
        return HTTPException(status_code=404, detail="Orders not found")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        return HTTPException(status_code=500, detail="Error connecting to the trading service.")
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/order/{ord_no}", response_model=CancelResponse)
def delete_order_endpoint(ord_no: str, trader=Depends(get_trader)):
    try:
        res = cancel_order(trader, ord_no)
        return res
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTPError: {e}")
        return HTTPException(status_code=404, detail="Order not found")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        return HTTPException(status_code=500, detail="Error connecting to the trading service.")
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/market_status", response_model=MarketStatusResponse)
def get_market_status_endpoint(trader=Depends(get_trader)):
    try:
        res = get_market_status(trader)
        return res
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")