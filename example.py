from configparser import ConfigParser
from fugle_trade.sdk import SDK
from fugle_trade.order import OrderObject
from fugle_trade.constant import (APCode, Trade, PriceFlag, BSFlag, Action)
# 讀取設定檔
config = ConfigParser()
config.read('./config.ini')
sdk = SDK(config)
# 登入
sdk.login()
# 建立委託物件
order = OrderObject(
    buy_sell = Action.Buy,
    price_flag = PriceFlag.Market,
    price = 920,
    stock_no = "2330",
    quantity = 60,
    ap_code = APCode.IntradayOdd
)
sdk.place_order(order)