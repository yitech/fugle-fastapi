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


@patch.object(TraderSingleton, 'trader', create=True)  # Mock TraderSingleton.trader
def test_get_inventories(mock_trader, mock_trader_methods):
    # Mock data for get_inventories response
    mock_data = [
        {
            "ap_code": "",
            "cost_qty": "70",
            "cost_sum": "-62949",
            "make_a_per": "8.16",
            "make_a_sum": "5139",
            "price_avg": "898.00",
            "price_evn": "903.27",
            "price_mkt": "977.00",
            "price_now": "977.00",
            "price_qty_sum": "62860",
            "qty_b": "0",
            "qty_bm": "0",
            "qty_c": "0",
            "qty_l": "70",
            "qty_s": "0",
            "qty_sm": "0",
            "rec_va_sum": "68088",
            "stk_na": "\u53f0\u7a4d\u96fb",
            "stk_no": "2330",
            "s_type": "H",
            "trade": "0",
            "value_mkt": "68390",
            "value_now": "68390",
            "stk_dats": [
                {
                    "buy_sell": "B",
                    "cost_r": "0",
                    "fee": "89",
                    "make_a": "5139",
                    "make_a_per": "8.16",
                    "ord_no": "B5978032272160",
                    "pay_n": "-62949",
                    "price": "898.00",
                    "price_evn": "903.27",
                    "qty": "70",
                    "qty_c": "0",
                    "qty_h": "0",
                    "qty_r": "0",
                    "t_date": "20240904",
                    "tax": "0",
                    "tax_g": "0",
                    "trade": "0",
                    "t_time": "",
                    "value_mkt": "68390",
                    "value_now": "68390",
                    "user_def": ""
                }
            ]
        }
    ]

    # Mock the return value of self.trader.get_inventories()
    mock_trader.get_inventories = MagicMock(return_value=mock_data)

    # Create the TraderSingleton instance
    trader = TraderSingleton()

    # Call the get_inventories method
    result = trader.get_inventories()

    # Verify that the mock get_inventories was called
    mock_trader.get_inventories.assert_called_once()

    # Assert the length of the result
    assert len(result) == 1

    # Assert the content of the InventorySummary
    inventory = result[0]
    assert inventory.ap_code == ""
    assert inventory.cost_qty == 70
    assert inventory.cost_sum == -62949
    assert inventory.make_a_per == 8.16
    assert inventory.make_a_sum == 5139
    assert inventory.price_avg == 898.00
    assert inventory.price_evn == 903.27
    assert inventory.price_mkt == 977.00
    assert inventory.price_now == 977.00
    assert inventory.price_qty_sum == 62860
    assert inventory.qty_b == 0
    assert inventory.qty_l == 70
    assert inventory.stk_na == "台積電"
    assert inventory.stk_no == "2330"

    # Assert the content of the InventoryDetail
    detail = inventory.stk_dats[0]
    assert detail.buy_sell == "B"
    assert detail.cost_r == 0
    assert detail.fee == 89
    assert detail.make_a == 5139
    assert detail.make_a_per == 8.16
    assert detail.ord_no == "B5978032272160"
    assert detail.pay_n == -62949
    assert detail.price == 898.00
    assert detail.price_evn == 903.27
    assert detail.qty == 70
    assert detail.t_date == "20240904"
    assert detail.value_mkt == 68390
    assert detail.value_now == 68390

@patch.object(TraderSingleton, 'trader', create=True)  # Mock TraderSingleton.trader
def test_get_balance(mock_trader, mock_trader_methods):
    mock_data = {
        "available_balance": 500000, 
        "exange_balance": 100000,  
        "stock_pre_save_amount": 100000
    }
    # Mock the return value of self.trader.get_balance()
    mock_trader.get_balance = MagicMock(return_value=mock_data)
    # Create the TraderSingleton instance
    trader = TraderSingleton()
    balance = trader.get_balance()
    mock_trader.get_balance.assert_called_once()

    assert balance.available_balance == 500000