from typing import Dict, Any
from enum import Enum
from pydantic import BaseModel, field_validator, ValidationInfo
from fugle_trade.constant import APCode, Trade, PriceFlag, BSFlag, Action


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