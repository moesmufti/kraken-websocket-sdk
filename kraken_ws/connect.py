import asyncio
import logging
import websockets
from websockets.exceptions import ConnectionClosed

# Constants
KRAKEN_WEBSOCKET_URL = "wss://ws.kraken.com/v2"
INITIAL_RETRY_DELAY = 1  # Initial delay in seconds before retrying
MAX_RETRY_DELAY = 60  # Maximum delay in seconds for exponential backoff
RETRY_EXCEPTIONS = (
    ConnectionClosed,
    asyncio.TimeoutError,
)  # Exceptions that trigger a reconnect


async def connect():
    """
    Establishes and maintains a WebSocket connection to Kraken.
    Implements exponential backoff for reconnection attempts
    in case of connection loss or timeout.

    Returns:
        websockets.WebSocketClientProtocol: The active WebSocket connection.
    """
    retry_delay = INITIAL_RETRY_DELAY

    while True:
        try:
            # Attempt to establish a WebSocket connection
            websocket = await websockets.connect(KRAKEN_WEBSOCKET_URL)
            logging.info("Connected to Kraken WebSocket.")
            return websocket  # Exit the loop upon successful connection

        except RETRY_EXCEPTIONS as e:
            # Handle expected exceptions and attempt to reconnect
            logging.warning(
                f"Connection lost ({e}). Reconnecting in {retry_delay} seconds..."
            )
            await asyncio.sleep(retry_delay)
            # Apply exponential backoff with a maximum delay
            retry_delay = min(retry_delay * 2, MAX_RETRY_DELAY)

        except asyncio.CancelledError:
            # Handle task cancellation gracefully
            logging.info("Connection task has been cancelled.")
            break  # Exit the loop to allow cleanup if necessary

        except Exception as e:
            # Log unexpected exceptions and terminate the connection attempt
            logging.error(f"Unexpected error: {e}")
            break

    return None  # Return None if connection was not established
