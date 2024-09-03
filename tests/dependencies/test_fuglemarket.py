import pytest
from unittest.mock import patch
from app.dependencies import get_market
from app.models.fuglemarket import KLines, Quote
import requests

@pytest.fixture
def mock_rest_client():
    with patch('fugle_marketdata.RestClient') as MockRestClient:
        mock_client_instance = MockRestClient.return_value
        yield mock_client_instance

def test_singleton_behavior():
    instance1 = get_market()
    instance2 = get_market()
    assert instance1 is instance2, "MarketSingleton did not return the same instance"


def test_get_historical_candles(mock_rest_client):
    # Mock an error response
    mock_response = {
        "statusCode": 404,
        "message": "Resource Not Found"
    }
    mock_rest_client.stock.historical.candles.return_value = mock_response

    market = get_market()
    
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        market.get_historical_candles(symbol="2330", from_date="2024-08-24", to_date="2024-08-24")
    assert "Resource Not Found" in str(exc_info.value)


def test_get_historical_candles_error(mock_rest_client):
    # Mock an error response
    mock_response = {
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
    mock_rest_client.stock.historical.candles.return_value = mock_response

    market = get_market()
    
    actaul = market.get_historical_candles(symbol="2330", from_date="2024-08-23", to_date="2024-08-23")
    expected = KLines(**mock_response)
    assert actaul == expected
