# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.clients.classes.api import API
from core.clients.classes.api_endpoint import APIEndpoint

if TYPE_CHECKING:
    from core.types import Args, JSONSchema, Kwargs


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ API MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class APIMixin:
    """A mixin for classes with API-related attributes and methods"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of API
    api: API

    # Initialize API base URL
    API_BASE_URL: str = ""

    # Initialize API endpoints
    API_ENDPOINTS: list[dict[str, str | JSONSchema]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, *args: Args, **kwargs: Kwargs) -> None:
        """Init Method"""

        # Call super init method
        super().__init__(*args, **kwargs)

        # Initialize and set API
        self.api = API(base_url=self.API_BASE_URL)

        # Initialize API endpoints
        if not hasattr(self, "API_ENDPOINTS"):
            self.API_ENDPOINTS = []

        # Iterate over API endpoints
        for api_endpoint_dict in self.API_ENDPOINTS:
            # Initialize an APIEndpoint instance
            api_endpoint = APIEndpoint.from_dict({**api_endpoint_dict, "api": self.api})

            # Push API endpoint
            api_endpoint.push()
