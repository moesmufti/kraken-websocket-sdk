from pydantic import BaseModel
from typing import Literal


class InstrumentsHeartbeatResponse(BaseModel):
    channel: Literal["heartbeat"]
    # No data field as heartbeat contains no additional data
