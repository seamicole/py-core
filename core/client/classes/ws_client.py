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
        ping_data: str | dict[str, Any] | None = None,
        ping_interval_ms: int | None = 30000,
        sync_tolerance_ms: int = 2000,
    ) -> None:
        """Init Method"""

        # Initialize websocket client session
        self.session = WSClientSession(
            manager=manager,
            ping_data=ping_data,
            ping_interval_ms=ping_interval_ms,
            sync_tolerance_ms=sync_tolerance_ms,
        )

        # Initialize websocket event loop
        self.event_loop = asyncio.get_event_loop()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LISTEN
    # └─────────────────────────────────────────────────────────────────────────────────

    async def listen(
        self,
        uri: str,
        data_subscribe: str | dict[Any, Any],
        data_unsubscribe: str | dict[Any, Any],
        receive: Callable[[str | bytes], Awaitable[None] | None],
        should_unsubscribe: Callable[[], bool] = lambda: False,
    ) -> None:
        """Listens to a websocket connection"""

        # Initialize while loop
        while self.session.is_alive and not should_unsubscribe():
            # Acquire connection
            conn = await self.session.acquire_connection(uri)

            # Send subscribe data
            await conn.send(data_subscribe)

            # Receive data
            await self.receive(conn, receive, should_unsubscribe)

            # Check if connection is still open
            if not conn.closed:
                # Send unsubscribe data
                await conn.send(data_unsubscribe)

            # Release connection
            await self.session.release_connection(uri, conn)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ RECEIVE
    # └─────────────────────────────────────────────────────────────────────────────────

    async def receive(
        self,
        conn: WebSocketClientProtocol,
        receive: Callable[[str | bytes], Awaitable[None] | None],
        should_unsubscribe: Callable[[], bool],
    ) -> None:
        """Receives messages from a websocket connection"""

        # Define receive loop
        async def receive_loop() -> None:
            # Initialize while loop
            while (
                not conn.closed and self.session.is_alive and not should_unsubscribe()
            ):
                # Initialize try-except block
                try:
                    # Receive message
                    message = await conn.recv()

                # Handle case of connection error
                except websockets.exceptions.ConnectionClosedError:
                    return

                # Handle case of coroutine function
                if asyncio.iscoroutinefunction(receive):
                    await receive(message)

                # Handle case of normal function
                else:
                    receive(message)

        # Create receive task
        receive_task = self.event_loop.create_task(receive_loop())

        # Initialize while loop
        while self.session.is_alive and not should_unsubscribe():
            # Return if receive task is done
            if receive_task.done():
                return

            # Sleep for 1 second
            await asyncio.sleep(self.session.sync_tolerance_s)

        # Cancel receive task
        receive_task.cancel()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SUBSCRIBE
    # └─────────────────────────────────────────────────────────────────────────────────

    async def subscribe(
        self,
        uri: str,
        data_subscribe: str | dict[Any, Any],
        data_unsubscribe: str | dict[Any, Any],
        receive: Callable[[str | bytes], Awaitable[None] | None],
        should_unsubscribe: Callable[[], bool] = lambda: False,
    ) -> None:
        """Subscribes to a websocket connection and listens for messages"""

        # Check if websockets is None
        if websockets is None:
            # Raise an ImportError
            raise ImportError("websockets is required to use this function")

        # Start session
        self.session.start()

        # Evaluate data if dictionary
        data_subscribe, data_unsubscribe = (
            json.dumps(
                {k: v({}, {}) if callable(v) else v for k, v in (data or {}).items()}
            )
            if isinstance(data, dict)
            else data
            for data in (data_subscribe, data_unsubscribe)
        )

        # Ensure data is a string
        data_subscribe, data_unsubscribe = (
            json.dumps(data) if isinstance(data, dict) else data
            for data in (data_subscribe, data_unsubscribe)
        )

        # Create listen task
        self.event_loop.create_task(
            self.listen(
                uri,
                data_subscribe,
                data_unsubscribe,
                receive,
                should_unsubscribe,
            )
        )
