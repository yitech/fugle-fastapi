from configparser import ConfigParser
from fugle_trade.sdk import SDK
from fugle_trade.order import OrderObject
from fugle_trade.constant import (APCode, Trade, PriceFlag, BSFlag, Action)
from dotenv import load_dotenv
import os
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