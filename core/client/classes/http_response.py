# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import re

from typing import Any, Generator, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from aiohttp import ClientResponse as AioHTTPResponse
    from httpx import Response as HTTPXResponse
    from requests import Response as RequestsResponse

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.types import JSONSchema
from core.dict.classes.dict_schema_context import DictSchemaContext
from core.dict.functions.dget import dget
from core.dict.functions.dfrom_schema import dfrom_schema

if TYPE_CHECKING:
    from core.client.classes.http_request import HTTPRequest
    from core.client.types import JSONDict, JSONFilter, JSONList, JSONValue

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TYPE VARIABLES
# └─────────────────────────────────────────────────────────────────────────────────────

T = TypeVar("T")


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

    # Declare type of text
    text: str | None

    # Declare type of JSON
    json: dict[str, Any] | None

    # Declare type of weight
    weight: int

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        request: HTTPRequest,
        obj: AioHTTPResponse | HTTPXResponse | RequestsResponse,
        text: str | None,
        json: dict[str, Any] | None,
        weight: int = 1,
    ) -> None:
        """Init Method"""

        # Set request
        self.request = request

        # Set obj
        self._obj = obj

        # Set text
        self.text = text

        # Set JSON
        self.json = json

        # Set weight
        self.weight = weight

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ DID SUCCEED
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def did_succeed(self) -> bool:
        """Returns a boolean of whether the response had a successful status code"""

        # Return did succeed
        return 200 <= self.status_code < 300

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
    # │ TEXT STRIPPED
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def text_stripped(self) -> str | None:
        """Returns the response string stripped of HTML"""

        # Return if text is None
        if self.text is None:
            return None

        # Return stripped text
        return re.sub(r"<[^>]+>", "", self.text)

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
    # │ DICT
    # └─────────────────────────────────────────────────────────────────────────────────

    def dict(
        self, json_path: str | None = None, json_schema: JSONSchema | None = None
    ) -> JSONDict | None:
        """Yields a series of dicts from the response"""

        # Get response JSON
        response_json = self.json

        # Continue if response JSON is None
        if response_json is None:
            return None

        # Set item to response JSON
        item = response_json

        # Check if JSON path is not None
        if json_path is not None and isinstance(response_json, dict):
            # Set item to JSON path
            item = dget(response_json, json_path)

        # Continue if item is not a list
        if not isinstance(item, dict):
            return

        # Return item
        return (
            dfrom_schema(item, schema=json_schema, delimiter=".")
            if json_schema is not None
            else item
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ DICTS
    # └─────────────────────────────────────────────────────────────────────────────────

    def dicts(
        self,
        json_path: str | None = None,
        json_filter: JSONFilter | None = None,
        json_schema: JSONSchema | None = None,
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
            # Continue if item is not a dict
            if not isinstance(item, dict):
                continue

            # Continue if item should be filtered
            if json_filter and not json_filter(
                DictSchemaContext(data=response_json, item=item)
            ):
                continue

            # Yield item
            yield dfrom_schema(
                item, schema=json_schema, delimiter="."
            ) if json_schema is not None else item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE
    # └─────────────────────────────────────────────────────────────────────────────────

    def instance(
        self,
        InstanceClass: type[T],
        json_path: str | None = None,
        json_schema: JSONSchema | None = None,
    ) -> T | None:
        """Yields a series of instances from the response"""

        # Get item
        item = self.dict(json_path=json_path, json_schema=json_schema)

        # Return if item is None
        if item is None:
            return None

        # Initialize and return instance
        return InstanceClass(**item)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCES
    # └─────────────────────────────────────────────────────────────────────────────────

    def instances(
        self,
        InstanceClass: type[T],
        json_path: str | None = None,
        json_filter: JSONFilter | None = None,
        json_schema: JSONSchema | None = None,
    ) -> Generator[T, None, None]:
        """Yields a series of instances from the response"""

        # Iterate over dicts
        for item in self.dicts(
            json_path=json_path,
            json_filter=json_filter,
            json_schema=json_schema,
        ):
            # Initialize and yield instance
            yield InstanceClass(**item)
