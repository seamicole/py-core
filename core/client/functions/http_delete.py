# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any

try:
    import aiohttp
except ImportError:
    aiohttp = None  # type: ignore

try:
    import httpx
except ImportError:
    httpx = None  # type: ignore

try:
    import requests
except ImportError:
    requests = None  # type: ignore

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.classes.http_request import HTTPRequest
from core.client.classes.http_response import HTTPResponse
from core.client.enums.http_method import HTTPMethod


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP DELETE
# └─────────────────────────────────────────────────────────────────────────────────────


def http_delete(
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    cookies: dict[str, Any] | None = None,
    timeout: int | float | None = None,
    weight: int = 1,
) -> HTTPResponse:
    """Makes an HTTP DELETE request and returns a HTTPResponse instance"""

    # Initialize request
    request = HTTPRequest(
        url=url,
        method=HTTPMethod.DELETE,
        params=params,
        headers=headers,
        cookies=cookies,
        timeout=timeout,
        weight=weight,
    )

    # Get the requester
    requester = httpx or requests

    # Check if requester is None
    if requester is None:
        # Raise an ImportError
        raise ImportError("httpx or requests is required to use this function")

    # Make the request
    response = requester.delete(
        url=url,
        params=params,
        headers=headers,
        cookies=cookies,
        timeout=timeout,
    )

    # Initialize try-except block
    try:
        # Get the response JSON
        response_json = response.json()
    except Exception:
        # Set the response JSON to None
        response_json = None

    # Initialize response
    res = HTTPResponse(
        request=request,
        obj=response,
        text=response.text,
        json=response_json,
        weight=weight,
    )

    # Set response
    request.response = res

    # Return response
    return res


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP DELETE ASYNC
# └─────────────────────────────────────────────────────────────────────────────────────


async def http_delete_async(
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    cookies: dict[str, Any] | None = None,
    timeout: int | float | None = None,
    weight: int = 1,
) -> HTTPResponse:
    """Makes an HTTP DELETE request and returns a HTTPResponse instance"""

    # Initialize request
    request = HTTPRequest(
        url=url,
        method=HTTPMethod.DELETE,
        params=params,
        headers=headers,
        cookies=cookies,
        timeout=timeout,
        weight=weight,
    )

    # Check if aiohttp is being used
    if aiohttp:
        # Initialize the session
        async with aiohttp.ClientSession(
            headers=headers,
            cookies=cookies,
            timeout=aiohttp.ClientTimeout(total=timeout),
        ) as session:
            # Make the request
            async with session.delete(url=url, params=params) as response_aiohttp:
                # Initialize try-except block
                try:
                    # Get the response JSON
                    response_json = await response_aiohttp.json()

                except Exception:
                    # Set the response JSON to None
                    response_json = None

                # Initialize response
                res = HTTPResponse(
                    request=request,
                    obj=response_aiohttp,
                    text=await response_aiohttp.text(),
                    json=response_json,
                    weight=weight,
                )

                # Set response
                request.response = res

                # Return response
                return res

    # Check if httpx is None
    if httpx is None:
        # Raise an ImportError
        raise ImportError("aiohttp or httpx is required to use this function")

    # Initialize the client
    async with httpx.AsyncClient(
        headers=headers, cookies=cookies, timeout=timeout
    ) as client:
        # Make the request
        response_httpx = await client.delete(url=url, params=params)

    # Initialize try-except block
    try:
        # Get the response JSON
        response_json = response_httpx.json()

    except Exception:
        # Set the response JSON to None
        response_json = None

    # Initialize response
    res = HTTPResponse(
        request=request,
        obj=response_httpx,
        text=response_httpx.text,
        json=response_json,
        weight=weight,
    )

    # Set response
    request.response = res

    # Return response
    return res
