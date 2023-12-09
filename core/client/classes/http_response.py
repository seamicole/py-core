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
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

if TYPE_CHECKING:
    from core.client.types import JSONDict, JSONList, JSONValue


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
    # │ JSON DICT
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def json_dict(self) -> JSONDict:
        """Return the JSON response as a dictionary"""

        # Return JSON as dict
        return self.json if isinstance(self.json, dict) else {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ JSON LIST
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def json_list(self) -> JSONList:
        """Return the JSON response as a list"""

        # Return JSON as list
        return self.json if isinstance(self.json, list) else []

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ JSON VALUE
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def json_value(self) -> JSONValue:
        """Return the JSON response as a value"""

        # Return JSON as value
        return self.json if not isinstance(self.json, (dict, list)) else None

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
