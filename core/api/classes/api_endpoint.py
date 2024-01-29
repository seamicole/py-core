# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, AsyncGenerator, Generator, TYPE_CHECKING, TypeVar

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.types import HTTPMethod
from core.dict.functions.dfrom_schema import dfrom_schema
from core.placeholders import nothing
from core.placeholders.types import Nothing

if TYPE_CHECKING:
    from core.api.classes.api import API
    from core.client.classes.http_response import HTTPResponse
    from core.client.types import HTTPMethodLiteral, JSONDict, JSONSchema

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TYPE VARIABLES
# └─────────────────────────────────────────────────────────────────────────────────────

T = TypeVar("T")


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
        params: dict[str, Any] | None = None,
        params_schema: dict[str, str] | None = None,
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

        # Set params
        self.params = params or None

        # Set params schema
        self.params_schema = params_schema

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        """Representation Method"""

        # Return representation
        return f"<{self.__class__.__name__}: {self.path}>"

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

    def request(
        self,
        params: dict[str, Any] | None = None,
        params_schema: dict[str, str] | None = None,
    ) -> HTTPResponse:
        """Makes a synchronous request to the API endpoint"""

        # Check if params and params schema
        if params and params_schema is not None:
            # Apply schema to params
            params = dfrom_schema(params, {v: k for k, v in params_schema.items()})

        # Make request and return response
        return self.api.request(
            self.method or HTTPMethod.GET,
            self.path,
            base_url=self.base_url,
            params=params if params is not None else self.params,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_async(
        self,
        params: dict[str, Any] | None = None,
        params_schema: dict[str, str] | None = None,
    ) -> HTTPResponse:
        """Makes an asynchronous request to the API endpoint"""

        # Check if params and params schema
        if params and params_schema is not None:
            # Apply schema to params
            params = dfrom_schema(params, {v: k for k, v in params_schema.items()})

        # Make request and return response
        return await self.api.request_async(
            self.method or HTTPMethod.GET,
            self.path,
            base_url=self.base_url,
            params=params if params is not None else self.params,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST DICT
    # └─────────────────────────────────────────────────────────────────────────────────

    def request_dict(
        self,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
    ) -> JSONDict | None:
        """Yields an object dict from the current API endpoint"""

        # Make request
        response = self.request(params=params)

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Get response dict
        response_dict = response.dict(json_path=json_path, json_schema=json_schema)

        # Check if overrides
        if response_dict is not None and overrides is not None:
            # Update response dict
            response_dict.update(overrides)

        # Return response dict
        return response_dict

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST DICTS
    # └─────────────────────────────────────────────────────────────────────────────────

    def request_dicts(
        self,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
    ) -> Generator[JSONDict, None, None]:
        """Yields a series of object dicts from the current API endpoint"""

        # Make request
        response = self.request(params=params)

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Iterate over items
        for item in response.dicts(json_path=json_path, json_schema=json_schema):
            # Check if overrides
            if item is not None and overrides is not None:
                # Update item
                item.update(overrides)

            # Yield item
            yield item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST DICT ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_dict_async(
        self,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
    ) -> JSONDict | None:
        """Yields an object dict from the current API endpoint"""

        # Make request
        response = await self.request_async(params=params)

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Get response dict
        response_dict = response.dict(json_path=json_path, json_schema=json_schema)

        # Check if overrides
        if response_dict is not None and overrides is not None:
            # Update response dict
            response_dict.update(overrides)

        # Return response dict
        return response_dict

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST DICTS ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_dicts_async(
        self,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
    ) -> AsyncGenerator[JSONDict, None]:
        """Yields a series of object dicts from the current API endpoint"""

        # Make request
        response = await self.request_async(params=params)

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Iterate over items
        for item in response.dicts(json_path=json_path, json_schema=json_schema):
            # Check if overrides
            if item is not None and overrides is not None:
                # Update item
                item.update(overrides)

            # Yield item
            yield item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST INSTANCE
    # └─────────────────────────────────────────────────────────────────────────────────

    def request_instance(
        self,
        InstanceClass: type[T],
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
    ) -> T | None:
        """Yields a series of object instances from the current API endpoint"""

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Get item
        item = self.request_dict(
            json_path=json_path,
            json_schema=json_schema,
            params=params,
            overrides=overrides,
        )

        # Return if item is None
        if item is None:
            return None

        # Initialize and return instance
        return InstanceClass(**item)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST INSTANCES
    # └─────────────────────────────────────────────────────────────────────────────────

    def request_instances(
        self,
        InstanceClass: type[T],
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
    ) -> Generator[T, None, None]:
        """Yields a series of object instances from the current API endpoint"""

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Iterate over items
        for item in self.request_dicts(
            json_path=json_path,
            json_schema=json_schema,
            params=params,
            overrides=overrides,
        ):
            # Initialize and yield instance
            yield InstanceClass(**item)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST INSTANCE ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_instance_async(
        self,
        InstanceClass: type[T],
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
    ) -> T | None:
        """Yields a series of object instances from the current API endpoint"""

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Get item
        item = await self.request_dict_async(
            json_path=json_path,
            json_schema=json_schema,
            params=params,
            overrides=overrides,
        )

        # Return if item is None
        if item is None:
            return None

        # Initialize and return instance
        return InstanceClass(**item)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST INSTANCES ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_instances_async(
        self,
        InstanceClass: type[T],
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
    ) -> AsyncGenerator[T, None]:
        """Yields a series of object instances from the current API endpoint"""

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Iterate over items
        async for item in self.request_dicts_async(
            json_path=json_path,
            json_schema=json_schema,
            params=params,
            overrides=overrides,
        ):
            # Initialize and yield instance
            yield InstanceClass(**item)
