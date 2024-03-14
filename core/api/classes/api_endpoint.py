# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, AsyncGenerator, Generator, TYPE_CHECKING, TypeVar

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.exceptions import HTTPStatusCodeError
from core.client.types import HTTPMethod
from core.dict.functions.dfrom_schema import dfrom_schema
from core.placeholders import nothing
from core.placeholders.types import Nothing

if TYPE_CHECKING:
    from core.api.classes.api import API
    from core.client.classes.http_response import HTTPResponse
    from core.client.types import HTTPMethodLiteral, JSONDict, JSONFilter, JSONSchema

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
        json: dict[str, Any] | None = None,
        json_path: str | None = None,
        json_filter: JSONFilter | None = None,
        json_schema: JSONSchema | None = None,
        params: dict[str, Any] | None = None,
        params_schema: dict[str, str] | None = None,
        weight: int = 1,
        authenticate: bool = False,
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

        # Set JSON
        self.json = json

        # Set JSON path
        self.json_path = json_path

        # Set JSON filter
        self.json_filter = json_filter

        # Set JSON schema
        self.json_schema = json_schema

        # Set params
        self.params = params or None

        # Set params schema
        self.params_schema = params_schema

        # Set weight
        self.weight = weight

        # Set authenticate
        self.authenticate = authenticate

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
        json: dict[str, Any] | None = None,
        path_schema: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        params_schema: dict[str, str] | None = None,
        weight: int | None = None,
    ) -> HTTPResponse:
        """Makes a synchronous request to the API endpoint"""

        # Check if params and params schema
        if params and params_schema is not None:
            # Apply schema to params
            params = dfrom_schema(params, {v: k for k, v in params_schema.items()})

        # Get path
        path = self.path

        # Check if path schema
        if path_schema is not None:
            # Iterate over path schema
            for key, val in path_schema.items():
                # Replace in path
                path = path.replace(f":{key}", val)

        # Make request and return response
        return self.api.request(
            self.method or HTTPMethod.GET,
            path,
            base_url=self.base_url,
            params=params if params is not None else self.params,
            json=json,
            weight=weight if weight is not None else self.weight,
            authenticate=self.authenticate,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_async(
        self,
        json: dict[str, Any] | None = None,
        path_schema: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        params_schema: dict[str, str] | None = None,
        weight: int | None = None,
        **subs: str,
    ) -> HTTPResponse:
        """Makes an asynchronous request to the API endpoint"""

        # Check if params and params schema
        if params and params_schema is not None:
            # Apply schema to params
            params = dfrom_schema(params, {v: k for k, v in params_schema.items()})

        # Get path
        path = self.path

        # Check if path schema
        if path_schema is not None:
            # Iterate over path schema
            for key, val in path_schema.items():
                # Replace in path
                path = path.replace(f":{key}", val)

        # Make request and return response
        return await self.api.request_async(
            self.method or HTTPMethod.GET,
            path,
            base_url=self.base_url,
            params=params if params is not None else self.params,
            json=json,
            weight=weight if weight is not None else self.weight,
            authenticate=self.authenticate,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST DICT
    # └─────────────────────────────────────────────────────────────────────────────────

    def request_dict(
        self,
        json: dict[str, Any] | None = None,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
        weight: int | None = None,
    ) -> JSONDict | None:
        """Yields an object dict from the current API endpoint"""

        # Make request
        response = self.request(params=params, json=json, weight=weight)

        # Check if response status code is not in 200 range
        if not response.did_succeed:
            # Raise HTTPStatusCodeError
            raise HTTPStatusCodeError(response.status_code)

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
        json: dict[str, Any] | None = None,
        json_path: str | None | Nothing = nothing,
        json_filter: JSONFilter | None = None,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
        weight: int | None = None,
    ) -> Generator[JSONDict, None, None]:
        """Yields a series of object dicts from the current API endpoint"""

        # Make request
        response = self.request(params=params, json=json, weight=weight)

        # Check if response status code is not in 200 range
        if not response.did_succeed:
            # Raise HTTPStatusCodeError
            raise HTTPStatusCodeError(response.status_code)

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Get JSON filter
        json_filter = self.json_filter if json_filter is None else json_filter

        # Iterate over items
        for item in response.dicts(
            json_path=json_path, json_filter=json_filter, json_schema=json_schema
        ):
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
        json: dict[str, Any] | None = None,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
        weight: int | None = None,
    ) -> JSONDict | None:
        """Yields an object dict from the current API endpoint"""

        # Make request
        response = await self.request_async(params=params, json=json, weight=weight)

        # Check if response status code is not in 200 range
        if not response.did_succeed:
            # Raise HTTPStatusCodeError
            raise HTTPStatusCodeError(response.status_code)

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
        json: dict[str, Any] | None = None,
        json_path: str | None | Nothing = nothing,
        json_filter: JSONFilter | None = None,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
        weight: int | None = None,
    ) -> AsyncGenerator[JSONDict, None]:
        """Yields a series of object dicts from the current API endpoint"""

        # Make request
        response = await self.request_async(params=params, json=json, weight=weight)

        # Check if response status code is not in 200 range
        if not response.did_succeed:
            # Raise HTTPStatusCodeError
            raise HTTPStatusCodeError(response.status_code)

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Get JSON filter
        json_filter = self.json_filter if json_filter is None else json_filter

        # Iterate over items
        for item in response.dicts(
            json_path=json_path, json_filter=json_filter, json_schema=json_schema
        ):
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
        json: dict[str, Any] | None = None,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
        weight: int | None = None,
    ) -> T | None:
        """Yields a series of object instances from the current API endpoint"""

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Get item
        item = self.request_dict(
            json=json,
            json_path=json_path,
            json_schema=json_schema,
            params=params,
            overrides=overrides,
            weight=weight,
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
        json: dict[str, Any] | None = None,
        json_path: str | None | Nothing = nothing,
        json_filter: JSONFilter | None = None,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
        weight: int | None = None,
    ) -> Generator[T, None, None]:
        """Yields a series of object instances from the current API endpoint"""

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Get JSON filter
        json_filter = self.json_filter if json_filter is None else json_filter

        # Iterate over items
        for item in self.request_dicts(
            json=json,
            json_path=json_path,
            json_filter=json_filter,
            json_schema=json_schema,
            params=params,
            overrides=overrides,
            weight=weight,
        ):
            # Initialize and yield instance
            yield InstanceClass(**item)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST INSTANCE ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_instance_async(
        self,
        InstanceClass: type[T],
        json: dict[str, Any] | None = None,
        json_path: str | None | Nothing = nothing,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
        weight: int | None = None,
    ) -> T | None:
        """Yields a series of object instances from the current API endpoint"""

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Get item
        item = await self.request_dict_async(
            json=json,
            json_path=json_path,
            json_schema=json_schema,
            params=params,
            overrides=overrides,
            weight=weight,
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
        json: dict[str, Any] | None = None,
        json_path: str | None | Nothing = nothing,
        json_filter: JSONFilter | None = None,
        json_schema: JSONSchema | None | Nothing = nothing,
        params: dict[str, Any] | None = None,
        overrides: dict[str, Any] | None = None,
        weight: int | None = None,
    ) -> AsyncGenerator[T, None]:
        """Yields a series of object instances from the current API endpoint"""

        # Get JSON path and schema
        json_path = self.json_path if isinstance(json_path, Nothing) else json_path
        json_schema = (
            self.json_schema if isinstance(json_schema, Nothing) else json_schema
        )

        # Get JSON filter
        json_filter = self.json_filter if json_filter is None else json_filter

        # Iterate over items
        async for item in self.request_dicts_async(
            json=json,
            json_path=json_path,
            json_filter=json_filter,
            json_schema=json_schema,
            params=params,
            overrides=overrides,
            weight=weight,
        ):
            # Initialize and yield instance
            yield InstanceClass(**item)
