# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urlparse

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.api.classes.api_store import api_store
from core.collections.classes.item import Item
from core.enums import HTTPMethod

if TYPE_CHECKING:
    from core.api.classes.api import API
    from core.api.classes.api_response import APIResponse
    from core.types import Args, JSONSchema, Kwargs


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ API ENDPOINT
# └─────────────────────────────────────────────────────────────────────────────────────


class APIEndpoint(Item):
    """A utility class that represents API endpoints"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of API
    api: API

    # Declare type of kind
    kind: str

    # Declare type of method
    method: HTTPMethod

    # Declare type of route
    route: str

    # Declare type of base URL
    _base_url: str | None = None

    # Declare type of JSON root
    json_root: str | None = None

    # Declare type of JSON schema
    json_schema: JSONSchema | None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        api: API,
        kind: str,
        method: HTTPMethod | str,
        url: str | None = None,
        route: str | None = None,
        base_url: str | None = None,
        json_root: str | None = None,
        json_schema: JSONSchema | None = None,
        *args: Args,
        **kwargs: Kwargs,
    ) -> None:
        """Initialize the API endpoint"""

        # Check if no URL or route was provided
        if url is None and route is None:
            # Get class name
            class_name = self.__class__.__name__

            # Raise TypeError
            raise TypeError(f"{class_name}.__init__() requires either a URL or a route")

        # Call super init method
        super().__init__(*args, **kwargs)

        # Set API
        self.api = api

        # Set kind
        self.kind = kind.lower().strip()

        # Set method
        self.method = HTTPMethod(method.upper()) if isinstance(method, str) else method

        # Check if URL is not null
        if url:
            # Lowercase and strip URL
            url = url.lower().strip()

            # Parse the URL
            url_parsed = urlparse(url)

            # Extract the base URL
            base_url = f"{url_parsed.scheme}://{url_parsed.netloc}"

            # Extract the route
            route = url_parsed.path[1:]

        # Set route
        self.route = route.lower().strip() if route else ""

        # Set base URL
        self._base_url = base_url

        # Set JSON root
        self.json_root = json_root

        # Set JSON schema
        self.json_schema = json_schema

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __STR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __str__(self) -> str:
        """String Method"""

        # Return the endpoint route
        return self.route

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ URL
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def url(self) -> str:
        """Returns the URL for the endpoint"""

        # Construct and return the URL
        return self.api.construct_url(self.route, base_url=self.base_url)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ BASE URL
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def base_url(self) -> str:
        """Returns the base URL for the endpoint"""

        # Return the base URL
        return self._base_url if self._base_url is not None else self.api.base_url

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST
    # └─────────────────────────────────────────────────────────────────────────────────

    def request(self) -> APIResponse:
        """Make a synchronous HTTP request to the endpoint"""

        # Make request and return response
        return self.api.request(self.method, self.route, base_url=self.base_url)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_async(self) -> APIResponse:
        """Make an asynchronous HTTP request to the endpoint"""

        # Make request and return response
        return await self.api.request_async(
            self.method, self.route, base_url=self.base_url
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ META
    # └─────────────────────────────────────────────────────────────────────────────────

    class Meta(Item.Meta):
        """Meta Class"""

        # Define items
        ITEMS = api_store.get_or_create("api_endpoints")
