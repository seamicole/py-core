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

if TYPE_CHECKING:
    from core.client.classes.http_response import HTTPResponse


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP REQUEST
# └─────────────────────────────────────────────────────────────────────────────────────


def http_request(
    method: HTTPMethod | str,
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    cookies: dict[str, Any] | None = None,
    timeout: int | float | None = None,
    data: Any = None,
    json: dict[str, Any] | None = None,
) -> HTTPResponse:
    """Makes an HTTP request and returns a HTTPResponse instance"""

    # Check if
    if method == HTTPMethod.POST or (
        isinstance(method, str) and method.lower() == "post"
    ):
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

    # Otherwise handle default case
    else:
        # Make a GET request
        return http_get(
            url=url, params=params, headers=headers, cookies=cookies, timeout=timeout
        )


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP REQUEST ASYNC
# └─────────────────────────────────────────────────────────────────────────────────────


async def http_request_async(
    method: HTTPMethod | str,
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    cookies: dict[str, Any] | None = None,
    timeout: int | float | None = None,
    data: Any = None,
    json: dict[str, Any] | None = None,
) -> HTTPResponse:
    """Makes an HTTP request and returns a HTTPResponse instance"""

    # Check if
    if method == HTTPMethod.POST or (
        isinstance(method, str) and method.lower() == "post"
    ):
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

    # Otherwise handle default case
    else:
        # Make a GET request
        return await http_get_async(
            url=url, params=params, headers=headers, cookies=cookies, timeout=timeout
        )
