from pydantic import BaseModel, ValidationError

class BalanceResponse(BaseModel):
    available: int
    locked: int

class InventoryResponse(BaseModel):
    symbol: str
    qty_share: int
