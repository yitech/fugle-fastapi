import requests
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_trader
from app.crud import (
    get_settlements,
    get_balance,
    get_inventories
)
from app.schema.trader import (
    SettlementResponse,
    BalanceResponse,
    InventoryResponse
)
import logging

logger = logging.getLogger("fugle")

router = APIRouter()


@router.get("/settlements", response_model=list[SettlementResponse])
def get_settlements_endpoint(trader=Depends(get_trader)):
    try:
        res = get_settlements(trader)
        return res
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        return HTTPException(
            status_code=500, detail="Error connecting to the trading service."
        )
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")



@router.get("/balance", response_model=BalanceResponse)
def get_balance(trader=Depends(get_trader)):
    try:
        res = get_balance(trader)
        return res
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        return HTTPException(
            status_code=500, detail="Error connecting to the trading service."
        )
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/inventories", response_model=InventoryResponse)
def get_inventories(trader=Depends(get_trader)):
    try:
        res = get_inventories(trader)
        return res
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        return HTTPException(
            status_code=500, detail="Error connecting to the trading service."
        )
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")
    

