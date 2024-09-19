from fastapi import APIRouter, Depends, HTTPException
import logging

logger = logging.getLogger("fugle")

router = APIRouter()


@router.get("/settlements", response_model="Settlements")
def get_settlements():
    return {"message": "Not implemented yet"}


@router.get("/balance", response_model="Balance")
def get_balance():
    return {"message": "Not implemented yet"}


@router.get("/inventories", response_model="Inventories")
def get_inventories():
    return {"message": "Not implemented yet"}

