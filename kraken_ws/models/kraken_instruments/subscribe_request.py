from typing import Optional, Literal
from pydantic import BaseModel, Field


class InstrumentsSubscribeParams(BaseModel):
    channel: Literal["instrument"]
    snapshot: Optional[bool] = Field(
        default=True, description="Request a snapshot after subscribing."
    )


class InstrumentsSubscribeRequest(BaseModel):
    method: Literal["subscribe"]
    params: InstrumentsSubscribeParams
    req_id: Optional[int] = Field(
        default=None, description="Optional client-originated request identifier."
    )
