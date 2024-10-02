from typing import Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, field_validator, ValidationInfo
from fugle_trade.constant import APCode, Trade, PriceFlag, BSFlag, Action


class OrderPlacement(BaseModel):
    ord_date: str
    ord_time: str
    ord_type: str
    ord_no: str
    ret_code: str
    ret_msg: str
    work_date: str


class OrderResult(BaseModel):
    ap_code: APCode
    avg_price: float
    bs_flag: BSFlag
    buy_sell: Action
    cel_qty: float
    cel_qty_share: int
    celable: str
    err_code: str
    err_msg: str
    mat_qty: float
    mat_qty_share: int
    od_price: float
    ord_date: str
    ord_no: str
    ord_status: str
    ord_time: str
    org_qty: float
    org_qty_share: int
    pre_ord_no: str
    price_flag: PriceFlag
    stock_no: str
    trade: Trade
    work_date: str
    user_def: str = ""

    @field_validator("ord_no")
    def validate_ord_no(cls, v: str, info: ValidationInfo):
        pre_ord_no = info.data.get("pre_ord_no")
        if v == "" and pre_ord_no == "":
            raise ValueError("ord_no cannot be empty")
        return v

    @property
    def ord_id(self):
        return self.ord_no if self.ord_no != "" else self.pre_ord_no

    def update(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)
        return self

    def model_dump_with_enum(self) -> Dict[str, Any]:
        # Convert the model to a dictionary and manually convert enums
        result = super().model_dump()
        for key, value in result.items():
            if isinstance(value, Enum):
                result[key] = value.value
        return result


class NotifyAck(BaseModel):
    kind: str
    work_date: str
    ret_date: str
    ret_time: str
    ord_status: str
    ord_no: str
    pre_ord_no: str
    stock_no: str
    ap_code: APCode
    buy_sell: Action
    trade: Trade
    price_flag: PriceFlag
    od_price: float
    org_qty: float
    mat_qty: float
    cel_qty: float
    cel_type: str
    err_code: str
    err_msg: str
    action: str
    before_qty: float
    after_qty: float
    bs_flag: BSFlag

    @field_validator("ord_no")
    def validate_ord_no(cls, v: str, info: ValidationInfo):
        pre_ord_no = info.data.get("pre_ord_no")
        if v == "" and pre_ord_no == "":
            raise ValueError("ord_no cannot be empty")
        return v

    @property
    def ord_id(self):
        return self.ord_no if self.ord_no != "" else self.pre_ord_no


class CancelResult(BaseModel):
    ord_date: str
    ord_time: str
    ret_code: str
    ret_msg: str


class MarketStatusResult(BaseModel):
    is_trading_day: bool
    last_trading_day: str
    next_trading_day: str


class Settlement(BaseModel):
    c_date: str
    date: str
    price: str


class Balance(BaseModel):
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


class InventorySummary(BaseModel):
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
