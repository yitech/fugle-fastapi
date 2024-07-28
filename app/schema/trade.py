from pydantic import BaseModel
from typing import List, Optional

class CreateOrder(BaseModel):
    buy_sell: str
    ap_code: str
    price_flag: str
    bs_flag: str
    stock_no: str
    quantity: int
    price: float