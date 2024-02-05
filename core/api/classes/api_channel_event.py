# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

if TYPE_CHECKING:
    from core.api.classes.api_channel import APIChannel
    from core.client.types import JSONSchema


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ API CHANNEL EVENT
# └─────────────────────────────────────────────────────────────────────────────────────


class APIChannelEvent:
    """An API channel event utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        channel: APIChannel,
        key: str,
        data: str | dict[Any, Any],
        json_path: str | None = None,
        json_schema: JSONSchema | None = None,
    ) -> None:
        """Init Method"""

        # Set key
        self.key = key

        # Set channel
        self.channel = channel

        # Set data
        self.data = data

        # Set JSON path
        self.json_path = json_path

        # Set JSON schema
        self.json_schema = json_schema

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        """Representation Method"""

        # Return representation
        return f"<{self.__class__.__name__}: {self.channel.api.ws_uri}: {self.key}>"
