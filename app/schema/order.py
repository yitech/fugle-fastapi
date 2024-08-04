from pydantic import BaseModel, Field, ValidationInfo, field_validator
from fugle_trade.constant import (APCode, PriceFlag, BSFlag, Action)

class CreateOrder(BaseModel):
    buy_sell: Action
    ap_code: APCode
    price_flag: PriceFlag
    bs_flag: BSFlag
    stock_no: str
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)

    @field_validator('quantity')
    def validate_quantity(cls, v: int, info: ValidationInfo):
        ap_code = info.data.get('ap_code')
        # v = values.get('quantity')
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


class OrderResponse(BaseModel):
    ord_date: str
    ord_time: str
    ord_type: str
    ord_no: str
    ret_code: str
    ret_msg: str
    work_date: str