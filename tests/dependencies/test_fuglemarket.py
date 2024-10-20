import pytest
from unittest.mock import patch, MagicMock
from app.dependencies import get_market, MarketSingleton
from app.schema.v1 import QuoteResponse, KLinesResponse

@pytest.fixture(autouse=True)
def reset_singleton():
    # Reset the singleton before each test
    MarketSingleton._instance = None


@patch('app.dependencies.fuglemarket.FUGLE_MARKET_API_KEY', 'mock_api_key')  # Patch the API key
@patch('app.dependencies.fuglemarket.RestClient')
def test_singleton_behavior(mock_rest_client):
    mock_instance = MagicMock()
    mock_rest_client.return_value = mock_instance
    instance1 = get_market()
    instance2 = get_market()
    mock_rest_client.assert_called_once_with(api_key="mock_api_key")
    assert instance1 is instance2, "MarketSingleton did not return the same instance"

@patch('app.dependencies.fuglemarket.FUGLE_MARKET_API_KEY', 'mock_api_key')  # Patch the API key
@patch('app.dependencies.fuglemarket.RestClient')
def test_get_intraday_quote(mock_rest_client):
    mock_instance = MagicMock()
    mock_instance.stock = MagicMock()
    mock_instance.stock.intraday = MagicMock()
    mock_instance.stock.intraday.quote.return_value = {
        "date": "2024-09-03",
        "type": "EQUITY",
        "exchange": "TWSE",
        "market": "TSE",
        "symbol": "2330",
        "name": "\u53f0\u7a4d\u96fb",
        "referencePrice": 948,
        "previousClose": 948,
        "openPrice": 948,
        "openTime": 1725325202715144,
        "highPrice": 952,
        "highTime": 1725328645925118,
        "lowPrice": 947,
        "lowTime": 1725325217910932,
        "closePrice": 947,
        "closeTime": 1725331182490743,
        "avgPrice": 948.72,
        "change": -1,
        "changePercent": -0.11,
        "amplitude": 0.53,
        "lastPrice": 947,
        "lastSize": 47,
        "bids": [
            {"price": 946, "size": 279},
            {"price": 945, "size": 358},
            {"price": 944, "size": 182},
            {"price": 943, "size": 290},
            {"price": 942, "size": 240}
        ],
        "asks": [
            {"price": 947, "size": 226},
            {"price": 948, "size": 294},
            {"price": 949, "size": 378},
            {"price": 950, "size": 347},
            {"price": 951, "size": 726}
        ],
        "total": {
            "tradeValue": 7031881000,
            "tradeVolume": 7412,
            "tradeVolumeAtBid": 3143,
            "tradeVolumeAtAsk": 3614,
            "transaction": 1605,
            "time": 1725331182490743
        },
        "lastTrade": {
            "bid": 947,
            "ask": 948,
            "price": 947,
            "size": 47,
            "time": 1725331182490743,
            "serial": 3793375
        },
        "lastTrial": {
            "bid": 948,
            "ask": 949,
            "price": 948,
            "size": 651,
            "time": 1725325198501421,
            "serial": 94416
        },
        "isTrial": True,
        "serial": 3797531,
        "lastUpdated": 1725331190961515
    }
    mock_rest_client.return_value = mock_instance
    market = get_market()
    actual_quote = market.get_intraday_quote(symbol="2330")
    QuoteResponse(**actual_quote)
    mock_instance.stock.intraday.quote.assert_called_once_with(symbol="2330")
    


@patch('app.dependencies.fuglemarket.FUGLE_MARKET_API_KEY', 'mock_api_key')  # Patch the API key
@patch('app.dependencies.fuglemarket.RestClient')
def test_get_historical_candles(mock_rest_client):
    mock_instance = MagicMock()
    mock_instance.stock = MagicMock()
    mock_instance.stock.historical = MagicMock()
    mock_instance.stock.historical.candles.return_value = {
      "symbol": "2330",
      "type": "EQUITY",
      "exchange": "TWSE",
      "market": "TSE",
      "timeframe": "D",
      "data": [
        {
          "date": "2024-08-23",
          "open": 944,
          "high": 952,
          "low": 939,
          "close": 949,
          "volume": 31203321
        }
      ]
    }
    mock_rest_client.return_value = mock_instance
    market = get_market()
    actaul = market.get_historical_candles(symbol="2330", from_date="2024-08-23", to_date="2024-08-23")
    KLinesResponse(**mock_instance.stock.historical.candles.return_value)
    mock_rest_client.return_value.stock.historical.candles.assert_called_once_with(
            symbol="2330", **{"from": "2024-08-23", "to": "2024-08-23", "timeframe": "D"}
    )

@patch('app.dependencies.fuglemarket.FUGLE_MARKET_API_KEY', 'mock_api_key')  # Patch the API key
@patch('app.dependencies.fuglemarket.RestClient')
def test_get_historical_candles_error(mock_rest_client):
    mock_instance = MagicMock()
    mock_instance.stock = MagicMock()
    mock_instance.stock.historical = MagicMock()
    mock_instance.stock.historical.candles.return_value = {
        "statusCode": 404,
        "message": "Resource Not Found"
    }

    mock_rest_client.return_value = mock_instance

    market = get_market()
    market.get_historical_candles(symbol="2330", from_date="2024-08-23", to_date="2024-08-23")
    mock_rest_client.return_value.stock.historical.candles.assert_called_once_with(
            symbol="2330", **{"from": "2024-08-23", "to": "2024-08-23", "timeframe": "D"}
    )
