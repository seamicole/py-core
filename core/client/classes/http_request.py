# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

if TYPE_CHECKING:
    from core.client.classes.http_response import HTTPResponse
    from core.client.enums.http_method import HTTPMethod


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP REQUEST
# └─────────────────────────────────────────────────────────────────────────────────────


class HTTPRequest:
    """An HTTP request utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of URL
    url: str

    # Declare type of method
    method: HTTPMethod

    # Declare type of params
    params: dict[str, Any] | None

    # Declare type of headers
    headers: dict[str, Any] | None

    # Declare type of cookies
    cookies: dict[str, Any] | None

    # Declare type of timeout
    timeout: int | float | None

    # Declare type of date
    data: Any

    # Declare type of data
    json: dict[str, Any] | None

    # Declare type of weight
    weight: int

    # Declare type of response
    response: HTTPResponse | None

    # Declare type of is retry
    is_retry: bool

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        url: str,
        method: HTTPMethod,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int | float | None = None,
        data: Any = None,
        json: dict[str, Any] | None = None,
        weight: int = 1,
        is_retry: bool = False,
    ) -> None:
        """Init Method"""

        # Set URL
        self.url = url

        # Set weight
        self.weight = weight

        # Set method
        self.method = method

        # Set params
        self.params = params

        # Set headers
        self.headers = headers

        # Set cookies
        self.cookies = cookies

        # Set timeout
        self.timeout = timeout

        # Set data
        self.data = data

        # Set JSON
        self.json = json

        # Initialize response to None
        self.response = None

        # Set is retry
        self.is_retry = is_retry
