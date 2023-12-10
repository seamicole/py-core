# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.functions.http_get import http_get, http_get_async
from core.client.functions.http_post import http_post, http_post_async
from core.client.enums.http_method import HTTPMethod
from core.client.exceptions import InvalidHTTPMethodError

if TYPE_CHECKING:
    from core.client.classes.http_response import HTTPResponse
    from core.client.types import HTTPMethodLiteral


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP REQUEST
# └─────────────────────────────────────────────────────────────────────────────────────


def http_request(
    method: HTTPMethod | HTTPMethodLiteral,
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    cookies: dict[str, Any] | None = None,
    timeout: int | float | None = None,
    data: Any = None,
    json: dict[str, Any] | None = None,
) -> HTTPResponse:
    """Makes an HTTP request and returns a HTTPResponse instance"""

    # Check if method is a string
    if isinstance(method, str):
        # Convert method to HTTPMethod
        method = HTTPMethod(method.upper())

    # Check if GET
    if method == HTTPMethod.GET:
        # Make a GET request
        return http_get(
            url=url, params=params, headers=headers, cookies=cookies, timeout=timeout
        )

    # Otherwise, check if POST
    elif method == HTTPMethod.POST:
        # Make a POST request
        return http_post(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
        )

    # Otherwise, raise an exception
    else:
        # Raise an InvalidHTTPMethodError exception
        raise InvalidHTTPMethodError(method=method)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP REQUEST ASYNC
# └─────────────────────────────────────────────────────────────────────────────────────


async def http_request_async(
    method: HTTPMethod | HTTPMethodLiteral,
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    cookies: dict[str, Any] | None = None,
    timeout: int | float | None = None,
    data: Any = None,
    json: dict[str, Any] | None = None,
) -> HTTPResponse:
    """Makes an HTTP request and returns a HTTPResponse instance"""

    # Check if method is a string
    if isinstance(method, str):
        # Convert method to HTTPMethod
        method = HTTPMethod(method.upper())

    # Check if GET
    if method == HTTPMethod.GET:
        # Make a GET request
        return await http_get_async(
            url=url, params=params, headers=headers, cookies=cookies, timeout=timeout
        )

    # Check if
    elif method == HTTPMethod.POST:
        # Make a POST request
        return await http_post_async(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
        )

    # Otherwise, raise an exception
    else:
        # Raise an InvalidHTTPMethodError exception
        raise InvalidHTTPMethodError(method=method)
