import requests
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_trader
from app.schema.v1 import SettlementResponse, BalanceResponse, InventoryResponse
from pydantic import TypeAdapter
import logging

logger = logging.getLogger("fugle")

router = APIRouter()


@router.get("/settlements", response_model=list[SettlementResponse])
def get_settlements_endpoint(trader=Depends(get_trader)):
    try:
        res = trader.get_settlements()
        response = [SettlementResponse(**s) for s in res]
        return response
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        return HTTPException(
            status_code=500, detail="Error connecting to the trading service."
        )
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/balance", response_model=BalanceResponse)
def get_balance_endpoint(trader=Depends(get_trader)):
    try:
        res = trader.get_balance()
        response = BalanceResponse(**res)
        return response
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        return HTTPException(
            status_code=500, detail="Error connecting to the trading service."
        )
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/inventories", response_model=list[InventoryResponse])
def get_inventories_endpoint(trader=Depends(get_trader)):
    try:
        res = trader.get_inventories()
        logger.info(f"Inventories: {res}")
        adapter = TypeAdapter(list[InventoryResponse])
        return adapter.validate_python(res)
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        return HTTPException(
            status_code=500, detail="Error connecting to the trading service."
        )
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")
