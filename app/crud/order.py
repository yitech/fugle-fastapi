from app.dependencies.fugle import TraderSingleton
from app.schema.order import CreateOrder
from fugle_trade.order import OrderObject


def create_order(trader: TraderSingleton, order: CreateOrder):
    order = OrderObject(
        ap_code=order.ap_code,
        buy_sell=order.buy_sell,
        price_flag=order.price_flag,
        bs_flag=order.bs_flag,
        price=order.price,
        stock_no=order.stock_no,
        quantity=order.quantity
    )
    
    res = trader.place_order(order)
    return res
