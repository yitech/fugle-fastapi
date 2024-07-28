from app.dependencies.fugle import TraderSingleton
from app.schema.trade import CreateOrder
from fugle_trade.order import OrderObject


def create_order(trader: TraderSingleton, order: CreateOrder):
    order = OrderObject(
        ap_code=CreateOrder.ap_code,
        buy_sell=CreateOrder.buy_sell,
        price_flag=CreateOrder.price_flag,
        bs_flag=CreateOrder.bs_flag,
        price=CreateOrder.price,
        stock_no=CreateOrder.stock_no,
        quantity=CreateOrder.quantity
    )
    res = trader.place_order(order)
    return res
