from typing import Literal, Optional
from fastapi import APIRouter, Depends, HTTPException
from app.schema import QuoteResponse, KLinesResponse
from app.dependencies import get_market
from app.crud.marketdata import get_intraday_quote, get_historical_candles

router = APIRouter()


@router.get("/intraday/quote", response_model=QuoteResponse)
def get_quote(
    symbol: str,
    type: Literal["oddlot", "EQUITY"] = "EQUITY",
    market=Depends(get_market),
):
    try:
        res = get_intraday_quote(market, symbol, type)
    except ValueError as e:
        return HTTPException(status_code=501, detail=str(e))
    return res


@router.get("/historical/candles", response_model=KLinesResponse)
def get_candles(
    symbol: str,
    from_date: str,
    to_date: str,
    resolution: str = "D",
    market=Depends(get_market),
):
    try:
        res = get_historical_candles(market, symbol, from_date, to_date, resolution)
    except ValueError as e:
        return HTTPException(status_code=501, detail=str(e))
    return res
