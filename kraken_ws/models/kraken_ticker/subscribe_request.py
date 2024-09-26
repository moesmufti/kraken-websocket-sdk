from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class TickerSubscribeParams(BaseModel):
    channel: Literal["ticker"]
    symbol: List[str]  # List of currency pairs to subscribe to
    event_trigger: Optional[Literal["bbo", "trades"]] = Field(
        default="trades",
        description="The book event that triggers ticker updates.",
    )
    snapshot: Optional[bool] = Field(
        default=True,
        description="Request a snapshot after subscribing.",
    )


class TickerSubscribeRequest(BaseModel):
    method: Literal["subscribe"]
    params: TickerSubscribeParams
    req_id: Optional[int] = Field(
        default=None,
        description="Optional client-originated request identifier.",
    )
