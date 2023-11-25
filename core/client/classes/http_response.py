# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from aiohttp import ClientResponse as AioHTTPResponse
    from httpx import Response as HTTPXResponse
    from requests import Response as RequestsResponse


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP RESPONSE
# └─────────────────────────────────────────────────────────────────────────────────────


class HTTPResponse:
    """An HTTP response utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of obj
    _obj: AioHTTPResponse | HTTPXResponse | RequestsResponse

    # Declare type of JSON
    json: dict[str, Any] | None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        obj: AioHTTPResponse | HTTPXResponse | RequestsResponse,
        json: dict[str, Any] | None,
    ) -> None:
        """Init Method"""

        # Set obj
        self._obj = obj

        # Set JSON
        self.json = json

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ STATUS CODE
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def status_code(self) -> int:
        """Return the response object status code"""

        # Check if response object is AioHTTP
        if hasattr(self._obj, "status"):
            return self._obj.status

        # Return status code
        return self._obj.status_code
