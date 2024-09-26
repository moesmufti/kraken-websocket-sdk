# kraken_ws/receive_messages.py

import json
import logging
import asyncio
from typing import Any, Dict, List
from kraken_ws.models.kraken_instruments import (
    InstrumentsPair,
    InstrumentsSnapshotOrUpdateResponse,
)
from kraken_ws.models.kraken_ticker import TickerData
import websockets
from kraken_ws.utils.utils import ws_response_adapter


async def receive_messages(
    websocket: websockets.WebSocketClientProtocol,
    tickers_queue: asyncio.Queue,
    instruments_queue: asyncio.Queue,
) -> None:
    """
    Continuously receives messages from the WebSocket and dispatches them to the appropriate queues.

    Args:
        websocket: The active WebSocket connection.
        tickers_queue: Queue for 'ticker_update' messages. Contains the following keys: 'type', 'response' - full parsed response, 'data' - parsed response.data
        instruments_queue: Queue for 'instruments' messages. Contains the following keys: 'type', 'response' - full parsed response, 'data' - parsed response.data
    """
    try:
        while True:
            response = await websocket.recv()
            await _handle_message(response, tickers_queue, instruments_queue)
    except websockets.exceptions.ConnectionClosed as e:
        logging.warning(f"WebSocket connection closed: {e}")
    except asyncio.CancelledError:
        logging.info("Receive messages task has been cancelled.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


async def _handle_message(
    message: str, tickers_queue: asyncio.Queue, instruments_queue: asyncio.Queue
) -> None:
    """
    Parses and handles a single WebSocket message.

    Args:
        message: The raw JSON message received from the WebSocket.
        tickers_queue: Queue for 'ticker_update' messages.
        instruments_queue: Queue for 'instruments' messages.
    """
    try:
        data: Dict[str, Any] = json.loads(message)

        if "method" in data:
            await _handle_method_response(data)
        elif "channel" in data:
            await _handle_channel_message(data, tickers_queue, instruments_queue)
        else:
            logging.warning("Received unknown message format")
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON received: {e}")
    except Exception as e:
        logging.error(f"Failed to process message: {e}")


async def _handle_method_response(data: Dict[str, Any]) -> None:
    """
    Handles method response messages (e.g., subscribe confirmations).

    Args:
        data: Parsed JSON data from the WebSocket message.
    """
    try:
        ws_response_adapter.validate_python(data)
    except Exception as e:
        logging.error(f"Failed to parse method response: {e}")


async def _handle_channel_message(
    data: Dict[str, Any], tickers_queue: asyncio.Queue, instruments_queue: asyncio.Queue
) -> None:
    """
    Dispatches messages based on their channel type.

    Args:
        data: Parsed JSON data from the WebSocket message.
        tickers_queue: Queue for 'ticker_update' messages.
        instruments_queue: Queue for 'instruments' messages.
    """
    channel: str = data.get("channel", "")

    if channel == "instrument":
        await _handle_instrument_channel(data, instruments_queue)
    elif channel == "ticker":
        await _handle_ticker_channel(data, tickers_queue)
    elif channel == "heartbeat":
        pass
    elif channel == "status":
        await _handle_status_update(data)
    else:
        logging.warning(f"Unknown channel: {channel}")


async def _handle_instrument_channel(
    data: Dict[str, Any], instruments_queue: asyncio.Queue
) -> None:
    """
    Processes instrument channel messages and enqueues relevant data.

    Args:
        data: Parsed JSON data from the WebSocket message.
        instruments_queue: Queue for 'instruments' messages. Contains the following keys: 'type', 'response' - full parsed response, 'data' - parsed response.data
    """
    try:
        parsed_response: InstrumentsSnapshotOrUpdateResponse = (
            ws_response_adapter.validate_python(data)
        )

        if parsed_response.type in {"snapshot", "update"}:
            pairs: List[InstrumentsPair] = parsed_response.data.pairs
            logging.info(f"{len(pairs)} Instrument pairs detected")

            await instruments_queue.put(
                {
                    "type": "instruments",
                    "response": parsed_response,
                    "data": parsed_response.data,
                }
            )
    except Exception as e:
        logging.error(f"Failed to handle instrument channel: {e}")


async def _handle_ticker_channel(
    data: Dict[str, Any], tickers_queue: asyncio.Queue
) -> None:
    """
    Processes ticker channel messages and enqueues relevant data.

    Args:
        data: Parsed JSON data from the WebSocket message.
        tickers_queue: Queue for 'ticker_update' messages. Contains the following keys: 'type', 'response' - full parsed response, 'data' - parsed response.data
    """
    try:
        parsed_response: TickerData = ws_response_adapter.validate_python(data)

        if parsed_response.type in {"snapshot", "update"}:
            await tickers_queue.put(
                {
                    "type": "update",
                    "response": parsed_response,
                    "data": parsed_response.data,
                }
            )
        else:
            logging.warning(f"Unknown ticker type: {parsed_response.type}")
    except Exception as e:
        logging.error(f"Failed to handle ticker channel: {e}")


async def _handle_status_update(data: Dict[str, Any]) -> None:
    """
    Processes status update messages.

    Args:
        data: Parsed JSON data from the WebSocket message.
    """
    try:
        ws_response_adapter.validate_python(data)
    except Exception as e:
        logging.error(f"Failed to handle status update: {e}")
