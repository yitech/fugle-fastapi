import unittest
from unittest.mock import patch, MagicMock
from fugle_marketdata import RestClient
import json

client = RestClient(api_key="ZjZjOTU1ZjctYjdlZC00OWUzLThiOGQtZjg1MDcwMThhYzBkIDU3NWNjOGQ1LWY3NGUtNDJmOS05MDdjLTRiOTViMjM1ZTIwZg==")
res = client.stock.historical.candles(symbol="2330", **{"from":"2024-08-20", "to":"2024-08-24", "timeframe":"D"})
print(json.dumps(res, indent=2))