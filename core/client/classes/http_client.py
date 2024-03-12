# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import asyncio
import time

from multiprocessing.managers import SyncManager
from typing import Any, Callable, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.classes.http_client_session import HTTPClientSession
from core.client.classes.http_response import HTTPResponse
from core.client.functions.http_request import http_request, http_request_async
from core.log.classes.logger import Logger

if TYPE_CHECKING:
    from core.client.classes.http_request import HTTPRequest
    from core.client.enums.http_method import HTTPMethod
    from core.client.types import HTTPMethodLiteral


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP CLIENT
# └─────────────────────────────────────────────────────────────────────────────────────


class HTTPClient:
    """An HTTP client utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        weight_per_second: int | float | None = None,
        manager: SyncManager | None = None,
        logger: Logger | None = None,
        logger_key: str | None = None,
        authenticate_request: Callable[[HTTPRequest], HTTPRequest] | None = None,
    ) -> None:
        """Init Method"""

        # Assert weight per second is greater than 0
        assert (
            weight_per_second is None or weight_per_second > 0
        ), "Weight per second must be greater than zero!"

        # Initialize HTTP client session
        self.session = HTTPClientSession(manager=manager)

        # Set weight interval
        self.weight_interval = (
            (1 / weight_per_second if weight_per_second < 1 else 1)
            if weight_per_second is not None
            else None
        )

        # Set weight per second
        self.weight_per_second = weight_per_second

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

        # Set authenticate request
        self._authenticate_request = authenticate_request

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ DELETE
    # └─────────────────────────────────────────────────────────────────────────────────

    def delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int | float | None = None,
        weight: int = 1,
        authenticate: Callable[[HTTPRequest], HTTPRequest] | bool = False,
    ) -> HTTPResponse:
        """Makes a DELETE request to the API"""

        # Make DELETE request and return response
        return self.request(
            url=url,
            method=HTTPMethod.DELETE,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            weight=weight,
            authenticate=(
                authenticate
                if callable(authenticate)
                else (
                    self._authenticate_request
                    if authenticate is True and self._authenticate_request is not None
                    else False
                )
            ),
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ DELETE ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def delete_async(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int | float | None = None,
        weight: int = 1,
        authenticate: Callable[[HTTPRequest], HTTPRequest] | bool = False,
    ) -> HTTPResponse:
        """Makes an asynchronous DELETE request to the API"""

        # Make DELETE request and return response
        return await self.request_async(
            url=url,
            method=HTTPMethod.DELETE,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            weight=weight,
            authenticate=(
                authenticate
                if callable(authenticate)
                else (
                    self._authenticate_request
                    if authenticate is True and self._authenticate_request is not None
                    else False
                )
            ),
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ GET
    # └─────────────────────────────────────────────────────────────────────────────────

    def get(
        self,
        url: str,
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
            url=url,
            method=HTTPMethod.GET,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            weight=weight,
            authenticate=(
                authenticate
                if callable(authenticate)
                else (
                    self._authenticate_request
                    if authenticate is True and self._authenticate_request is not None
                    else False
                )
            ),
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ GET ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def get_async(
        self,
        url: str,
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
            url=url,
            method=HTTPMethod.GET,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            weight=weight,
            authenticate=(
                authenticate
                if callable(authenticate)
                else (
                    self._authenticate_request
                    if authenticate is True and self._authenticate_request is not None
                    else False
                )
            ),
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ POST
    # └─────────────────────────────────────────────────────────────────────────────────

    def post(
        self,
        url: str,
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
            url=url,
            method=HTTPMethod.POST,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
            weight=weight,
            authenticate=(
                authenticate
                if callable(authenticate)
                else (
                    self._authenticate_request
                    if authenticate is True and self._authenticate_request is not None
                    else False
                )
            ),
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ POST ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def post_async(
        self,
        url: str,
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
            url=url,
            method=HTTPMethod.POST,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
            weight=weight,
            authenticate=(
                authenticate
                if callable(authenticate)
                else (
                    self._authenticate_request
                    if authenticate is True and self._authenticate_request is not None
                    else False
                )
            ),
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST
    # └─────────────────────────────────────────────────────────────────────────────────

    def request(
        self,
        url: str,
        method: HTTPMethod | HTTPMethodLiteral,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int | float | None = None,
        data: Any = None,
        json: dict[str, Any] | None = None,
        weight: int = 1,
        logger: Logger | None = None,
        authenticate: Callable[[HTTPRequest], HTTPRequest] | bool = False,
    ) -> HTTPResponse:
        """Makes a request to the API"""

        # Get time to sleep
        time_to_sleep = self.throttle(weight=weight)

        # Initialize while loop
        while time_to_sleep > 0:
            # Sleep and throttle
            time.sleep(time_to_sleep)
            time_to_sleep = self.throttle(weight=weight)

        # Get response
        response = http_request(
            url=url,
            method=method,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
            weight=weight,
            logger=logger if logger is not None else self.logger,
            authenticate=(
                authenticate
                if callable(authenticate)
                else (self._authenticate_request if authenticate is True else None)
            ),
        )

        # Log response
        self.session.log_response(response)

        # Return response
        return response

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_async(
        self,
        url: str,
        method: HTTPMethod | HTTPMethodLiteral,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int | float | None = None,
        data: Any = None,
        json: dict[str, Any] | None = None,
        weight: int = 1,
        logger: Logger | None = None,
        authenticate: Callable[[HTTPRequest], HTTPRequest] | bool = False,
    ) -> HTTPResponse:
        """Makes an asynchronous request to the API"""

        # Get time to sleep
        time_to_sleep = self.throttle(weight=weight)

        # Initialize while loop
        while time_to_sleep > 0:
            # Sleep and throttle
            await asyncio.sleep(time_to_sleep)
            time_to_sleep = self.throttle(weight=weight)

        # Get response
        response = await http_request_async(
            url=url,
            method=method,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
            weight=weight,
            logger=logger if logger is not None else self.logger,
            authenticate=(
                authenticate
                if callable(authenticate)
                else (self._authenticate_request if authenticate is True else None)
            ),
        )
        if response.status_code != 200:
            print(response.status_code)

        # Log response
        self.session.log_response(response)

        # Return response
        return response

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ THROTTLE
    # └─────────────────────────────────────────────────────────────────────────────────

    def throttle(self, weight: int) -> float:
        """Throttles the client before making a request"""

        # Check if no rate limits are applied
        if self.weight_interval is None or self.weight_per_second is None:
            return 0

        # Acquire lock
        with self.session._lock:
            # Log request
            self.session.log_request(weight, self.weight_interval)

            # Get weight used
            weight_used = self.session._usage["wt"]

            # Break if weight respects limit
            if weight_used / self.weight_interval <= self.weight_per_second:
                return 0

            # Decrement weight
            self.session._usage["wt"] -= weight

            # Get timestamp
            ts = self.session._usage["ts"]

        # Get time to sleep
        time_to_sleep = self.weight_interval - (time.time() - ts)

        # Return time to sleep
        return max(time_to_sleep, 0)
