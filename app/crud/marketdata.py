from typing import Literal
from app.dependencies.fuglemarket import MarketSingleton
from app.schema import QuoteResponse, KLinesResponse


def get_intraday_quote(
    market: MarketSingleton, symbol: str, kind: Literal["oddlot", "EQUITY"] = "EQUITY"
) -> QuoteResponse:
    return market.get_intraday_quote(symbol, kind)


def get_historical_candles(
    market: MarketSingleton,
    symbol: str,
    from_date: str,
    to_date: str,
    resolution: str = "D",
) -> KLinesResponse:
    try:
        return market.get_historical_candles(symbol, from_date, to_date, resolution)
    except Exception as e:
        raise ValueError(str(e))
