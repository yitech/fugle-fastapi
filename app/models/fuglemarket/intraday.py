from pydantic import BaseModel
from typing import Optional
from datetime import date


class BidAsk(BaseModel):
    price: float
    size: int


class Total(BaseModel):
    tradeValue: int
    tradeVolume: int
    tradeVolumeAtBid: int
    tradeVolumeAtAsk: int
    transaction: int
    time: int


class LastTrade(BaseModel):
    bid: float
    ask: float
    price: float
    size: int
    time: int
    serial: int


class LastTrial(BaseModel):
    bid: float
    ask: float
    price: float
    size: int
    time: int
    serial: int


class Quote(BaseModel):
    date: date
    type: str
    exchange: str
    market: str
    symbol: str
    name: str
    referencePrice: float
    previousClose: float
    openPrice: float
    openTime: int
    highPrice: float
    highTime: int
    lowPrice: float
    lowTime: int
    closePrice: float
    closeTime: int
    avgPrice: float
    change: float
    changePercent: float
    amplitude: float
    lastPrice: float
    lastSize: int
    bids: list[BidAsk]
    asks: list[BidAsk]
    total: Total
    lastTrade: LastTrade
    lastTrial: LastTrial
    isTrial: bool
    serial: int
    lastUpdated: int


class KLine(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int


class KLines(BaseModel):
    symbol: str
    type: str
    exchange: str
    market: str
    timeframe: str
    data: list[KLine]
