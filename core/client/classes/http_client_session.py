# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import time

from multiprocessing import Manager
from multiprocessing.managers import DictProxy
from typing import cast, Literal, TYPE_CHECKING
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
    # │ TYPE ALIASES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Define a request log type alias
    class RequestLog(TypedDict):
        reqs: dict[int, int]
        rets: dict[int, int]
        errs: dict[int, set[str]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of usage
    _usage: DictProxy[Literal["weight"] | Literal["second"], int | float]

    # Declare type of requests
    _requests: DictProxy[str, dict[HTTPMethodLiteral, HTTPClientSession.RequestLog]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        """Init Method"""

        # Initialize a manager
        self._manager = Manager()

        # Initialize usage
        self._usage = self._manager.dict({"weight": 0, "second": time.time()})

        # Initialize requests
        self._requests = self._manager.dict()

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

        # Get second
        second = time.time()

        # Initialize lock
        with self._manager.Lock():
            # Check if one second elapsed
            if second - self._usage["second"] >= 1:
                # Reset usage
                self._usage["weight"] = response.weight
                self._usage["second"] = second

            # Otherwise increment weight
            else:
                # Increment weight
                self._usage["weight"] += response.weight

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
                rets_dict[response.status_code] = (
                    rets_dict.get(response.status_code, 0) + 1
                )

            # Check if is error
            if not response.is_success and response.text_stripped:
                # Get errs dict
                errs_dict = method_dict["errs"]

                # Add error message
                errs_dict.setdefault(response.status_code, set()).add(
                    response.text_stripped
                )

            # Set URL dict
            self._requests[url] = url_dict
