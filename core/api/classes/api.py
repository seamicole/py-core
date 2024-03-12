# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import asyncio
import posixpath

from multiprocessing import Manager
from typing import Any, Awaitable, Callable, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.api.classes.api_channel_collection import APIChannelCollection
from core.api.classes.api_endpoint_collection import APIEndpointCollection
from core.client.classes.http_client import HTTPClient
from core.client.classes.ws_client import WSClient
from core.log.classes.logger import Logger

if TYPE_CHECKING:
    from core.client.classes.http_request import HTTPRequest
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
        ws_ping_data: str | dict[str, Any] | None = None,
        ws_ping_interval_ms: int | None = None,
        logger: Logger | None = None,
        logger_key: str | None = None,
        authenticate_request: Callable[[HTTPRequest], HTTPRequest] | None = None,
    ) -> None:
        """Init Method"""

        # Initialize manager
        manager = Manager()

        # Initialize logger
        self.logger = (
            logger
            if logger is not None
            else Logger(
                key=logger_key
                if logger_key
                else f"{self.__class__.__name__}.{hex(id(self))}",
                log_limit=1000,
            )
        )

        # Initialize HTTP client
        self.client = HTTPClient(
            manager=manager,
            weight_per_second=weight_per_second,
            logger=self.logger,
            authenticate_request=authenticate_request,
        )

        # Set base url
        self.base_url = base_url

        # Initialize endpoints
        self.endpoints: APIEndpointCollection = APIEndpointCollection(
            keys=(("url", "method"),)
        )

        # Initialize websocket client
        self.ws = WSClient(
            manager=manager,
            ping_data=ws_ping_data,
            ping_interval_ms=ws_ping_interval_ms,
            logger=self.logger,
        )

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
        authenticate: Callable[[HTTPRequest], HTTPRequest] | bool = False,
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
            authenticate=authenticate,
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
        authenticate: Callable[[HTTPRequest], HTTPRequest] | bool = False,
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
            authenticate=authenticate,
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
        authenticate: Callable[[HTTPRequest], HTTPRequest] | bool = False,
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
            authenticate=authenticate,
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
        authenticate: Callable[[HTTPRequest], HTTPRequest] | bool = False,
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
            authenticate=authenticate,
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
        authenticate: Callable[[HTTPRequest], HTTPRequest] | bool = False,
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
            logger=self.logger,
            authenticate=authenticate,
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
        authenticate: Callable[[HTTPRequest], HTTPRequest] | bool = False,
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
            logger=self.logger,
            authenticate=authenticate,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SUBSCRIBE
    # └─────────────────────────────────────────────────────────────────────────────────

    async def subscribe(
        self,
        data_subscribe: str | dict[Any, Any],
        data_unsubscribe: str | dict[Any, Any],
        receive: Callable[[str | bytes], Awaitable[None] | None],
        should_unsubscribe: Callable[[], bool] = lambda: False,
        uri: str | None = None,
    ) -> None:
        """Subscribes to a websocket channel"""

        # Subscribe to websocket channel
        await self.ws.subscribe(
            uri=uri or self.ws_uri,
            data_subscribe=data_subscribe,
            data_unsubscribe=data_unsubscribe,
            receive=receive,
            should_unsubscribe=should_unsubscribe,
        )
