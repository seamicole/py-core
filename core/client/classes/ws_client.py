# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import json
import ssl

try:
    import websockets
except ImportError:
    websockets = None  # type: ignore

from multiprocessing.managers import SyncManager
from typing import Any, Awaitable, Callable
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

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LISTEN
    # └─────────────────────────────────────────────────────────────────────────────────

    async def listen(
        self,
        conn: WebSocketClientProtocol,
        callback: Callable[[str | bytes], Awaitable[None]],
    ) -> None:
        """Listens to a websocket connection"""

        # Initialize while loop
        while True:
            # Receive message
            message = await conn.recv()

            # Invoke callback
            await callback(message)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SUBSCRIBE
    # └─────────────────────────────────────────────────────────────────────────────────

    async def subscribe(
        self,
        uri: str,
        data: str | dict[Any, Any],
        callback: Callable[[str | bytes], Awaitable[None]],
    ) -> None:
        """Subscribes to a websocket connection and listens for messages"""

        # Check if websockets is None
        if websockets is None:
            # Raise an ImportError
            raise ImportError("websockets is required to use this function")

        # Ensure data is a string
        if isinstance(data, dict):
            data = json.dumps(data)

        # Initialize while loop
        while True:
            # Get context
            ctx = ssl.create_default_context()

            # Initialize websocket connection
            async with websockets.connect(uri, ssl=ctx, compression=None) as conn:
                # Send subscription message
                await conn.send(data)

                # Listen to connection
                await self.listen(conn, callback)
