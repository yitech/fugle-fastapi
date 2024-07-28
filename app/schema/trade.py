from pydantic import BaseModel, Field, field_validator
from fugle_trade.constant import (APCode, Trade, PriceFlag, BSFlag, Action)

class CreateOrder(BaseModel):
    buy_sell: Action
    ap_code: APCode
    price_flag: PriceFlag
    bs_flag: BSFlag
    stock_no: str
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)

    @field_validator('stock_no')
    def stock_no_must_be_str(cls, v):
        if not isinstance(v, str):
            raise TypeError("stock_no must be a string")
        return v
"""
    @field_validator('quantity')
    def validate_quantity(cls, v, values):
        ap_code = values.get('ap_code')
        if ap_code == APCode.Common or ap_code == APCode.AfterMarket:
            if v < 1 or v > 499:
                raise ValueError("quantity must be within range 1 ~ 499")
        elif ap_code == APCode.Odd or ap_code == APCode.IntradayOdd:
            if v < 1 or v > 1000:
                raise ValueError("quantity must be within range 1 ~ 999")
        elif ap_code == APCode.Emg:
            if v < 1 or v > 499000 or (v > 1000 and v % 1000 != 0):
                raise ValueError("quantity must be within range 1 ~ 499000, or a multiple of 1000")
        return v
"""