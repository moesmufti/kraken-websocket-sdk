import asyncio
import logging
from kraken_ws import (
    connect,
    subscribe_to_tickers,
    send_messages,
    receive_messages,
    subscribe_to_instruments,
)
from kraken_ws.models.kraken_ticker import TickerData, Ticker
from config import setup_logging

# Set up logging
setup_logging(level=logging.INFO)


async def process_subscribed_tickers(
    tickers_queue: asyncio.Queue, instruments_queue: asyncio.Queue
):
    while True:
        ticker_message = await tickers_queue.get()
        ticker_response: TickerData = ticker_message.get("response")
        if ticker_response.type == "update":
            ticker_data: Ticker = ticker_message.get("data")
            logging.info(f"Received ticker data: {ticker_data}")


async def main():
    # Create required Queues
    send_queue = asyncio.Queue(maxsize=1000)
    tickers_queue = asyncio.Queue() # Queue to store ticker data
    instruments_queue = asyncio.Queue() # Queue to store instruments data
    
    # Connect to the websocket
    websocket = await connect()

    # Create send and receive tasks
    send_task = asyncio.create_task(send_messages(websocket, send_queue))
    receive_task = asyncio.create_task(
        receive_messages(websocket, tickers_queue, instruments_queue)
    )

    # Subscribe to instruments
    await subscribe_to_instruments(send_queue)
    logging.info("Subscribed to instruments.")

    # Example delay for instruments data to be received
    instruments_message = await instruments_queue.get()
    instruments_data = instruments_message.get("data")
    
    # Subscribe to tickers
    if instruments_data:
        await subscribe_to_tickers(send_queue, ["BTC/USD", "ETH/USD"])
        logging.info("Subscribed to tickers.")

    # Example task to process ticker data
    process_subscribed_tickers_task = asyncio.create_task(
        process_subscribed_tickers(tickers_queue, instruments_queue)
    )

    # Run tasks
    try:
        await asyncio.gather(
            send_task,
            receive_task,
            process_subscribed_tickers_task,
        )
    except asyncio.CancelledError:
        logging.info("Main task has been cancelled.")
    except Exception as e:
        logging.error(f"Main encountered an error: {e}")
    finally:
        logging.info("Exiting main.")
        await websocket.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    except Exception as e:
        logging.error(f"Program terminated with an error: {e}")
