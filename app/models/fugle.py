from pydantic import BaseModel, field_validator, ValidationInfo
from fugle_trade.constant import (APCode, Trade, PriceFlag, BSFlag, Action)

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
    user_def: str = ''
    
    @field_validator('ord_no')
    def validate_ord_no(cls, v: str, info: ValidationInfo):
        pre_ord_no = info.data.get('pre_ord_no')
        if v == '' and pre_ord_no == '':
            raise ValueError("ord_no cannot be empty")
        return v
    
    @property
    def ord_id(self):
        return self.ord_no if self.ord_no != '' else self.pre_ord_no
    
    def update(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)
        return self


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
    
    @field_validator('ord_no')
    def validate_ord_no(cls, v: str, info: ValidationInfo):
        pre_ord_no = info.data.get('pre_ord_no')
        if v == '' and pre_ord_no == '':
            raise ValueError("ord_no cannot be empty")
        return v
    
    @property
    def ord_id(self):
        return self.ord_no if self.ord_no != '' else self.pre_ord_no
"""
    @field_validator('org_qty_share')
    def validate_org_qty_share(cls, v: Optional[int], info: ValidationInfo):
        if v:
            raise ValueError("share should not be provided")
        return int(info.data['org_qty'] * 1000)

    @field_validator('mat_qty_share')
    def validate_mat_qty_share(cls, v: Optional[int], info: ValidationInfo):
        if v:
            raise ValueError("share should not be provided")
        return int(info.data['mat_qty'] * 1000)
    
    @field_validator('cel_qty_share')
    def validate_cel_qty_share(cls, v: Optional[int], info: ValidationInfo):
        if v:
            raise ValueError("share should not be provided")
        return int(info.data['cel_qty'] * 1000)
    
""" 