from typing import Literal
from fastapi import APIRouter, Depends
from app.schema import QuoteResponse, KLinesResponse
from app.dependencies import get_market
from app.crud import get_intraday_quote, get_historical_candles

import requests

router = APIRouter()


@router.get("/intraday/quote", response_model=QuoteResponse)
def get_quote(
    symbol: str,
    type: Literal["oddlot", "EQUITY"] = "EQUITY",
    market=Depends(get_market),
):
    try:
        res = get_intraday_quote(market, symbol, type)
        return res
    except Exception as e:
        raise ValueError(f"Unhandled Exception: {str(e)}")


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
        return res
    except requests.exceptions.HTTPError as e:
        raise e
    except Exception as e:
        raise Exception(f"Unhandled Exception: {str(e)}")
