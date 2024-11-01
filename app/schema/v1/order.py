from pydantic import BaseModel, Field, ValidationInfo, field_validator
from enum import Enum
from fugle_trade.constant import APCode, Trade, PriceFlag, BSFlag, Action


    

class CreateOrder(BaseModel):
    buy_sell: Action
    ap_code: APCode
    price_flag: PriceFlag
    bs_flag: BSFlag
    trade: Trade
    stock_no: str
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    user_def: str = ""

    @field_validator("quantity")
    def validate_quantity(cls, v: int, info: ValidationInfo):
        ap_code = info.data.get("ap_code")
        # v = values.get('quantity')
        if ap_code == APCode.Common or ap_code == APCode.AfterMarket:
            if v < 1 or v > 499:
                raise ValueError("quantity must be within range 1 ~ 499")
        elif ap_code == APCode.Odd or ap_code == APCode.IntradayOdd:
            if v < 1 or v > 1000:
                raise ValueError("quantity must be within range 1 ~ 999")
        elif ap_code == APCode.Emg:
            if v < 1 or v > 499000 or (v > 1000 and v % 1000 != 0):
                raise ValueError(
                    "quantity must be within range 1 ~ 499000, or a multiple of 1000"
                )
        return v


class OrderResponse(BaseModel):
    ord_date: str
    ord_time: str
    ord_type: str
    ord_no: str
    ret_code: str
    ret_msg: str
    work_date: str


class CancelResponse(BaseModel):
    ret_code: str
    ret_msg: str
    ord_date: str
    ord_time: str


class OrderResultResponse(BaseModel):
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


class MarketStatusResponse(BaseModel):
    is_trading_day: bool
    last_trading_day: str
    next_trading_day: str


class MatDetail(BaseModel):
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
    buy_sell: str
    c_date: str
    cost: int
    make: int
    make_per: float
    mat_dats: list[MatDetail]
    price_avg: str
    price_qty: str
    qty: str
    recv: int
    s_type: str
    stk_na: str
    stk_no: str
    t_date: str
    trade: int
