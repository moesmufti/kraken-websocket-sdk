from typing import Union
from kraken_ws.models.kraken_ticker import TickerData, TickerMethodResponse
from kraken_ws.models.kraken_instruments import InstrumentsHeartbeatResponse  # Import as necessary

TickerWebSocketResponse = Union[
    TickerData,
    TickerMethodResponse,
    InstrumentsHeartbeatResponse,  # Reuse existing heartbeat model
]
