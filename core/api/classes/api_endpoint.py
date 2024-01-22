# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.types import HTTPMethod

if TYPE_CHECKING:
    from core.api.classes.api import API
    from core.client.classes.http_response import HTTPResponse
    from core.client.types import HTTPMethodLiteral, JSONSchema


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ API ENDPOINT
# └─────────────────────────────────────────────────────────────────────────────────────


class APIEndpoint:
    """An API endpoint utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        api: API,
        path: str,
        method: HTTPMethod | HTTPMethodLiteral | None = None,
        base_url: str | None = None,
        json_path: str | None = None,
        json_schema: JSONSchema | None = None,
    ) -> None:
        """Init Method"""

        # Set API
        self.api = api

        # Set path
        self.path = path

        # Check if method is a string
        if isinstance(method, str):
            # Convert to HTTPMethod
            method = HTTPMethod[method.upper()]

        # Set method
        self.method = method

        # Set base URL
        self.base_url = base_url

        # Set JSON path
        self.json_path = json_path

        # Set JSON schema
        self.json_schema = json_schema

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ URL
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def url(self) -> str:
        """Constructs and returns the API endpoint URL"""

        # Construct and return URL
        return self.api.construct_url(self.path, base_url=self.base_url)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST
    # └─────────────────────────────────────────────────────────────────────────────────

    def request(self) -> HTTPResponse:
        """Makes a synchronous request to the API endpoint"""

        # Make request and return response
        return self.api.request(
            self.method or HTTPMethod.GET,
            self.path,
            base_url=self.base_url,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_async(self) -> HTTPResponse:
        """Makes an asynchronous request to the API endpoint"""

        # Make request and return response
        return await self.api.request_async(
            self.method or HTTPMethod.GET,
            self.path,
            base_url=self.base_url,
        )
