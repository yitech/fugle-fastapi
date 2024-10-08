from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from app.schema import QuoteResponse, KLinesResponse
from app.dependencies import get_market
from app.crud import get_intraday_quote, get_historical_candles
import requests
import logging

logger = logging.getLogger("fugle")

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
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTPError: {http_err}")
        raise HTTPException(status_code=400, detail=f"HTTP Error: {str(http_err)}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        raise HTTPException(
            status_code=500, detail="Error connecting to the market data source."
        )
    except ValueError as val_err:
        logger.error(f"ValueError: {val_err}")
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(val_err)}")
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


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
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTPError: {http_err}")
        raise HTTPException(status_code=400, detail=f"HTTP Error: {str(http_err)}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        raise HTTPException(
            status_code=500, detail="Error connecting to the market data source."
        )
    except ValueError as val_err:
        logger.error(f"ValueError: {val_err}")
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(val_err)}")
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
