# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import asyncio
import time

from multiprocessing import Manager
from multiprocessing.managers import SyncManager
from typing import Any, Awaitable, Callable

try:
    import websockets
except ImportError:
    websockets = None  # type: ignore

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.classes.ws_connection import WSConnection
from core.log.classes.logger import Logger


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ WS CLIENT SESSION
# └─────────────────────────────────────────────────────────────────────────────────────


class WSClientSession:
    """An websocket client session utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of connections
    _connections: dict[str, set[WSConnection]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        manager: SyncManager | None = None,
        ping_data: str | dict[str, Any] | None = None,
        ping_interval_ms: int | None = 30000,
        sync_tolerance_ms: int = 2000,
        logger: Logger | None = None,
        logger_key: str | None = None,
    ) -> None:
        """Init Method"""

        # Initialize a manager
        self._manager = manager or Manager()

        # Initialize process and thread locks
        self._plock = self._manager.Lock()
        self._tlock = asyncio.Lock()

        # Initialize connections
        self._connections = {}

        # Initialize is alive
        self._is_alive = self._manager.Value("b", False)
        self._is_alive_cache = False
        self._is_alive_updated_at = time.time()

        # Initialize connection count
        self._connection_count = self._manager.Value("i", 0)

        # Set ping data
        self.ping_data = ping_data

        # Set ping interval
        self.ping_interval_ms = ping_interval_ms

        # Set sync tolerance
        self.sync_tolerance_ms = sync_tolerance_ms

        # Initialize logger
        self.logger = (
            logger
            if logger is not None
            else Logger(
                key=logger_key
                if logger_key
                else f"{self.__class__.__name__}.{hex(id(self))}",
                log_limit=1000,
            )
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ IS ALIVE
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def is_alive(self) -> bool:
        """Get is alive"""

        # Check if cache is still valid
        if time.time() - self._is_alive_updated_at < self.sync_tolerance_s:
            return self._is_alive_cache

        # Get is alive
        with self._plock:
            self._is_alive_cache = self._is_alive.value
            self._is_alive_updated_at = time.time()

        # Return is alive cache
        return self._is_alive_cache

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PING INTERVAL S
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def ping_interval_s(self) -> float | None:
        """Get ping interval in seconds"""

        # Return if ping interval is None
        if self.ping_interval_ms is None:
            return None

        # Return ping interval in seconds
        return self.ping_interval_ms / 1000

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SYNC TOLERANCE S
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def sync_tolerance_s(self) -> float:
        """Get sync tolerance in seconds"""

        # Return sync tolerance in seconds
        return self.sync_tolerance_ms / 1000

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _DECREMENT CONNECTION COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    def _decrement_connection_count(self) -> None:
        """Decrement connection count"""

        # Decrement connection count
        with self._plock:
            self._connection_count.value -= 1

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _INCREMENT CONNECTION COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    def _increment_connection_count(self) -> None:
        """Increment connection count"""

        # Increment connection count
        with self._plock:
            self._connection_count.value += 1

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ACQUIRE CONNECTION
    # └─────────────────────────────────────────────────────────────────────────────────

    async def acquire_connection(
        self,
        uri: str,
        receive: Callable[[str | bytes], Awaitable[None] | None],
        key: str | None = None,
    ) -> WSConnection:
        """Acquires a free or newly initialized websocket connection"""

        # Get subscriptions per connection
        subscriptions_per_connection = 20

        # Acquire lock
        async with self._tlock:
            # Initialize connections
            connections = None

            # Check if key is not None
            if key is not None:
                # Get connections
                connections = self._connections.setdefault(key, set())

                # Iterate over connections
                for connection in connections:
                    # Check if subscriptions per connection does not exceed the maximum
                    if (
                        subscriptions_per_connection is None
                        or (await connection.subscription_count)
                        < subscriptions_per_connection
                    ):
                        # Return connection
                        return connection

            # Increment connection count
            self._increment_connection_count()

            # Create a new connection
            connection = WSConnection(uri=uri, session=self, receive=receive)

            # Add connection to connections
            if connections is not None:
                connections.add(connection)

        # Return connection
        return connection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ RELEASE CONNECTION
    # └─────────────────────────────────────────────────────────────────────────────────

    async def release_connection(self, connection: WSConnection) -> None:
        """Releases an acquired websocket connection"""

        # Initialize is found
        is_found = False

        # Acquire lock
        async with self._tlock:
            # Iterate over connections
            for key, connections in self._connections.items():
                # Continue if connection not in connections
                if connection not in connections:
                    continue

                # Check if connection is still open
                if connection._conn is not None and not connection._conn.closed:
                    # Initialize try-except block
                    try:
                        # Close connection
                        await asyncio.wait_for(connection._conn.close(), timeout=30)

                    # Handle any exception
                    except Exception:
                        pass

                # Discard connection
                connections.discard(connection)

                # Set is found
                is_found = True

        # Check if found
        if is_found:
            # Decrement connection count
            self._decrement_connection_count()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ START
    # └─────────────────────────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Starts the websocket client session"""

        # Acquire lock
        with self._plock:
            # Set is alive to true
            self._is_alive.value = True

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ STOP
    # └─────────────────────────────────────────────────────────────────────────────────

    def stop(self) -> None:
        """Stops the websocket client session"""

        # Acquire lock
        with self._plock:
            # Set is alive to false
            self._is_alive.value = False
