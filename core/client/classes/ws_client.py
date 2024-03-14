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
from typing import Any, Awaitable, Callable

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.classes.ws_client_session import WSClientSession
from core.dict.classes.dict_schema_context import DictSchemaContext
from core.log.classes.logger import Logger


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
        logger: Logger | None = None,
        logger_key: str | None = None,
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
    # │ EVENT LOOP TASK COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def event_loop_task_count(self) -> int:
        """Returns the number of tasks running in the event loop"""

        # Return event loop task count
        return sum(not task.done() for task in asyncio.all_tasks(loop=self.event_loop))

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
        connection_key: str | None = None,
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
                {
                    k: v(DictSchemaContext(data={})) if callable(v) else v
                    for k, v in (data or {}).items()
                }
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

        # Acquire websocket connection
        ws_connection = await self.session.acquire_connection(
            uri=uri, receive=receive, key=connection_key
        )

        # Subscribe to channel
        await ws_connection.subscribe(
            data_subscribe=data_subscribe,
            data_unsubscribe=data_unsubscribe,
            should_unsubscribe=should_unsubscribe,
        )

        # Listen to websocket connection
        await ws_connection.listen(event_loop=self.event_loop, listen_tolerance_ms=0)
