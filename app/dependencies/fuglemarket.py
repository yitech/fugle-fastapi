from typing import Literal
from app.models.fuglemarket import Quote, KLines
from app.core.config import settings
from fugle_marketdata import RestClient
import logging

import requests

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

    def get_intraday_quote(
        self, symbol: str, kind: Literal["oddlot", "EQUITY"] = "EQUITY"
    ) -> Quote:
        stock = self.client.stock
        if kind == "EQUITY":
            res = stock.intraday.quote(symbol=symbol)
        else:  # kind == "oddlot":
            res = stock.intraday.quote(symbol=symbol, type=kind)
        if res.get("statusCode", 200) != 200:
            raise Exception(f"Error: {res.get('message')}")
        logger.info(f"{res=}")
        quote = Quote(**res)
        return quote

    def get_historical_candles(
        self, symbol: str, from_date: str, to_date: str, resolution: str = "D"
    ) -> KLines:
        """
        Get historical candles for a stock.
        Parameters:
        symbol (str): Stock symbol, e.g., "2330".
        from_date (str): Start date, e.g., "2021-01-01".
        to_date (str): End date, e.g., "2021-01-31".
        resolution (str): Resolution of the data. It can be one of the following:
            - "1", "3", "5", "10", "15", "30", "60" for minute intervals.
            - "D" for daily.
            - "W" for weekly.
            - "M" for monthly.
        Returns:
        KLines: An object containing the historical candle data.
        """
        stock = self.client.stock
        res = stock.historical.candles(
            symbol=symbol, **{"from": from_date, "to": to_date, "timeframe": resolution}
        )
        if res.get("statusCode", 200) == 200:
            klines = KLines(**res)
            return klines
        elif res.get("statusCode", 200) == 404:
            raise requests.exceptions.HTTPError(f"Error: {res.get('message')}")
        else:
            raise Exception(f"Error: {res.get('message')}")


def get_market():
    return MarketSingleton()
