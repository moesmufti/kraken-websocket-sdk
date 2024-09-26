from pydantic import BaseModel
from typing import List, Literal


class InstrumentsStatusObject(BaseModel):
    system: Literal["online", "cancel_only", "maintenance", "post_only"]
    api_version: str
    connection_id: int
    version: str


class InstrumentsStatusUpdateResponse(BaseModel):
    channel: Literal["status"]
    type: Literal["update"]
    data: List[InstrumentsStatusObject]
