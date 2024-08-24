from typing import Literal
from app.dependencies.fuglemarket import MarketSingleton
from app.schema.intraday import Quote

def get_intraday_quote(market: MarketSingleton, symbol: str, kind: Literal["oddlot", "EQUITY"]="EQUITY") -> Quote:
    return market.get_intraday_quote(symbol, kind)


