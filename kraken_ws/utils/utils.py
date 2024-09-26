from pydantic import TypeAdapter
from typing import Union
from kraken_ws.models.kraken_instruments.websocket_response import InstrumentsWebSocketResponse as InstrumentWebSocketResponse
from kraken_ws.models.kraken_ticker.websocket_response import TickerWebSocketResponse

# Union of instrument and ticker responses
CombinedWebSocketResponse = Union[InstrumentWebSocketResponse, TickerWebSocketResponse]

ws_response_adapter = TypeAdapter(CombinedWebSocketResponse)