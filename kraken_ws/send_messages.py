import asyncio
import logging
import websockets


async def send_messages(
    websocket: websockets.WebSocketClientProtocol, send_queue: asyncio.Queue
):
    """
    Continuously sends messages from the send_queue to the WebSocket.

    Args:
        websocket: An active WebSocket connection with an async `send` method.
        send_queue (asyncio.Queue): Queue containing messages to be sent.
    """
    try:
        while True:
            # Wait for the next message from the queue
            message = await send_queue.get()
            if message is None:
                # None is a signal to gracefully shut down the sender
                logging.info("Received shutdown signal. Exiting send_messages loop.")
                break

            # Attempt to send the message over the WebSocket
            try:
                await websocket.send(message)
            except Exception as send_error:
                logging.error(f"Failed to send message: {message}. Error: {send_error}")
                # Optionally, you can decide how to handle send failures here
    except asyncio.CancelledError:
        logging.info("Send messages task has been cancelled.")
    except Exception as e:
        logging.exception(f"Unexpected error in send_messages: {e}")
    finally:
        logging.info("Send messages task has terminated.")
