# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, AsyncGenerator, Generator, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.types import HTTPMethod
from core.placeholders import nothing
from core.placeholders.types import Nothing

if TYPE_CHECKING:
    from core.api.classes.api import API
    from core.client.classes.http_response import HTTPResponse
    from core.client.types import HTTPMethodLiteral, JSONDict, JSONSchema


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ API ENDPOINT
# └─────────────────────────────────────────────────────────────────────────────────────


class APIEndpoint:
    """An API endpoint utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        api: API,
        path: str,
        method: HTTPMethod | HTTPMethodLiteral | None = None,
        base_url: str | None = None,
        json_path: str | None = None,
        json_schema: JSONSchema | None = None,
    ) -> None:
        """Init Method"""

        # Set API
        self.api = api

        # Set path
        self.path = path

        # Check if method is a string
        if isinstance(method, str):
            # Convert to HTTPMethod
            method = HTTPMethod[method.upper()]

        # Set method
        self.method = method

        # Set base URL
        self.base_url = base_url

        # Set JSON path
        self.json_path = json_path

        # Set JSON schema
        self.json_schema = json_schema

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ URL
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def url(self) -> str:
        """Constructs and returns the API endpoint URL"""

        # Construct and return URL
        return self.api.construct_url(self.path, base_url=self.base_url)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST
    # └─────────────────────────────────────────────────────────────────────────────────

    def request(self) -> HTTPResponse:
        """Makes a synchronous request to the API endpoint"""

        # Make request and return response
        return self.api.request(
            self.method or HTTPMethod.GET,
            self.path,
            base_url=self.base_url,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_async(self) -> HTTPResponse:
        """Makes an asynchronous request to the API endpoint"""

        # Make request and return response
        return await self.api.request_async(
            self.method or HTTPMethod.GET,
            self.path,
            base_url=self.base_url,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST DICTS
    # └─────────────────────────────────────────────────────────────────────────────────

    def request_dicts(
        self,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
    ) -> Generator[JSONDict, None, None]:
        """Yields a series of object dicts from the current API endpoint"""

        # Make request
        response = self.request()

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Iterate over items
        for item in response.yield_dicts(json_path=json_path, json_schema=json_schema):
            yield item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST DICTS ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_dicts_async(
        self,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
    ) -> AsyncGenerator[JSONDict, None]:
        """Yields a series of object dicts from the current API endpoint"""

        # Make request
        response = await self.request_async()

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Iterate over items
        for item in response.yield_dicts(json_path=json_path, json_schema=json_schema):
            yield item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST INSTANCES
    # └─────────────────────────────────────────────────────────────────────────────────

    def request_instances(
        self,
        InstanceClass: type,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
    ) -> Generator[Any, None, None]:
        """Yields a series of object instances from the current API endpoint"""

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Iterate over items
        for item in self.request_dicts(json_path=json_path, json_schema=json_schema):
            # Initialize and yield instance
            yield InstanceClass(**item)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST INSTANCES ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_instances_async(
        self,
        InstanceClass: type,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
    ) -> AsyncGenerator[Any, None]:
        """Yields a series of object instances from the current API endpoint"""

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Iterate over items
        async for item in self.request_dicts_async(
            json_path=json_path, json_schema=json_schema
        ):
            # Initialize and yield instance
            yield InstanceClass(**item)
