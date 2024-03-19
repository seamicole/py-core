# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import time

from typing import Any, Callable, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.functions.http_delete import http_delete, http_delete_async
from core.client.functions.http_get import http_get, http_get_async
from core.client.functions.http_post import http_post, http_post_async
from core.client.enums.http_method import HTTPMethod
from core.client.classes.http_request import HTTPRequest
from core.client.exceptions import InvalidHTTPMethodError

if TYPE_CHECKING:
    from core.client.classes.http_response import HTTPResponse
    from core.client.types import HTTPMethodLiteral
    from core.log.classes.logger import Logger


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CONSTRUCT LOG
# └─────────────────────────────────────────────────────────────────────────────────────


def construct_log(
    method: HTTPMethod,
    url: str,
    is_cached: bool,
    params: dict[str, Any] | None = None,
    status_code: int | None = None,
) -> str:
    """Constructs and returns a log"""

    # Pad method name
    method_name = f"{method.name:>7}"

    # Check if status code is not None
    if status_code is not None:
        # Add to method name
        method_name = f"{method_name} {status_code}"

    # Check if params is not None
    if params is not None:
        # Get param string
        param_string = "&".join([f"{k}={v}" for k, v in params.items()])

        # Append to URL
        url = f"{url}?{param_string}"

    # Construct log
    log = f"{method_name} {url}"

    # Check if cached
    if is_cached:
        log = f"{log} [CACHED]"

    # Return log
    return log


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ LOG REQUEST
# └─────────────────────────────────────────────────────────────────────────────────────


def log_request(logger: Logger | None, request: HTTPRequest, is_cached: bool) -> None:
    """Constructs and prints a request log"""

    # Return if no logger
    if logger is None:
        return

    # Construct log
    log = construct_log(
        method=request.method,
        url=request.url,
        is_cached=is_cached,
        params=request.params,
    )

    # Print log
    logger.debug(log, key="http_requests")


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ LOG RESPONSE
# └─────────────────────────────────────────────────────────────────────────────────────


def log_response(
    logger: Logger | None,
    request: HTTPRequest,
    status_code: int,
    ms: int,
    is_cached: bool,
) -> None:
    """Constructs and prints a response log"""

    # Return if no logger
    if logger is None:
        return

    # Construct log
    log = construct_log(
        method=request.method,
        status_code=status_code,
        url=request.url,
        is_cached=is_cached,
        params=request.params,
    )

    # Add ms to log
    log = f"{log} ({ms} ms)"

    # Print log
    logger.debug(log, key="http_responses")


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
    authenticate: Callable[[HTTPRequest], HTTPRequest] | None = None,
    cached_responses: dict[str, HTTPResponse] | None = None,
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

    # Initialize request
    request = HTTPRequest(
        url=url,
        method=method,
        params=params,
        data=data,
        json=json,
        headers=headers,
        cookies=cookies,
        timeout=timeout,
        weight=weight,
    )

    # Check if a response cache was passed
    if cached_responses:
        # Get response
        response = cached_responses.get(request.signature)

        # Check if response is not None
        if response is not None:
            # Log request and response
            log_request(logger=logger, request=request, is_cached=True)
            log_response(
                logger=logger,
                request=request,
                status_code=response.status_code,
                ms=0,
                is_cached=True,
            )

            # Return response
            return response

    # Get request signature before applying authentication
    request_signature = request.signature if cached_responses is not None else None

    # Authenticate request
    if authenticate is not None:
        request = authenticate(request)

    # Log request
    log_request(logger=logger, request=request, is_cached=False)

    # Get t0
    t0 = time.time()

    # Check if GET
    if method == HTTPMethod.GET:
        # Make a GET request
        response = http_get(request=request)

    # Otherwise, check if POST
    elif method == HTTPMethod.POST:
        # Make a POST request
        response = http_post(request=request)

    # Otherwise, check if DELETE
    elif method == HTTPMethod.DELETE:
        # Make a DELETE request
        response = http_delete(request=request)

    # Otherwise, raise an exception
    else:
        # Raise an InvalidHTTPMethodError exception
        raise InvalidHTTPMethodError(method=method)

    # Get t1
    t1 = time.time()

    # Get ms
    ms = int((t1 - t0) * 1000)

    # Log response
    log_response(
        logger=logger,
        request=request,
        status_code=response.status_code,
        ms=ms,
        is_cached=False,
    )

    # Check if a response cache was passed
    if cached_responses is not None and request_signature is not None:
        # Cache response
        cached_responses[request_signature] = response

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
    authenticate: Callable[[HTTPRequest], HTTPRequest] | None = None,
    cached_responses: dict[str, HTTPResponse] | None = None,
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

    # Initialize request
    request = HTTPRequest(
        url=url,
        method=method,
        params=params,
        data=data,
        json=json,
        headers=headers,
        cookies=cookies,
        timeout=timeout,
        weight=weight,
    )

    # Check if a response cache was passed
    if cached_responses:
        # Get response
        response = cached_responses.get(request.signature)

        # Check if response is not None
        if response is not None:
            # Log request and response
            log_request(logger=logger, request=request, is_cached=True)
            log_response(
                logger=logger,
                request=request,
                status_code=response.status_code,
                ms=0,
                is_cached=True,
            )

            # Return response
            return response

    # Get request signature before applying authentication
    request_signature = request.signature if cached_responses is not None else None

    # Authenticate request
    if authenticate is not None:
        request = authenticate(request)

    # Log request
    log_request(logger=logger, request=request, is_cached=False)

    # Get t0
    t0 = time.time()

    # Check if GET
    if method == HTTPMethod.GET:
        # Make a GET request
        response = await http_get_async(request=request)

    # Otherwise, check if POST
    elif method == HTTPMethod.POST:
        # Make a POST request
        response = await http_post_async(request=request)

    # Otherwise, check if DELETE
    elif method == HTTPMethod.DELETE:
        # Make a DELETE request
        response = await http_delete_async(request=request)

    # Otherwise, raise an exception
    else:
        # Raise an InvalidHTTPMethodError exception
        raise InvalidHTTPMethodError(method=method)

    # Get t1
    t1 = time.time()

    # Get ms
    ms = int((t1 - t0) * 1000)

    # Log response
    log_response(
        logger=logger,
        request=request,
        status_code=response.status_code,
        ms=ms,
        is_cached=False,
    )

    # Check if a response cache was passed
    if cached_responses is not None and request_signature is not None:
        # Cache response
        cached_responses[request_signature] = response

    # Return response
    return response
