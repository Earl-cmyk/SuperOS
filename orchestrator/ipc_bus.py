# orchestrator/ipc_bus.py
#
# IPC Bus
#
# Central asynchronous publish/subscribe message bus.
# This is the ONLY communication spine between UI, services, and kernel.
# No direct calls. No shared state. No shortcuts.

import asyncio
from collections import defaultdict
from typing import Any, Awaitable, Callable, Dict, List
from loguru import logger

MessageHandler = Callable[[Any], Awaitable[None]]


class IPCBus:
    def __init__(self):
        self._subscribers: Dict[str, List[MessageHandler]] = defaultdict(list)
        self._queue: asyncio.Queue[tuple[str, Any]] = asyncio.Queue()
        self._running: bool = False

    # -------------------------
    # Subscription API
    # -------------------------

    def subscribe(self, channel: str, handler: MessageHandler):
        logger.debug(f"IPC subscribe: {channel} -> {handler.__name__}")
        self._subscribers[channel].append(handler)

    # -------------------------
    # Publish API
    # -------------------------

    async def publish(self, channel: str, payload: Any):
        if not self._running:
            logger.warning("IPC publish while bus not running")
        await self._queue.put((channel, payload))

    # -------------------------
    # Event Loop
    # -------------------------

    async def run(self):
        self._running = True
        logger.info("IPC bus online")

        while self._running:
            channel, payload = await self._queue.get()
            handlers = self._subscribers.get(channel, [])

            if not handlers:
                logger.debug(f"IPC drop (no subscribers): {channel}")
                continue

            for handler in handlers:
                try:
                    await handler(payload)
                except Exception as e:
                    logger.exception(
                        f"IPC handler error on channel '{channel}': {e}"
                    )

    # -------------------------
    # Shutdown
    # -------------------------

    def stop(self):
        logger.info("IPC bus shutting down")
        self._running = False
