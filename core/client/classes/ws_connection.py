# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import asyncio
import json
import ssl

try:
    import websockets
except ImportError:
    websockets = None  # type: ignore

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from websockets.legacy.client import WebSocketClientProtocol

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any, Awaitable, Callable

if TYPE_CHECKING:
    from core.client.classes.ws_client_session import WSClientSession

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ LITERALS
# └─────────────────────────────────────────────────────────────────────────────────────

WEBSOCKET_ERRORS = "websocket_errors"
WEBSOCKET_EVENTS = "websocket_events"


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ WS CONNECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class WSConnection:
    """A websocket connection utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of connection cache
    _conn: WebSocketClientProtocol | None

    # Declare type of subscriptions cache
    _subs: dict[str, tuple[str, Callable[[], bool] | None]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        uri: str,
        session: WSClientSession,
        receive: Callable[[str | bytes], Awaitable[None] | None],
        ping_data: str | dict[str, Any] | None = None,
        ping_interval_ms: int | None = 30000,
    ) -> None:
        """Init Method"""

        # Set URI
        self.uri = uri

        # Set session
        self.session = session

        # Set ping data and ping interval
        self.ping_data = ping_data
        self.ping_interval_ms = ping_interval_ms

        # Initialize thread lock
        self._tlock = asyncio.Lock()

        # Initialize connection cache
        self._conn = None

        # Initialize subscription cache
        self._subs = {}

        # Set receive task callback
        self._receive_task_callback = receive

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _LOG
    # └─────────────────────────────────────────────────────────────────────────────────

    def _log(self, message: str) -> str:
        """Generates a standardized log message"""

        # Get log prefix
        log_prefix = f"WSConn {self.id}"

        # Add log prefix to message
        message = f"{log_prefix}: {message}"

        # Return message
        return message

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ID
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def id(self) -> int:
        """Returns the ID of the websocket connection instance"""

        # Return websocket connection ID
        return id(self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PING DATA STR
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def ping_data_str(self) -> str | None:
        """Returns an evaluated string of the connection's ping data"""

        # Get ping data
        ping_data = self.ping_data

        # Return if ping data is None
        if ping_data is None:
            return None

        # Evaluate ping data if dictionary
        ping_data = (
            {k: v({}, {}) if callable(v) else v for k, v in ping_data.items()}
            if isinstance(ping_data, dict)
            else ping_data
        )

        # Ensure ping data is a string
        ping_data_str = (
            json.dumps(ping_data) if isinstance(ping_data, dict) else ping_data
        )

        # Return ping data string
        return ping_data_str

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
    # │ SUBSCRIPTION COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    async def subscription_count(self) -> int:
        """Returns the subscription count of the websocket the connection"""

        # Acquire lock
        async with self._tlock:
            # Return subscription count
            return len(self._subs)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ESTABLISH
    # └─────────────────────────────────────────────────────────────────────────────────

    async def establish(self) -> WebSocketClientProtocol:
        """Establishes a new websocket connection"""

        # Check if websockets is None
        if websockets is None:
            # Raise an ImportError
            raise ImportError("websockets is required to use this function")

        # Log message
        self.session.logger.debug(
            self._log(f"Connecting to {self.uri}"), key=WEBSOCKET_EVENTS
        )

        # Get context
        ctx = ssl.create_default_context()

        # Initialize try-except block
        try:
            # Create a new connection
            conn = await websockets.connect(self.uri, ssl=ctx, compression=None)

        # Handle any exception
        except Exception as e:
            # Log message
            self.session.logger.error(
                self._log(f"Error connecting to {self.uri}"),
                key=WEBSOCKET_ERRORS,
                exception=e,
            )
            raise

        # Return connection
        return conn

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LISTEN
    # └─────────────────────────────────────────────────────────────────────────────────

    async def listen(self, event_loop: asyncio.AbstractEventLoop | None = None) -> None:
        """Listens to the websocket connection"""

        # Get event loop
        event_loop = event_loop if event_loop is not None else asyncio.get_event_loop()

        # Initialize while loop
        while self.session.is_alive:
            # Acquire lock
            async with self._tlock:
                # Establish connection
                conn = await self.establish()

                # Cache connection
                self._conn = conn

                # Iterate over subscriptions
                for data_subscribe in self._subs:
                    # Send subscribe message
                    await self.send_subscribe(conn=conn, data=data_subscribe)

            # Receive data
            await self.receive(conn=conn, event_loop=event_loop)

            # Acquire lock
            async with self._tlock:
                # Check if connection is still open
                if not conn.closed:
                    # Iterate over keys
                    for key in list(self._subs):
                        # Get unsubscribe data
                        (data_unsubscribe, _) = self._subs[key]

                        # Send unsubscribe message
                        if self.send_unsubscribe(conn=conn, data=data_unsubscribe):
                            # Pop subscription from subscriptions
                            self._subs.pop(key)

                    # Log message
                    self.session.logger.debug(
                        self._log(f"Disconnecting from {self.uri}"),
                        key=WEBSOCKET_EVENTS,
                    )

                    # Initialize try-except block
                    try:
                        # Close connection
                        await asyncio.wait_for(conn.close(), timeout=10)

                    # Handle any exception
                    except Exception:
                        # Log message
                        self.session.logger.error(
                            self._log(f"Error disconnecting from {self.uri}"),
                            key=WEBSOCKET_ERRORS,
                        )

                # Set connection to None
                self._conn = None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ RECEIVE
    # └─────────────────────────────────────────────────────────────────────────────────

    async def receive(
        self, conn: WebSocketClientProtocol, event_loop: asyncio.AbstractEventLoop
    ) -> None:
        """Receives messages from a websocket connection"""

        # Initialize ping task
        ping_task = None

        # Check if ping data is not None
        if self.ping_data is not None:
            # Get ping interval
            ping_interval_s = self.ping_interval_s

            # Check if ping interval is not None
            if ping_interval_s is not None:
                # Define ping loop
                async def ping_loop() -> None:
                    # Initialize while loop
                    while not conn.closed and self.session.is_alive:
                        # Get ping data string
                        ping_data_str = self.ping_data_str

                        # Continue if None
                        if ping_data_str is None:
                            continue

                        # Send ping
                        await conn.send(ping_data_str)

                        # Wait for ping interval
                        await asyncio.sleep(ping_interval_s)

                # Create ping task
                ping_task = asyncio.create_task(ping_loop())

        # Define receive loop
        async def receive_loop() -> None:
            # Initialize while loop
            while not conn.closed and self.session.is_alive:
                # Initialize try-except block
                try:
                    # Receive message
                    message = await conn.recv()

                # Handle case of connection error
                except websockets.exceptions.ConnectionClosedError as e:
                    # Log message
                    self.session.logger.error(
                        self._log(f"Connection interrupted: {self.uri}"),
                        key=WEBSOCKET_ERRORS,
                        exception=e,
                    )
                    return

                # Handle case of coroutine function
                if asyncio.iscoroutinefunction(self._receive_task_callback):
                    await self._receive_task_callback(message)

                # Handle case of normal function
                else:
                    self._receive_task_callback(message)

        # Create receive task
        receive_task = event_loop.create_task(receive_loop())

        # Initialize while loop
        while self.session.is_alive:
            # Return if receive task is done
            if receive_task.done():
                return

            # Iterate over keys
            for key in list(self._subs):
                # Get unsubscribe data
                (data_unsubscribe, should_unsubscribe) = self._subs[key]

                # Continue if should not unsubscribe
                if should_unsubscribe is None or not should_unsubscribe():
                    continue

                # Acquire lock
                async with self._tlock:
                    # Check if connection is still open
                    if not conn.closed:
                        # Send unsubscribe message
                        if self.send_unsubscribe(conn=conn, data=data_unsubscribe):
                            # Pop subscription from subscriptions
                            self._subs.pop(key)

            # Sleep for n seconds
            await asyncio.sleep(self.session.sync_tolerance_s)

        # Cancel receive task
        receive_task.cancel()

        # Cancel ping task
        ping_task and ping_task.cancel()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SEND
    # └─────────────────────────────────────────────────────────────────────────────────

    async def send(
        self,
        conn: WebSocketClientProtocol,
        data: str,
        info_message: str,
        error_message: str,
    ) -> bool:
        """Sends a message to the open connection"""

        # Initialize try-except block
        try:
            # Get log message
            log_message = self._log(info_message)

            # Append data to message
            log_message = f"{log_message}\n\n\t{data}"

            # Log message
            self.session.logger.debug(self._log(log_message), key=WEBSOCKET_EVENTS)

            # Send subscribe data
            await conn.send(data)

        # Handle any exception
        except Exception:
            # Get log message
            log_message = self._log(error_message)

            # Append data to message
            log_message = f"{log_message}\n\n\t{data}"

            # Log message
            self.session.logger.error(log_message, key=WEBSOCKET_ERRORS)

            # Return False
            return False

        # Return True
        return True

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SEND SUBSCRIBE
    # └─────────────────────────────────────────────────────────────────────────────────

    async def send_subscribe(self, conn: WebSocketClientProtocol, data: str) -> bool:
        """Sends a subscribe message to the open connection"""

        # Set subscribe data to connection
        return await self.send(
            conn=conn,
            data=data,
            info_message=f"Subscribing to channel at {self.uri}",
            error_message=f"Error subscribing to channel at {self.uri}",
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SEND UNSUBSCRIBE
    # └─────────────────────────────────────────────────────────────────────────────────

    async def send_unsubscribe(self, conn: WebSocketClientProtocol, data: str) -> bool:
        """Sends an unsubscribe message to the open connection"""

        # Set subscribe data to connection
        return await self.send(
            conn=conn,
            data=data,
            info_message=f"Unsubscribing to channel at {self.uri}",
            error_message=f"Error unsubscribing to channel at {self.uri}",
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SUBSCRIBE
    # └─────────────────────────────────────────────────────────────────────────────────

    async def subscribe(
        self,
        data_subscribe: str,
        data_unsubscribe: str,
        should_unsubscribe: Callable[[], bool] | None = None,
    ) -> None:
        """Subscribes to a websocket channel in the websocket connection listen loop"""

        # Acquire lock
        async with self._tlock:
            # Return if already subscribed
            if data_subscribe in self._subs:
                return

            # Add to subscriptions
            self._subs[data_subscribe] = (data_unsubscribe, should_unsubscribe)

        # Add subscription to active connection
        if self._conn is not None and not self._conn.closed:
            # Send subscribe message
            await self.send_subscribe(conn=self._conn, data=data_subscribe)
