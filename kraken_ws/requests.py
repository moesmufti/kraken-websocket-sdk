import asyncio
import logging
from typing import List
from kraken_ws.models.kraken_instruments import (
    InstrumentsSubscribeRequest,
    InstrumentsUnsubscribeRequest,
)
from kraken_ws.models.kraken_ticker import (
    TickerSubscribeRequest,
    TickerUnsubscribeRequest,
)

_request_id = 1
_request_lock = asyncio.Lock()


async def get_unique_req_id():
    global _request_id
    async with _request_lock:
        req_id = _request_id
        _request_id += 1
    return req_id


async def subscribe_to_instruments(send_queue):
    """
    Subscribes to the 'instrument' channel to receive instrument data.
    """
    req_id = await get_unique_req_id()
    subscribe_request = InstrumentsSubscribeRequest(
        method="subscribe",
        params={
            "channel": "instrument",
            "snapshot": True,
        },
        req_id=req_id,
    )

    logging.info("Sending instruments subscription message")
    logging.debug(subscribe_request.model_dump_json())
    await send_queue.put(subscribe_request.model_dump_json())


async def unsubscribe_from_instruments(send_queue):
    """
    Unsubscribes from the 'instrument' channel.
    """
    req_id = await get_unique_req_id()
    unsubscribe_request = InstrumentsUnsubscribeRequest(
        method="unsubscribe",
        params={
            "channel": "instrument",
        },
        req_id=req_id,
    )

    logging.info("Sending instruments unsubscription message")
    logging.debug(unsubscribe_request.model_dump_json())
    await send_queue.put(unsubscribe_request.model_dump_json())

async def subscribe_to_tickers(send_queue: asyncio.Queue, symbols: List[str]):
    """
    Subscribes to the 'ticker' channel for the specified symbols.
    """
    req_id = await get_unique_req_id()
    subscribe_request = TickerSubscribeRequest(
        method="subscribe",
        params={
            "channel": "ticker",
            "symbol": symbols,
            "event_trigger": "trades",  # or "bbo" based on your requirements
            "snapshot": True,
        },
        req_id=req_id,
    )

    logging.info("Sending ticker subscription message")
    logging.debug(subscribe_request.model_dump_json())
    await send_queue.put(subscribe_request.model_dump_json())


async def unsubscribe_from_tickers(send_queue: asyncio.Queue, symbols: List[str]):
    """
    Unsubscribes from the 'ticker' channel for the specified symbols.
    """
    req_id = await get_unique_req_id()
    unsubscribe_request = TickerUnsubscribeRequest(
        method="unsubscribe",
        params={
            "channel": "ticker",
            "symbol": symbols,
        },
        req_id=req_id,
    )

    logging.info("Sending ticker unsubscription message")
    logging.debug(unsubscribe_request.model_dump_json())
    await send_queue.put(unsubscribe_request.model_dump_json())