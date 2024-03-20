# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

if TYPE_CHECKING:
    from core.client.classes.http_request import HTTPRequest
    from core.client.classes.http_response import HTTPResponse


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP TRANSACTION
# └─────────────────────────────────────────────────────────────────────────────────────


class HTTPTransaction:
    """An HTTP receipt utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, response: HTTPResponse) -> None:
        """Init Method"""

        # Set response
        self.response = response

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ DID SUCCEED
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def did_succeed(self) -> bool:
        """Returns a boolean of whether the transaction succeeded"""

        # Return response did succeed
        return self.response.did_succeed

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ MESSAGE
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def message(self) -> str:
        """Returns a message associated with the response"""

        # Get response JSON
        response_json = self.response.json

        # Check if response JSON is not None
        if response_json is not None:
            # Get keys
            keys = {k.lower(): k for k in response_json}

            # Iterate over possible message keys
            for key in ("info", "message", "msg"):
                # Check if key in keys
                if key in keys:
                    return str(response_json[keys[key]])

        # Return empty string
        return ""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def request(self) -> HTTPRequest:
        """Returns the HTTP request"""

        # Return request
        return self.response.request

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ STATUS CODE
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def status_code(self) -> int:
        """Returns the response status code"""

        # Return response status code
        return self.response.status_code
