from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import ValidationError
from app.schema.v2 import TransactionResponse
from app.dependencies import get_trader
import logging

logger = logging.getLogger("fugle")

router = APIRouter()

@router.get("/transactions", response_model=list[TransactionResponse])
def get_transaction_endpoint(query_range: Literal["0d", "3d", "1m", "3m"]= Query("0d"),
                              trader=Depends(get_trader)):
    try:
        res = trader.get_trade_history(query_range)
        response = []
        for data in res:
            for transaction in data["mat_dats"]:
                response.append(TransactionResponse.from_rawdata(transaction))
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
