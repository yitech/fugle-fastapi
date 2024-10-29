from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from app.schema.v1 import (
    CreateOrder,
    OrderResponse,
    OrderResultResponse,
    CancelResponse,
    MarketStatusResponse,
    TransactionResponse
)
from pydantic import TypeAdapter
from app.dependencies import get_trader
import logging

logger = logging.getLogger("fugle")

router = APIRouter()


@router.post("/order", response_model=OrderResponse)
def create_order_endpoint(order: CreateOrder, trader=Depends(get_trader)):
    try:
        res = trader.create_order(order)
        response = OrderResponse(**res)
        return response
    except ValidationError as e:
        logger.error(f"ValidationError: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        raise HTTPException(status_code=400, detail=f"Missing key: {e}")
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/orders", response_model=list[OrderResultResponse])
def get_orders_endpoint(trader=Depends(get_trader)):
    try:
        res = trader.get_order_results()
        response = [OrderResultResponse(**item) for item in res]
        return response
    except ValidationError as e:
        logger.error(f"ValidationError: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        raise HTTPException(status_code=400, detail=f"Missing key: {e}")
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/order/{ord_no}", response_model=CancelResponse)
def delete_order_endpoint(ord_no: str, trader=Depends(get_trader)):
    try:
        res = trader.cancel_order(ord_no)
        response = CancelResponse(**res)
        return response
    except ValidationError as e:
        logger.error(f"ValidationError: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        raise HTTPException(status_code=400, detail=f"Missing key: {e}")
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/market_status", response_model=MarketStatusResponse)
def get_market_status_endpoint(trader=Depends(get_trader)):
    try:
        res = trader.get_market_status()
        response = MarketStatusResponse(**res)
        return response
    except ValidationError as e:
        logger.error(f"ValidationError: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        raise HTTPException(status_code=400, detail=f"Missing key: {e}")
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/transactions", response_model=list[TransactionResponse])
def get_transaction_endpoint(query_range: Literal["0d", "3d", "1m", "3m"], trader=Depends(get_trader)):
    try:
        res = trader.get_trade_history(query_range)
        adapter = TypeAdapter(list[TransactionResponse])
        return adapter.validate_python(res)
    except ValidationError as e:
        logger.error(f"ValidationError: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        raise HTTPException(status_code=400, detail=f"Missing key: {e}")
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

