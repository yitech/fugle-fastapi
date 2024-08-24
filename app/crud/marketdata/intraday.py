from typing import Literal
from app.dependencies.fuglemarket import MarketSingleton
from app.schema.intraday import Quote

def get_stock_quote(market: MarketSingleton, symbol: str, kind: Literal["oddlot", "EQUITY"]="EQUITY") -> Quote:
    res = market.get_stock_quote(symbol, kind)
    return res

