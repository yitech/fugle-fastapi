import pytest
from unittest.mock import patch, MagicMock
from app.dependencies import get_trader, TraderSingleton
from app.models.fugle import (
    Settlement
)
import requests



@pytest.fixture
def mock_trader_methods():
    with patch.object(TraderSingleton, '_initialize', MagicMock()) as mock_init, \
         patch.object(TraderSingleton, '_start_scheduler', MagicMock()) as mock_scheduler:
        yield mock_init, mock_scheduler

def test_trader_singleton(mock_trader_methods):
    mock_init, mock_scheduler = mock_trader_methods

    # Create two instances of Trader
    trader1 = TraderSingleton()
    trader2 = TraderSingleton()

    mock_init.assert_called_once()
    mock_scheduler.assert_called_once()
    assert trader1 is trader2


@patch.object(TraderSingleton, 'trader', create=True)  # Mock TraderSingleton.trader
def test_get_settlements(mock_trader, mock_trader_methods):
    # Mock the return value of self.trader.get_settlements()
    mock_data = [
        {
            "c_date": "20220310",
            "date": "20220308",
            "price": "-80912"
        },
        {
            "c_date": "20220311",
            "date": "20220309",
            "price": "4826"
        }
    ]

    mock_trader.get_settlements = MagicMock(return_value=mock_data)

    # Create the TraderSingleton instance
    trader = TraderSingleton()

    # Call the get_settlements method
    result = trader.get_settlements()

    # Verify that the mock get_settlements was called
    mock_trader.get_settlements.assert_called_once()

    # Verify the result is an instance of SettlementResult
    assert len(result) == 2

    # Check if the values in SettlementResult are correct
    assert result[0] == Settlement(c_date="20220310", date="20220308", price="-80912")
    assert result[1] == Settlement(c_date="20220311", date="20220309", price="4826")