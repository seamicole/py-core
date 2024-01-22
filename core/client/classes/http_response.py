# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, Generator, TYPE_CHECKING

if TYPE_CHECKING:
    from aiohttp import ClientResponse as AioHTTPResponse
    from httpx import Response as HTTPXResponse
    from requests import Response as RequestsResponse

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.types import JSONSchema
from core.dict.functions.dget import dget
from core.dict.functions.dfrom_schema import dfrom_schema

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

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ YIELD DICTS
    # └─────────────────────────────────────────────────────────────────────────────────

    def yield_dicts(
        self, json_path: str | None = None, json_schema: JSONSchema | None = None
    ) -> Generator[JSONDict, None, None]:
        """Yields a series of dicts from the response"""

        # Get response JSON
        response_json = self.json

        # Continue if response JSON is None
        if response_json is None:
            return None

        # Set items to response JSON
        items = response_json

        # Check if JSON path is not None
        if json_path is not None and isinstance(response_json, dict):
            # Set items to JSON path
            items = dget(response_json, json_path)

        # Continue if items is not a list
        if not isinstance(items, list):
            return

        # Iterate over itmes
        for item in items:
            # Yield item
            yield dfrom_schema(
                item, schema=json_schema, delimiter="."
            ) if json_schema is not None else item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ YIELD INSTANCES
    # └─────────────────────────────────────────────────────────────────────────────────

    def yield_instances(
        self,
        InstanceClass: type,
        json_path: str | None = None,
        json_schema: JSONSchema | None = None,
    ) -> Generator[Any, None, None]:
        """Yields a series of instances from the response"""

        # Iterate over dicts
        for item in self.yield_dicts(json_path=json_path, json_schema=json_schema):
            # Initialize and yield instance
            yield InstanceClass(**item)
