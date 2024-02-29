# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import time

from typing import Any, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.functions.http_delete import http_delete, http_delete_async
from core.client.functions.http_get import http_get, http_get_async
from core.client.functions.http_post import http_post, http_post_async
from core.client.enums.http_method import HTTPMethod
from core.client.exceptions import InvalidHTTPMethodError

if TYPE_CHECKING:
    from core.client.classes.http_response import HTTPResponse
    from core.client.types import HTTPMethodLiteral
    from core.log.classes.logger import Logger


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CONSTRUCT LOG
# └─────────────────────────────────────────────────────────────────────────────────────


def construct_log(method: HTTPMethod, url: str) -> str:
    """Constructs and returns a log"""

    # Pad method name
    method_name = f"{method.name:>7}"

    # Construct log
    log = f"{method_name} {url}"

    # Return log
    return log


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ LOG REQUEST
# └─────────────────────────────────────────────────────────────────────────────────────


def log_request(logger: Logger | None, method: HTTPMethod, url: str) -> None:
    """Constructs and prints a request log"""

    # Return if no logger
    if logger is None:
        return

    # Construct log
    log = construct_log(method=method, url=url)

    # Print log
    logger.debug(log, key="http_requests")


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ LOG RESPONSE
# └─────────────────────────────────────────────────────────────────────────────────────


def log_response(logger: Logger | None, method: HTTPMethod, url: str, ms: int) -> None:
    """Constructs and prints a response log"""

    # Return if no logger
    if logger is None:
        return

    # Construct log
    log = construct_log(method=method, url=url)

    # Add ms to log
    log = f"{log} ({ms} ms)"

    # Print log
    logger.info(log, key="http_responses")


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
    weight: int = 1,
    logger: Logger | None = None,
) -> HTTPResponse:
    """Makes an HTTP request and returns a HTTPResponse instance"""

    # Check if method is a string
    if isinstance(method, str):
        # Check if method not in HTTP methods
        if method not in HTTPMethod.__members__:
            # Raise an InvalidHTTPMethodError exception
            raise InvalidHTTPMethodError(method=method)

        # Convert to enum
        method = HTTPMethod[method]

    # Log request
    log_request(logger=logger, method=method, url=url)

    # Get t0
    t0 = time.time()

    # Check if GET
    if method == HTTPMethod.GET:
        # Make a GET request
        response = http_get(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            weight=weight,
        )

    # Otherwise, check if POST
    elif method == HTTPMethod.POST:
        # Make a POST request
        response = http_post(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
            weight=weight,
        )

    # Otherwise, check if DELETE
    elif method == HTTPMethod.DELETE:
        # Make a DELETE request
        response = http_delete(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            weight=weight,
        )

    # Otherwise, raise an exception
    else:
        # Raise an InvalidHTTPMethodError exception
        raise InvalidHTTPMethodError(method=method)

    # Get t1
    t1 = time.time()

    # Get ms
    ms = int((t1 - t0) * 1000)

    # Log response
    log_response(logger=logger, method=method, url=url, ms=ms)

    # Return response
    return response


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
    weight: int = 1,
    logger: Logger | None = None,
) -> HTTPResponse:
    """Makes an HTTP request and returns a HTTPResponse instance"""

    # Check if method is a string
    if isinstance(method, str):
        # Check if method not in HTTP methods
        if method not in HTTPMethod.__members__:
            # Raise an InvalidHTTPMethodError exception
            raise InvalidHTTPMethodError(method=method)

        # Convert to enum
        method = HTTPMethod[method]

    # Log request
    log_request(logger=logger, method=method, url=url)

    # Get t0
    t0 = time.time()

    # Check if GET
    if method == HTTPMethod.GET:
        # Make a GET request
        response = await http_get_async(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            weight=weight,
        )

    # Otherwise, check if POST
    elif method == HTTPMethod.POST:
        # Make a POST request
        response = await http_post_async(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            data=data,
            json=json,
            weight=weight,
        )

    # Otherwise, check if DELETE
    elif method == HTTPMethod.DELETE:
        # Make a DELETE request
        response = await http_delete_async(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            weight=weight,
        )

    # Otherwise, raise an exception
    else:
        # Raise an InvalidHTTPMethodError exception
        raise InvalidHTTPMethodError(method=method)

    # Get t1
    t1 = time.time()

    # Get ms
    ms = int((t1 - t0) * 1000)

    # Log response
    log_response(logger=logger, method=method, url=url, ms=ms)

    # Return response
    return response
