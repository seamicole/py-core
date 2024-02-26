# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import asyncio
import time
import ssl

from multiprocessing import Manager
from multiprocessing.managers import SyncManager
from typing import TYPE_CHECKING

try:
    import websockets
except ImportError:
    websockets = None  # type: ignore

if TYPE_CHECKING:
    from websockets.legacy.client import WebSocketClientProtocol


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ WS CLIENT SESSION
# └─────────────────────────────────────────────────────────────────────────────────────


class WSClientSession:
    """An websocket client session utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of connections
    _connections: dict[str, dict[WebSocketClientProtocol, int]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        manager: SyncManager | None = None,
        ping_interval_ms: int | None = 30000,
        sync_tolerance_ms: int = 2000,
    ) -> None:
        """Init Method"""

        # Initialize a manager
        self._manager = manager or Manager()

        # Initialize lock
        self._lock = self._manager.Lock()

        # Initialize connections
        self._connections = {}

        # Initialize is alive
        self._is_alive = self._manager.Value("b", False)
        self._is_alive_cache = False
        self._is_alive_updated_at = time.time()

        # Initialize connection ID and connection count
        self._connection_id = self._manager.Value("i", 0)  # Not used yet
        self._connection_count = self._manager.Value("i", 0)

        # Set ping interval
        self.ping_interval_ms = ping_interval_ms

        # Set sync tolerance
        self.sync_tolerance_ms = sync_tolerance_ms

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
        with self._lock:
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
        with self._lock:
            self._connection_count.value -= 1

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _GET CONNECTION ID
    # └─────────────────────────────────────────────────────────────────────────────────

    def _get_connection_id(self) -> int:
        """Get connection ID"""

        # Get connection ID
        with self._lock:
            # Get connection ID
            connection_id = self._connection_id.value

            # Increment connection ID
            self._connection_id.value += 1

            # Return connection ID
            return connection_id

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _INCREMENT CONNECTION COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    def _increment_connection_count(self) -> None:
        """Increment connection count"""

        # Increment connection count
        with self._lock:
            self._connection_count.value += 1

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ACQUIRE CONNECTION
    # └─────────────────────────────────────────────────────────────────────────────────

    async def acquire_connection(
        self, uri: str, max_channels: int | None = None
    ) -> WebSocketClientProtocol:
        """Acquires a free or newly initialized websocket connection"""

        # Acquire lock
        with self._lock:
            # Get connections
            connections = self._connections.setdefault(uri, {})

            # Iterate over connections
            for connection, channel_count in connections.items():
                # If max channels is none or channel count is less than max channels
                if max_channels is None or channel_count < max_channels:
                    # Increment channel count and return
                    connections[connection] += 1

                    # Return connection
                    return connection

        # Increment connection count
        self._increment_connection_count()

        # Get context
        ctx = ssl.create_default_context()

        # Create a new connection
        connection = await websockets.connect(uri, ssl=ctx, compression=None)

        # Add connection to connections
        connections[connection] = 1

        # Get ping interval
        ping_interval_s = self.ping_interval_s

        # Check if ping interval is not None
        if ping_interval_s is not None:
            # Define ping loop
            async def ping_loop() -> None:
                # Initialize while loop
                while not connection.closed:
                    # Send ping
                    # await connection.ping()
                    print("PING!")

                    # Wait for ping interval
                    await asyncio.sleep(ping_interval_s)

            # Create ping task
            asyncio.create_task(ping_loop())

        # Return connection
        return connection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ RELEASE CONNECTION
    # └─────────────────────────────────────────────────────────────────────────────────

    async def release_connection(
        self, uri: str, connection: WebSocketClientProtocol
    ) -> None:
        """Releases an acquired websocket connection"""

        # Acquire lock
        with self._lock:
            # Get connections
            connections = self._connections.get(uri)

            # Return if no connections
            if connections is None or connection not in connections:
                return

        # Check if channel count is 1
        if connections[connection] <= 1:
            # Check if connection is still open
            if not connection.closed:
                # Initialize try-except block
                try:
                    # Close connection
                    await asyncio.wait_for(connection.close(), timeout=10)

                # Handle any exception
                except Exception:
                    pass

            # Remove connection
            del connections[connection]

            # Decrement connection count
            self._decrement_connection_count()

        # Decrement channel count
        else:
            connections[connection] -= 1

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ START
    # └─────────────────────────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Starts the websocket client session"""

        # Acquire lock
        with self._lock:
            # Set is alive to true
            self._is_alive.value = True

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ STOP
    # └─────────────────────────────────────────────────────────────────────────────────

    def stop(self) -> None:
        """Stops the websocket client session"""

        # Acquire lock
        with self._lock:
            # Set is alive to false
            self._is_alive.value = False
