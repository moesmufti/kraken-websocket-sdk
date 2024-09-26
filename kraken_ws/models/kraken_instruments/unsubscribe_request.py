from typing import Optional, Literal
from pydantic import BaseModel, Field


class InstrumentsUnsubscribeParams(BaseModel):
    channel: Literal["instrument"]


class InstrumentsUnsubscribeRequest(BaseModel):
    method: Literal["unsubscribe"]
    params: InstrumentsUnsubscribeParams
    req_id: Optional[int] = Field(
        default=None, description="Optional client-originated request identifier."
    )
