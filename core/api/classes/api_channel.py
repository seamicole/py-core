# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, Awaitable, Callable, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.api.classes.api_channel_event_collection import APIChannelEventCollection

if TYPE_CHECKING:
    from core.api.classes.api import API


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ API CHANNEL
# └─────────────────────────────────────────────────────────────────────────────────────


class APIChannel:
    """An API channel utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, api: API) -> None:
        """Init Method"""

        # Set API
        self.api = api

        # Initialize events
        self.events = APIChannelEventCollection(keys=("key",))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        """Representation Method"""

        # Return representation
        return f"<{self.__class__.__name__}: {self.api.ws_uri}>"

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SUBSCRIBE
    # └─────────────────────────────────────────────────────────────────────────────────

    async def subscribe(
        self,
        receive: Callable[[str | bytes], Awaitable[None] | None],
        data_subscribe: str | dict[Any, Any] | None = None,
        data_unsubscribe: str | dict[Any, Any] | None = None,
        should_unsubscribe: Callable[[], bool] = lambda: False,
        connection_key: str | None = None,
    ) -> None:
        """Subscribes to an API channel"""

        # Subscribe to channel
        await self.api.ws.subscribe(
            uri=self.api.ws_uri,
            data_subscribe=(
                data_subscribe
                if data_subscribe is not None
                else self.events["subscribe"].data
            ),
            data_unsubscribe=(
                data_unsubscribe
                if data_unsubscribe is not None
                else self.events["unsubscribe"].data
            ),
            receive=receive,
            should_unsubscribe=should_unsubscribe,
            connection_key=connection_key,
        )
