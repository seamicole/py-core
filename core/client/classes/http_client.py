# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.classes.http_client_session import HTTPClientSession
from core.client.functions.http_request import http_request, http_request_async

if TYPE_CHECKING:
    from core.client.classes.http_response import HTTPResponse
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

    def __init__(self) -> None:
        """Init Method"""

        # Initialize HTTP client session
        self.session = HTTPClientSession()

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
    ) -> HTTPResponse:
        """Makes a request to the API"""

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
        )

        # Log response
        self.session.log_request(url=url, method=method, response=response)

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
    ) -> HTTPResponse:
        """Makes an asynchronous request to the API"""

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
        )

        # Log response
        self.session.log_request(url=url, method=method, response=response)

        # Return response
        return response
