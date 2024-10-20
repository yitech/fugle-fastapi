from typing import Optional
from pydantic import BaseModel


class SettlementResponse(BaseModel):
    c_date: str
    date: str
    price: str


class BalanceResponse(BaseModel):
    available_balance: int
    exchange_balance: int
    stock_pre_save_amount: int


class InventoryDetail(BaseModel):
    buy_sell: str
    cost_r: Optional[float] = None
    fee: float
    make_a: float
    make_a_per: float
    ord_no: str
    pay_n: float
    price: float
    price_evn: float
    qty: int
    qty_c: Optional[int] = None
    qty_h: Optional[int] = None
    qty_r: Optional[int] = None
    t_date: str
    t_time: Optional[str] = None
    tax: Optional[float] = None
    tax_g: Optional[float] = None
    trade: Optional[int] = None
    value_mkt: float
    value_now: float
    user_def: Optional[str] = None


class InventoryResponse(BaseModel):
    ap_code: Optional[str] = None
    cost_qty: float
    cost_sum: float
    make_a_per: float
    make_a_sum: float
    price_avg: float
    price_evn: float
    price_mkt: float
    price_now: float
    price_qty_sum: float
    qty_b: int
    qty_bm: int
    qty_c: int
    qty_l: int
    qty_s: int
    qty_sm: int
    rec_va_sum: float
    s_type: str
    stk_dats: list[InventoryDetail]
    stk_na: str
    stk_no: str
    trade: Optional[int] = None
    value_mkt: float
    value_now: float
