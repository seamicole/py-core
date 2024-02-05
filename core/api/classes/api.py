# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import asyncio
import posixpath

from multiprocessing import Manager
from typing import Any, Callable, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.api.classes.api_channel_collection import APIChannelCollection
from core.api.classes.api_endpoint_collection import APIEndpointCollection
from core.client.classes.http_client import HTTPClient
from core.client.classes.ws_client import WSClient

if TYPE_CHECKING:
    from core.client.classes.http_response import HTTPResponse
    from core.client.enums.http_method import HTTPMethod
    from core.client.types import HTTPMethodLiteral


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ API
# └─────────────────────────────────────────────────────────────────────────────────────


class API:
    """An API utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        base_url: str,
        weight_per_second: float | int | None = None,
        ws_uri: str | None = None,
    ) -> None:
        """Init Method"""

        # Initialize manager
        manager = Manager()

        # Initialize HTTP client
        self.client = HTTPClient(weight_per_second=weight_per_second, manager=manager)

        # Set base url
        self.base_url = base_url

        # Initialize endpoints
        self.endpoints: APIEndpointCollection = APIEndpointCollection(
            keys=(("url", "method"),)
        )

        # Initialize websocket client
        self.ws = WSClient(manager=manager)

        # Set websocket URI
        self.ws_uri = ws_uri or base_url

        # Initialize channels
        self.channels: APIChannelCollection = APIChannelCollection()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ WS EVENT LOOP
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def ws_event_loop(self) -> asyncio.AbstractEventLoop:
        """Returns the websocket event loop"""

        # Return websocket event loop
        return self.ws.event_loop

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CONSTRUCT URL
    # └─────────────────────────────────────────────────────────────────────────────────

    def construct_url(self, *path: str, base_url: str | None = None) -> str:
        """Constructs a URL from the base URL and endpoint"""

        # Get base URL
        base_url = base_url or self.base_url

        # Construct URL
        url = posixpath.join(base_url, *path)

        # Return URL
        return url

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ GET
    # └─────────────────────────────────────────────────────────────────────────────────

    def get(
        self,
        *path: str,
        base_url: str | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int | float | None = None,
        weight: int = 1,
    ) -> HTTPResponse:
        """Makes a GET request to the API"""

        # Make GET request and return response
        return self.request(
            HTTPMethod.GET,
            *path,
            base_url=base_url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            weight=weight,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ GET ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def get_async(
        self,
        *path: str,
        base_url: str | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int | float | None = None,
        weight: int = 1,
    ) -> HTTPResponse:
        """Makes an asynchronous GET request to the API"""

        # Make GET request and return response
        return await self.request_async(
            HTTPMethod.GET,
            *path,
            base_url=base_url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            weight=weight,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ POST
    # └─────────────────────────────────────────────────────────────────────────────────

    def post(
        self,
        *path: str,
        base_url: str | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int | float | None = None,
        data: Any = None,
        json: dict[str, Any] | None = None,
        weight: int = 1,
    ) -> HTTPResponse:
        """Makes a POST request to the API"""

        # Make POST request and return response
        return self.request(
            HTTPMethod.POST,
            *path,
            base_url=base_url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
            weight=weight,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ POST ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def post_async(
        self,
        *path: str,
        base_url: str | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int | float | None = None,
        data: Any = None,
        json: dict[str, Any] | None = None,
        weight: int = 1,
    ) -> HTTPResponse:
        """Makes an asynchronous POST request to the API"""

        # Make POST request and return response
        return await self.request_async(
            HTTPMethod.POST,
            *path,
            base_url=base_url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
            weight=weight,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST
    # └─────────────────────────────────────────────────────────────────────────────────

    def request(
        self,
        method: HTTPMethod | HTTPMethodLiteral,
        *path: str,
        base_url: str | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int | float | None = None,
        data: Any = None,
        json: dict[str, Any] | None = None,
        weight: int = 1,
    ) -> HTTPResponse:
        """Makes a request to the API"""

        # Get URL
        url = self.construct_url(*path, base_url=base_url)

        # Make request and return response
        return self.client.request(
            url=url,
            method=method,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
            weight=weight,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_async(
        self,
        method: HTTPMethod | HTTPMethodLiteral,
        *path: str,
        base_url: str | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int | float | None = None,
        data: Any = None,
        json: dict[str, Any] | None = None,
        weight: int = 1,
    ) -> HTTPResponse:
        """Makes an asynchronous request to the API"""

        # Get URL
        url = self.construct_url(*path, base_url=base_url)

        # Make request and return response
        return await self.client.request_async(
            url=url,
            method=method,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
            weight=weight,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SUBSCRIBE
    # └─────────────────────────────────────────────────────────────────────────────────

    async def subscribe(
        self,
        data: str | dict[Any, Any],
        callback: Callable[[str | bytes], None],
        uri: str | None = None,
    ) -> None:
        """Subscribes to a websocket channel"""

        # Subscribe to websocket channel
        await self.ws.subscribe(uri=uri or self.ws_uri, data=data, callback=callback)
