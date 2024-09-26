from typing import List, Optional
from pydantic import BaseModel, Field
from typing import Literal


class InstrumentsAsset(BaseModel):
    borrowable: bool
    collateral_value: Optional[float] = None
    id: str
    margin_rate: Optional[float] = None
    precision: int
    precision_display: int
    status: Literal[
        "depositonly",
        "disabled",
        "enabled",
        "fundingtemporarilydisabled",
        "withdrawalonly",
        "workinprogress",
    ]


class InstrumentsPair(BaseModel):
    base: str
    quote: str
    cost_min: Optional[float] = None
    cost_precision: int
    has_index: bool
    margin_initial: Optional[float] = None
    marginable: bool
    position_limit_long: Optional[int] = None
    position_limit_short: Optional[int] = None
    price_increment: float
    price_precision: int
    qty_increment: float
    qty_min: float
    qty_precision: int
    status: Literal[
        "cancel_only",
        "delisted",
        "limit_only",
        "maintenance",
        "online",
        "post_only",
        "reduce_only",
        "work_in_progress",
    ]
    symbol: str
    tick_size: Optional[float] = Field(
        default=None, description="Deprecated. Use 'price_increment'."
    )


class InstrumentsData(BaseModel):
    assets: List[InstrumentsAsset]
    pairs: List[InstrumentsPair]


class InstrumentsSnapshotOrUpdateResponse(BaseModel):
    channel: Literal["instrument"]
    type: Literal["snapshot", "update"]
    data: InstrumentsData
