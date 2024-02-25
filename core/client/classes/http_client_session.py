# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import time

from multiprocessing import Manager
from multiprocessing.managers import DictProxy, SyncManager
from typing import Literal, TYPE_CHECKING
from typing_extensions import TypedDict

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

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
    _usage: DictProxy[Literal["wt"] | Literal["ts"], int | float]

    # Declare type of requests
    _requests: DictProxy[str, dict[str, HTTPClientSession.RequestLog]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, manager: SyncManager | None = None) -> None:
        """Init Method"""

        # Initialize a manager
        self._manager = manager or Manager()

        # Initialize lock
        self._lock = self._manager.Lock()

        # Initialize usage
        self._usage = self._manager.dict({"wt": 0, "ts": time.time()})

        # Initialize requests
        self._requests = self._manager.dict()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LOG REQUEST
    # └─────────────────────────────────────────────────────────────────────────────────

    def log_request(self, weight: int, interval: float | None = None) -> None:
        """Logs an HTTP client request"""

        # Return if no interval
        if interval is None:
            return

        # Get ts
        ts = time.time()

        # Check if one second elapsed
        if ts - self._usage["ts"] >= interval:
            # Reset usage
            self._usage["wt"] = 0
            self._usage["ts"] = ts

        # Increment weight
        self._usage["wt"] += weight

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LOG RESPONSE
    # └─────────────────────────────────────────────────────────────────────────────────

    def log_response(self, response: HTTPResponse) -> None:
        """Logs an HTTP client response"""

        # Get request
        request = response.request

        # Get HTTP method key
        method_key = request.method.value

        # Initialize lock
        with self._lock:
            # Get URL dict
            url_dict = self._requests.setdefault(request.url, {})

            # Get method dict
            method_dict = url_dict.setdefault(
                method_key, {"reqs": {}, "rets": {}, "errs": {}}
            )

            # Get reqs dict
            reqs_dict = method_dict["reqs"]

            # Get status code
            status_code = response.status_code

            # Add request status code to requests
            reqs_dict[status_code] = reqs_dict.get(status_code, 0) + 1

            # Check if retry
            if request.is_retry:
                # Get rets dict
                rets_dict = method_dict["rets"]

                # Add request status code to requests
                rets_dict[status_code] = rets_dict.get(status_code, 0) + 1

            # Check if is error
            if not response.did_succeed and response.text_stripped:
                # Get errs dict
                errs_dict = method_dict["errs"]

                # Add error message
                errs_dict.setdefault(status_code, set()).add(response.text_stripped)

            # Set URL dict
            self._requests[request.url] = url_dict
