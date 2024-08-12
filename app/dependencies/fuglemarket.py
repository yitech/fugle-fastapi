from app.models.fuglemarket import Quote
from app.core.config import settings
from fugle_marketdata import RestClient
import logging

API_KEY = settings.FUGLE_API_KEY

logger = logging.getLogger("fugle")

class FugleMarket:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FugleMarket, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.client = RestClient(API_KEY)
        logger.info("Fugle Market initialized")

    def get_client(self):
        return self.client

    def get_stock_quote(self, symbol: str, kind: "oddlot" | "EQUITY" = "EQUITY") -> Quote:
        stock = self.client.stock
        res = stock.intraday.quote(symbol, kind)
        return Quote(**res)


    