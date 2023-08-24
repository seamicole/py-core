# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from enum import Enum


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP METHOD
# └─────────────────────────────────────────────────────────────────────────────────────


class HTTPMethod(Enum):
    """An enum class that represents the HTTP methods"""

    # Define DELETE enum
    DELETE = "DELETE"

    # Define GET enum
    GET = "GET"

    # Define PATCH enum
    PATCH = "PATCH"

    # Define POST enum
    POST = "POST"

    # Define PUT enum
    PUT = "PUT"
