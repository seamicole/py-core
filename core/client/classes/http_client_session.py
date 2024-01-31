# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import cast, TYPE_CHECKING
from typing_extensions import TypedDict

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.enums.http_method import HTTPMethod
from core.client.types import HTTPMethodLiteral

if TYPE_CHECKING:
    from core.client.classes.http_response import HTTPResponse


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP CLIENT SESSION
# └─────────────────────────────────────────────────────────────────────────────────────


class HTTPClientSession:
    """An HTTP client session utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of requests
    _requests: dict[str, dict[HTTPMethodLiteral, HTTPClientSession.RequestLog]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TYPE ALIASES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Define a request log type alias
    class RequestLog(TypedDict):
        reqs: dict[int, int]
        rets: dict[int, int]
        errs: dict[int, set[str]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        """Init Method"""

        # Initialize request stats
        self._requests = {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LOG REQUEST
    # └─────────────────────────────────────────────────────────────────────────────────

    def log_request(
        self,
        url: str,
        method: HTTPMethod | HTTPMethodLiteral,
        response: HTTPResponse,
        is_retry: bool = False,
    ) -> None:
        """Logs an HTTP client request"""

        # Get HTTP method key
        method_key = cast(
            HTTPMethodLiteral,
            method.value if isinstance(method, HTTPMethod) else HTTPMethodLiteral,
        )

        # Get URL dict
        url_dict = self._requests.setdefault(url, {})

        # Get method dict
        method_dict = url_dict.setdefault(
            method_key, {"reqs": {}, "rets": {}, "errs": {}}
        )

        # Get reqs dict
        reqs_dict = method_dict["reqs"]

        # Add request status code to requests
        reqs_dict[response.status_code] = reqs_dict.get(response.status_code, 0) + 1

        # Check if retry
        if is_retry:
            # Get rets dict
            rets_dict = method_dict["rets"]

            # Add request status code to requests
            rets_dict[response.status_code] = rets_dict.get(response.status_code, 0) + 1

        # Check if is error
        if not response.is_success and response.text_stripped:
            # Get errs dict
            errs_dict = method_dict["errs"]

            # Add error message
            errs_dict.setdefault(response.status_code, set()).add(
                response.text_stripped
            )
