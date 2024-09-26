from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class TickerUnsubscribeParams(BaseModel):
    channel: Literal["ticker"]
    symbol: List[str]  # List of currency pairs to unsubscribe from
    event_trigger: Optional[Literal["bbo", "trades"]] = Field(
        default="trades",
        description="The book event that triggers ticker updates.",
    )


class TickerUnsubscribeRequest(BaseModel):
    method: Literal["unsubscribe"]
    params: TickerUnsubscribeParams
    req_id: Optional[int] = Field(
        default=None,
        description="Optional client-originated request identifier.",
    )
