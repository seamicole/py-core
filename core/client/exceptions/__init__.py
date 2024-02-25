# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

if TYPE_CHECKING:
    from core.client.enums.http_method import HTTPMethod
    from core.client.types import HTTPMethodLiteral


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP STATUS ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class HTTPStatusCodeError(Exception):
    """Raised when a non-200 HTTP status code is detected"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, status: int) -> None:
        """Init Method"""

        # Initialize the exception
        super().__init__(f"HTTP status code: {status}")

        # Set the status
        self.status = status


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ INVALID HTTP METHOD ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class InvalidHTTPMethodError(Exception):
    """Raised when an invalid HTTP method is detected"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, method: HTTPMethod | HTTPMethodLiteral) -> None:
        """Init Method"""

        # Initialize the exception
        super().__init__(f"Invalid HTTP method: {method}")

        # Set the method
        self.method = method
