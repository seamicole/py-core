# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import posixpath

from typing import Any, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.functions.http_request import http_request, http_request_async
from core.collection.classes.collection import Collection

if TYPE_CHECKING:
    from core.api.classes.api_endpoint import APIEndpoint
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

    def __init__(self, base_url: str) -> None:
        """Init Method"""

        # Set base url
        self.base_url = base_url

        # Initialize endpoints
        self.endpoints: Collection[APIEndpoint] = Collection(keys=("url",))

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
    ) -> HTTPResponse:
        """Makes a request to the API"""

        # Get URL
        url = self.construct_url(*path, base_url=base_url)

        # Make request and return response
        return http_request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
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
    ) -> HTTPResponse:
        """Makes an asynchronous request to the API"""

        # Get URL
        url = self.construct_url(*path, base_url=base_url)

        # Make request and return response
        return await http_request_async(
            method=method,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
        )
