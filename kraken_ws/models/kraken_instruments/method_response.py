from pydantic import BaseModel
from typing import Literal
from typing import Optional

class InstrumentsMethodResponse(BaseModel):
    method: Literal["subscribe", "unsubscribe"]
    req_id: Optional[int]
    result: dict