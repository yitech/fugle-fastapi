from typing import Literal, Optional
from fastapi import APIRouter, Depends, HTTPException
from app.schema.fuglemarket import QuoteResponse
from app.dependencies import get_market
from app.crud.marketdata import get_intraday_quote

router = APIRouter()

@router.get("/intraday/quote", response_model=QuoteResponse)
def get_quote(symbol: str, type: Optional[Literal["oddlot", "EQUITY"]]="EQUITY", market=Depends(get_market)):
    try:
        res = get_intraday_quote(market, symbol, type)
    except ValueError as e:
        return HTTPException(status_code=501, detail=str(e))
    return res

