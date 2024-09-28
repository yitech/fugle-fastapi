from typing import Optional
from pydantic import (
    BaseModel, Field, ValidationInfo, field_validator
)
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
