from app.dependencies.fugle import TraderSingleton
from app.schema.trade import CreateOrder
from fugle_trade.order import OrderObject
from fugle_trade.constant import (APCode, Trade, PriceFlag, BSFlag, Action)



def create_order(trader: TraderSingleton, order: CreateOrder):
    order = OrderObject(
        buy_sell=CreateOrder.,
        price_flag=PriceFlag.Limit,
        bs_flag=BSFlag.ROD,
        price=1200,
        stock_no="2454",
        quantity=40,
        ap_code=APCode.IntradayOdd
    )
    trader.create_order(order)
    return [{"item_id": "item1"}, {"item_id": "item2"}]

# 讀取設定檔
config = ConfigParser()
config.read('./config.ini')
sdk = SDK(config)
# 登入
sdk.login()
# 建立委託物件
order = OrderObject(
    buy_sell=Action.Buy,
    price_flag=PriceFlag.Limit,
    bs_flag=BSFlag.ROD,
    price=1200,
    stock_no="2454",
    quantity=40,
    ap_code=APCode.IntradayOdd
)

res = sdk.get_balance()
# res = sdk.place_order(order)
print(res)