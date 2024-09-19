from app.dependencies.fugle import TraderSingleton
from app.schema.trader import (
    CreateOrder, OrderResponse, OrderResult, CancelResponse, MarketStatusResponse,
    SettlementResponse
)
from fugle_trade.order import OrderObject


def create_order(trader: TraderSingleton, order: CreateOrder) -> OrderResponse:
    order = OrderObject(
        ap_code=order.ap_code,
        buy_sell=order.buy_sell,
        price_flag=order.price_flag,
        bs_flag=order.bs_flag,
        trade=order.trade,
        price=order.price,
        stock_no=order.stock_no,
        quantity=order.quantity,
    )
    order_response = trader.place_order(order)
    return OrderResponse(**order_response)


def get_order_results(trader: TraderSingleton) -> list[OrderResult]:
    order_results = trader.get_order_results()
    results: list[OrderResult] = []
    for order in order_results:
        results.append(OrderResult(**order.model_dump()))
    return trader.get_order_results()


def cancel_order(trader: TraderSingleton, ord_no: str) -> CancelResponse:
    res = trader.cancel_order(ord_no)
    return CancelResponse(**res.model_dump())

def get_market_status(trader: TraderSingleton) -> MarketStatusResponse:
    res = trader.get_market_status()
    return MarketStatusResponse(**res.model_dump())

def get_settlements(trader: TraderSingleton) -> SettlementResponse:
    res = trader.get_settlements()
    return SettlementResponse(**res.model_dump())
