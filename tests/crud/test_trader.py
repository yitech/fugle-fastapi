import pytest
from unittest.mock import MagicMock
from app.dependencies.fugle import TraderSingleton
from app.schema.trader import (
    CreateOrder, OrderResponse, OrderResultResponse, CancelResponse, MarketStatusResponse,
    SettlementResponse
)
from app.models.fugle import (
    OrderResult, OrderPlacement, CancelResult, MarketStatusResult, Settlement
)
from app.crud import create_order, get_order_results, cancel_order, get_market_status, get_settlements


@pytest.fixture
def mock_trader():
    """Fixture for the mocked TraderSingleton."""
    trader = MagicMock(spec=TraderSingleton)
    yield trader


def test_create_order(mock_trader):
    # Mocked input and expected output
    mock_order = CreateOrder(
        buy_sell="B",
        ap_code="1",
        price_flag="0",
        bs_flag="R",
        trade="0",
        stock_no="2330",
        quantity=10,
        price=600.0
    )

    mock_response = OrderPlacement(
        ord_date="20220310", 
        ord_time="094932438",
        ord_type="2", 
        ord_no="A4461", 
        ret_code="000000", 
        ret_msg="",
        work_date="20220310"
    )
    
    mock_trader.place_order.return_value = mock_response

    # Call the function
    response = create_order(mock_trader, mock_order)

    # Assertions
    mock_trader.place_order.assert_called_once()
    assert isinstance(response, OrderResponse)
    assert response.ord_no == mock_response.ord_no
    assert response.ret_code == mock_response.ret_code


def test_get_order_results(mock_trader):
    # Mocked order results
    mock_orders = [
        OrderResult(
            ap_code="1",
            avg_price=0.0,
            bs_flag="R",
            buy_sell="B",
            cel_qty=1,
            cel_qty_share=1000,
            celable="2",
            err_code="00000000",
            err_msg="",
            mat_qty=0,
            mat_qty_share=0,
            od_price=25.95,
            ord_date="20220310",
            ord_no="A4461",
            ord_status="2",
            ord_time="094932438",
            org_qty=1,
            org_qty_share=1000,
            pre_ord_no="",
            price_flag="2",
            stock_no="2884",
            trade="0",
            work_date="20220310",
            user_def="下單測試"
        )
    ]
    
    mock_trader.get_order_results.return_value = mock_orders

    # Call the function
    results = get_order_results(mock_trader)

    # Assertions
    mock_trader.get_order_results.assert_called_once()
    assert len(results) == len(mock_orders)
    assert isinstance(results[0], OrderResultResponse)
    assert results[0].ord_no == mock_orders[0].ord_no


"""
def test_cancel_order(mock_trader):
    # Mocked cancel result
    mock_cancel_result = CancelResult(
        ord_date="2023-09-01",
        ord_time="12:35:00",
        ret_code="000",
        ret_msg="Success"
    )
    
    mock_trader.cancel_order.return_value = mock_cancel_result

    # Call the function
    response = cancel_order(mock_trader, "ORD123")

    # Assertions
    mock_trader.cancel_order.assert_called_once_with("ORD123")
    assert isinstance(response, CancelResponse)
    assert response.ret_code == mock_cancel_result.ret_code
    assert response.ret_msg == mock_cancel_result.ret_msg


def test_get_market_status(mock_trader):
    # Mocked market status result
    mock_market_status = MarketStatusResult(
        is_trading_day=True,
        last_trading_day="2023-08-31",
        next_trading_day="2023-09-01"
    )
    
    mock_trader.get_market_status.return_value = mock_market_status

    # Call the function
    response = get_market_status(mock_trader)

    # Assertions
    mock_trader.get_market_status.assert_called_once()
    assert isinstance(response, MarketStatusResponse)
    assert response.is_trading_day == mock_market_status.is_trading_day


def test_get_settlements(mock_trader):
    # Mocked settlement result
    mock_settlements = [
        Settlement(
            c_date="2023-08-31",
            date="2023-08-29",
            price="1000"
        ),
        Settlement(
            c_date="2023-09-01",
            date="2023-08-30",
            price="1500"
        )
    ]
    
    mock_trader.get_settlements.return_value = mock_settlements

    # Call the function
    response = get_settlements(mock_trader)

    # Assertions
    mock_trader.get_settlements.assert_called_once()
    assert len(response) == len(mock_settlements)
    assert isinstance(response[0], SettlementResponse)
    assert response[0].c_date == mock_settlements[0].c_date
    assert response[1].c_date == mock_settlements[1].c_date
"""