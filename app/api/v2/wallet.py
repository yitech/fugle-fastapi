import requests
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_trader
from app.schema.v2 import BalanceResponse, InventoryResponse
import logging

logger = logging.getLogger("fugle")

router = APIRouter()


@router.get("/balance", response_model=BalanceResponse)
def get_balance_endpoint(trader=Depends(get_trader)):
    try:
        total_balance = trader.get_balance()["available_balance"]
        settlements = trader.get_settlements()
        for settlement in settlements:
            total_balance += int(settlement["price"])
        orders = trader.get_order_results() # expect get open orders
        locked_balance = 0
        for order in orders:
            r_qty_share = order["org_qty_share"] - order["cel_qty_share"] - order["mat_qty_share"]
            locked_balance += r_qty_share * order["od_price"]
        return BalanceResponse(
                    available=total_balance-locked_balance, 
                    locked=locked_balance
                    )
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
        inventories = trader.get_inventories()
        logger.info(f"Inventories: {inventories}")
        response = []
        for inventory in inventories:
            response.append(InventoryResponse(
                symbol=inventory["stk_no"], 
                qty_share=int(inventory["cost_qty"]))
                )
        return response
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        return HTTPException(
            status_code=500, detail="Error connecting to the trading service."
        )
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")

