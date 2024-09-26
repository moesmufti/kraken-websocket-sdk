<h1 align="center">Kraken WebSocket SDK - Lightweight and minimal SDK for interacting with the Kraken Cryptocurrency Exchange Websocket API</h1>

**Disclaimer:**  
*This SDK is not affiliated with Kraken in any way and does not provide financial services or products. Trading involves significant risk and is speculative. Always do your own research and consult with a financial advisor before making any trading decisions.*

A Python package for interacting with Kraken's WebSocket API, enabling real-time data streaming for instruments and ticker channels with robust features for reliability and ease of use.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
  - [Connecting to Kraken WebSocket](#connecting-to-kraken-websocket)
  - [Subscribing to Channels](#subscribing-to-channels)
  - [Sending and Receiving Messages](#sending-and-receiving-messages)
  - [Processing Data](#processing-data)
- [Example](#example)
- [Running the Example](#running-the-example)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Subscribe to Instrument and Ticker Channels:** Receive updates on trading instruments and ticker information.
- **Handle Real-Time Updates:** Process incoming data in real-time with asynchronous support.
- **Automatic Reconnection:** Maintains connection with exponential backoff strategy in case of disconnections.
- **Asynchronous Support:** Built with `asyncio` for efficient concurrency.
- **Robust Error Handling:** Logs and manages unexpected errors gracefully.
- **Easy Integration:** Simple API to integrate with your applications.

## Installation

Install the package using `pip`:

```bash
pip install kraken-websocket-sdk
```

## Quick Start
Here's a minimal example to get you started with the Kraken WebSocket SDK:

Connecting to Kraken WebSocket
Establish a connection to Kraken's WebSocket API with automatic reconnection using exponential backoff.

```python
from kraken_ws import connect
import asyncio
import logging

async def establish_connection():
    websocket = await connect()
    if websocket:
        print("Connected to Kraken WebSocket.")
    else:
        print("Failed to connect to Kraken WebSocket.")

# Example usage
if __name__ == "__main__":
    asyncio.run(establish_connection())
```

Subscribing to Channels
Subscribe to desired channels such as instrument and ticker to receive relevant data.

```python
from kraken_ws import (
    subscribe_to_instruments,
    subscribe_to_tickers
)
import asyncio

async def subscribe_channels(send_queue):
    # Subscribe to instruments
    await subscribe_to_instruments(send_queue)
    print("Subscribed to instruments.")

    # Subscribe to tickers for specific symbols
    await subscribe_to_tickers(send_queue, ["BTC/USD", "ETH/USD"])
    print("Subscribed to tickers.")

# Example usage
if __name__ == "__main__":
    asyncio.run(subscribe_channels(asyncio.Queue()))
```

Sending and Receiving Messages
Use dedicated tasks to handle sending and receiving messages through the WebSocket connection.

```python
from kraken_ws.send_messages import send_messages
from kraken_ws.receive_messages import receive_messages
import asyncio

async def manage_communication(websocket, send_queue, tickers_queue, instruments_queue):
    send_task = asyncio.create_task(send_messages(websocket, send_queue))
    receive_task = asyncio.create_task(receive_messages(websocket, tickers_queue, instruments_queue))
    
    await asyncio.gather(send_task, receive_task)

# Example usage
if __name__ == "__main__":
    # Assume websocket and queues are already created
    websocket = None  # Replace with actual websocket connection
    send_queue = asyncio.Queue()
    tickers_queue = asyncio.Queue()
    instruments_queue = asyncio.Queue()

    asyncio.run(manage_communication(websocket, send_queue, tickers_queue, instruments_queue))
```

Processing Data
Process incoming ticker and instrument data asynchronously.

```python
import logging
import asyncio

async def process_tickers(tickers_queue):
    while True:
        ticker_message = await tickers_queue.get()
        ticker_data = ticker_message.get("data")
        logging.info(f"Received ticker data: {ticker_data}")

async def process_instruments(instruments_queue):
    while True:
        instruments_message = await instruments_queue.get()
        instruments_data = instruments_message.get("data")
        logging.info(f"Received instruments data: {instruments_data}")

# Example usage
if __name__ == "__main__":
    tickers_queue = asyncio.Queue()
    instruments_queue = asyncio.Queue()

    asyncio.run(asyncio.gather(
        process_tickers(tickers_queue),
        process_instruments(instruments_queue)
    ))
```

Logging
If you would like to use a preset logger that works with all the python logging statements, you can use the `kraken_ws.config.logging_config` module:

```python
import logging
from kraken_ws.config.logging_config import setup_logging
setup_logging(level=logging.INFO)
```

## Example
An example script demonstrating how to use the Kraken WebSocket SDK is provided in the examples directory.

## Running the Example
Clone the Repository:

git clone https://github.com/moesmufti/kraken-websocket-sdk.git
cd kraken-websocket-sdk

Install Dependencies:

Ensure you have Python 3.12 or later installed. Install the required packages:

pip install -r requirements.txt

Run the Example:

python examples/kraken_ws_example.py
This script connects to Kraken's WebSocket, subscribes to instrument and ticker channels for BTC/USD and ETH/USD, and logs the received data.

## Contributing
Contributions are welcome! Whether it's reporting bugs, improving documentation, or adding new features, your help is appreciated.

Fork the Repository

Create a Feature Branch

git checkout -b feature/YourFeature
Commit Your Changes

git commit -m "Add your message here"
Push to the Branch

git push origin feature/YourFeature
Open a Pull Request

Please ensure your contributions adhere to the project's coding standards and include appropriate tests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.