# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, Callable, TYPE_CHECKING

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
        callback: Callable[[str | bytes], None],
        data: str | dict[Any, Any] | None = None,
    ) -> None:
        """Subscribes to an API channel"""

        # Get subscribe event
        event = self.events["subscribe"]

        # Subscribe to channel
        await self.api.ws.subscribe(
            uri=self.api.ws_uri,
            data=data if data is not None else event.data,
            callback=callback,
        )
