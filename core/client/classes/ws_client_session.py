# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

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

    def __init__(self, manager: SyncManager | None = None) -> None:
        """Init Method"""

        # Initialize a manager
        self._manager = manager or Manager()

        # Initialize lock
        self._lock = self._manager.Lock()

        # Initialize connections
        self._connections = {}

        # Initialize is alive
        self._is_alive = self._manager.Value("b", True)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ IS ALIVE
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def is_alive(self) -> bool:
        """Get is alive"""

        # Get is alive
        with self._lock:
            return self._is_alive.value

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

        # Get context
        ctx = ssl.create_default_context()

        # Create a new connection
        connection = await websockets.connect(uri, ssl=ctx, compression=None)

        # Add connection to connections
        connections[connection] = 1

        # Return connection
        return connection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ KILL
    # └─────────────────────────────────────────────────────────────────────────────────

    async def kill(self) -> None:
        """Kills the websocket client session"""

        # Acquire lock
        with self._lock:
            # Set is alive to false
            self._is_alive.value = False

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
                # Close connection
                await connection.close()

                # Remove connection
                del connections[connection]

            # Decrement channel count
            else:
                connections[connection] -= 1
