from typing import Literal
from app.models.fuglemarket import Quote
from app.core.config import settings
from fugle_marketdata import RestClient
import logging

FUGLE_MARKET_API_KEY = settings.fugle_market_api_key

logger = logging.getLogger("fugle")

class MarketSingleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MarketSingleton, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.client = RestClient(api_key=FUGLE_MARKET_API_KEY)
        logger.info("Fugle Market initialized")

    def get_client(self):
        return self.client

    def get_intraday_quote(self, symbol: str, kind: Literal["oddlot", "EQUITY"]="EQUITY") -> Quote:
        stock = self.client.stock
        if kind == "EQUITY":
            res = stock.intraday.quote(symbol=symbol)
        else: # kind == "oddlot":
            res = stock.intraday.quote(symbol=symbol, type=kind)
        if res.get("statusCode", 200) != 200:
            raise Exception(f"Error: {res.get('message')}")
        quote = Quote(**res)
        return quote
    


def get_market():
    return MarketSingleton()