from typing import Literal
from app.dependencies.fuglemarket import MarketSingleton
from app.schema.fuglemarket import QuoteResponse

def get_intraday_quote(market: MarketSingleton, symbol: str, kind: Literal["oddlot", "EQUITY"]="EQUITY") -> QuoteResponse:
    return market.get_intraday_quote(symbol, kind)


