# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing_extensions import NotRequired, TypedDict

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.api.classes.api import API
from core.client.enums.http_method import HTTPMethod
from core.client.types import HTTPMethodLiteral, JSONSchema


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ API MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class APIMixin:
    """An API mixin class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TYPE ALIASES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Define an endpoint type alias
    class Endpoint(TypedDict):
        method: HTTPMethod | HTTPMethodLiteral
        path: str
        base_url: NotRequired[str]
        json_body: NotRequired[str]
        json_schema: NotRequired[JSONSchema]

    # Define an endpoint list type alias
    Endpoints = list[Endpoint] | None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of API base URL
    API_BASE_URL: str

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize API cache
    _api: API | None = None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ API
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def api(self) -> API:
        """Returns a cached or initialized API instance"""

        # Check if cached API instance is None
        if self._api is None:
            # Initialize and set API instance
            self._api = API(base_url=self.API_BASE_URL)

        # Return cached API instance
        return self._api
