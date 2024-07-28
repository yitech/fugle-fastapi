from fastapi import APIRouter, Depends
from app.schema.trade import CreateOrder
from app.dependencies import get_trader


router = APIRouter()

@router.post("/create_order", tags=["trade"])
async def create_order(
    order: CreateOrder,
    trader = Depends(get_trader)
):

    return [{"item_id": "item1"}, {"item_id": "item2"}]
