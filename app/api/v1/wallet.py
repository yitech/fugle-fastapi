import requests
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_trader
from app.crud import (
    get_settlements
)
from app.schema.trader import (
    SettlementResponse
)
import logging

logger = logging.getLogger("fugle")

router = APIRouter()


@router.get("/settlements", response_model=SettlementResponse)
def get_settlements_endpoint(trader=Depends(get_trader)):
    try:
        res = get_settlements(trader)
        return res
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        return HTTPException(status_code=500, detail="Error connecting to the trading service.")
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")

"""
@router.get("/balance", response_model="Balance")
def get_balance():
    return {"message": "Not implemented yet"}


@router.get("/inventories", response_model="Inventories")
def get_inventories():
    return {"message": "Not implemented yet"}
"""
