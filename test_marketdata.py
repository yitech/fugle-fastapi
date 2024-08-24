import unittest
from unittest.mock import patch, MagicMock
from fugle_marketdata import RestClient
import json

class TestFugleMarketData(unittest.TestCase):

    @patch('fugle_marketdata.RestClient')
    def test_intraday_quote(self, MockRestClient):
        # Expected output
        expected_data = {
            "date": "2024-08-20",
            "type": "EQUITY",
            "exchange": "TWSE",
            "market": "TSE",
            "symbol": "2337",
            "name": "\u65fa\u5b8f",
            "referencePrice": 27.55,
            "previousClose": 27.55,
            "openPrice": 27.7,
            "openTime": 1724115617825615,
            "highPrice": 28,
            "highTime": 1724121626080518,
            "lowPrice": 27.7,
            "lowTime": 1724115617825615,
            "closePrice": 27.9,
            "closeTime": 1724131800000000,
            "avgPrice": 27.9,
            "change": 0.35,
            "changePercent": 1.27,
            "amplitude": 1.09,
            "lastPrice": 27.9,
            "lastSize": 551,
            "bids": [
                {"price": 27.9, "size": 135},
                {"price": 27.85, "size": 157},
                {"price": 27.8, "size": 260},
                {"price": 27.75, "size": 307},
                {"price": 27.7, "size": 580}
            ],
            "asks": [
                {"price": 27.95, "size": 137},
                {"price": 28, "size": 660},
                {"price": 28.05, "size": 236},
                {"price": 28.1, "size": 189},
                {"price": 28.15, "size": 170}
            ],
            "total": {
                "tradeValue": 224122950,
                "tradeVolume": 8033,
                "tradeVolumeAtBid": 3686,
                "tradeVolumeAtAsk": 4265,
                "transaction": 1690,
                "time": 1724131800000000
            },
            "lastTrade": {
                "bid": 27.9,
                "ask": 27.95,
                "price": 27.9,
                "size": 551,
                "time": 1724131800000000,
                "serial": 7861006
            },
            "lastTrial": {
                "bid": 27.9,
                "ask": 27.95,
                "price": 27.9,
                "size": 549,
                "time": 1724131798800678,
                "serial": 7860195
            },
            "isClose": True,
            "serial": 7861006,
            "lastUpdated": 1724131800000000
        }

        # Mock the client instance and the method
        mock_client = MockRestClient.return_value
        mock_stock = MagicMock()
        mock_stock.intraday.quote.return_value = expected_data
        mock_client.stock = mock_stock

        client = RestClient(api_key="ZjZjOTU1ZjctYjdlZC00OWUzLThiOGQtZjg1MDcwMThhYzBkIDU3NWNjOGQ1LWY3NGUtNDJmOS05MDdjLTRiOTViMjM1ZTIwZg==")
        data = client.stock.intraday.quote(symbol="2337")

        # Check if the output matches the expected data
        self.assertEqual(data, expected_data)
        print(json.dumps(data, indent=4))

if __name__ == '__main__':
    unittest.main()
