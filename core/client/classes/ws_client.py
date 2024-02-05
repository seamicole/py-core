# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import asyncio
import json

try:
    import websockets
except ImportError:
    websockets = None  # type: ignore

from multiprocessing.managers import SyncManager
from typing import Any, Awaitable, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from websockets.legacy.client import WebSocketClientProtocol

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.classes.ws_client_session import WSClientSession


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ WS CLIENT
# └─────────────────────────────────────────────────────────────────────────────────────


class WSClient:
    """A websocket client utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        manager: SyncManager | None = None,
    ) -> None:
        """Init Method"""

        # Initialize websocket client session
        self.session = WSClientSession(manager=manager)

        # Initialize websocket event loop
        self.event_loop = asyncio.get_event_loop()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LISTEN
    # └─────────────────────────────────────────────────────────────────────────────────

    async def listen(
        self,
        conn: WebSocketClientProtocol,
        callback: Callable[[str | bytes], Awaitable[None] | None],
    ) -> None:
        """Listens to a websocket connection"""

        # Initialize while loop
        while self.session.is_alive:
            # Receive message
            message = await conn.recv()

            # Handle case of coroutine function
            if asyncio.iscoroutinefunction(callback):
                await callback(message)

            # Handle case of normal function
            else:
                callback(message)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SUBSCRIBE
    # └─────────────────────────────────────────────────────────────────────────────────

    async def subscribe(
        self,
        uri: str,
        data_subscribe: str | dict[Any, Any],
        data_unsubscribe: str | dict[Any, Any],
        callback: Callable[[str | bytes], Awaitable[None] | None],
    ) -> None:
        """Subscribes to a websocket connection and listens for messages"""

        # Check if websockets is None
        if websockets is None:
            # Raise an ImportError
            raise ImportError("websockets is required to use this function")

        # Ensure data is a string
        data_subscribe, data_unsubscribe = (
            json.dumps(data) if isinstance(data, dict) else data
            for data in (data_subscribe, data_unsubscribe)
        )

        # Initialize while loop
        while self.session.is_alive:
            # Acquire connection
            conn = await self.session.acquire_connection(uri)

            # Send subscribe data
            await conn.send(data_subscribe)

            # Listen to connection
            await self.listen(conn, callback)

            # Send unsubscribe data
            await conn.send(data_unsubscribe)

            # Release connection
            await self.session.release_connection(uri, conn)
