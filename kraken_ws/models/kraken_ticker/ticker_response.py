from typing import Optional, List, Literal
from pydantic import BaseModel


class TickerData(BaseModel):
    channel: Literal["ticker"]
    type: Literal["snapshot", "update"]
    data: List["Ticker"]  # Forward reference to be defined


class Ticker(BaseModel):
    symbol: str
    bid: float
    bid_qty: float
    ask: float
    ask_qty: float
    change: float
    change_pct: float
    high: float
    last: float
    low: float
    volume: float
    vwap: float
