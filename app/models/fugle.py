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
    cost_r: Optional[float] = None  # 已分攤成本
    fee: float  # 手續費
    make_a: float  # 未實現損益
    make_a_per: float  # 未實現獲益率
    ord_no: str  # 委託書號
    pay_n: float  # 淨收付金額
    price: float  # 成交價格
    price_evn: float  # 平衡損益價
    qty: int  # 庫存股數
    qty_c: Optional[int] = None  # 調整股數
    qty_h: Optional[int] = None  # 實高權值股數
    qty_r: Optional[int] = None  # 已分攤股數
    t_date: str  # 成交日期
    t_time: Optional[str] = None  # 成交時間
    tax: Optional[float] = None  # 交易稅
    tax_g: Optional[float] = None  # 證所稅
    trade: Optional[int] = None  # 交易類別
    value_mkt: float  # 市值(無假除權息)
    value_now: float  # 市值(有假除權息)
    user_def: Optional[str] = None  # 自訂欄位

class InventorySummary(BaseModel):
    ap_code: Optional[str] = None  # 盤別
    cost_qty: float  # 成本股數
    cost_sum: float  # 成本總計
    make_a_per: float  # 未實現獲利率
    make_a_sum: float  # 未實現損益小計
    price_avg: float  # 成交均價
    price_evn: float  # 損益平衡價
    price_mkt: float  # 即時價格(無假除權息)
    price_now: float  # 即時價格(有假除權息)
    price_qty_sum: float  # 價金總計
    qty_b: int  # 今委買股數
    qty_bm: int  # 今委買成交股數
    qty_c: int  # 調整股數
    qty_l: int  # 昨餘額股數
    qty_s: int  # 今委賣股數
    qty_sm: int  # 今委賣成交股數
    rec_va_sum: float  # 未實現收入小計
    s_type: str  # 市場別
    stk_dats: list[InventoryDetail]  # 庫存明細
    stk_na: str  # 股票名稱
    stk_no: str  # 股票代碼
    trade: Optional[int] = None  # 交易類別
    value_mkt: float  # 市值(無假除權息)
    value_now: float  # 市值(有假除權息)
