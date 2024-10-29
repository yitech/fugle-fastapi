from typing import Literal
from pydantic import BaseModel, ValidationError
from datetime import datetime

class RawTransaction(BaseModel):
    buy_sell: str
    c_date: str
    db_fee: str = "0"
    fee: str
    make: int
    make_per: float
    order_no: str
    pay_n: str
    price: str
    price_qty: str
    qty: str
    s_type: str
    stk_na: str
    stk_no: str
    t_date: str
    t_time: str = ""
    tax: str
    tax_g: str
    trade: int
    user_def: str = ""


class TransactionResponse(BaseModel):
    side: Literal["B", "S"]
    datetime: datetime
    fee: int
    order_no: str
    price: float
    qty: int
    symbol: str
    tax: int
    trade: int

    @classmethod
    def from_rawdata(cls, data: dict):
        """
        data format =
            {
                "buy_sell": "B",
                "c_date": "20240812",
                "db_fee": "0",
                "fee": "15",
                "make": 0,
                "make_per": 0.0,
                "order_no": "66910011350210",
                "pay_n": "-11115",
                "price": "1110.00",
                "price_qty": "11100",
                "qty": "10",
                "s_type": "H",
                "stk_na": "聯發科",
                "stk_no": "2454",
                "t_date": "20240808",
                "t_time": "",
                "tax": "0",
                "tax_g": "0",
                "trade": 0,
                "user_def": ""
            }
        """
        try:
            RawTransaction(**data) # validate data
        except ValidationError as e:
            raise e
        if data["t_time"] == "":
            dt = datetime.strptime(data["t_date"], "%Y%m%d")
        else:
            dt = datetime.strptime(data["t_date"]+data["t_time"], "%Y%m%d%H%M%S%f")
        return TransactionResponse(
            side=data["buy_sell"],
            datetime=dt,
            fee=int(data["fee"]),
            order_no=data["order_no"],
            price=float(data["price"]),
            qty=int(data["qty"]),
            symbol=data["stk_no"],
            tax=int(data["tax"]),
            trade=data["trade"]
        )