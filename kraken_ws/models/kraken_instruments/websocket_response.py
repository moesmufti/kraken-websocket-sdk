from typing import Union
from kraken_ws.models.kraken_instruments import InstrumentsSnapshotOrUpdateResponse, InstrumentsStatusUpdateResponse, InstrumentsHeartbeatResponse, InstrumentsMethodResponse

# Union of all possible responses
InstrumentsWebSocketResponse = Union[
    InstrumentsSnapshotOrUpdateResponse, InstrumentsStatusUpdateResponse, InstrumentsHeartbeatResponse, InstrumentsMethodResponse
]
