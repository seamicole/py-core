# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, TYPE_CHECKING
from typing_extensions import NotRequired, TypedDict

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.api.classes.api import API
from core.api.classes.api_channel import APIChannel
from core.api.classes.api_channel_event import APIChannelEvent
from core.api.classes.api_endpoint import APIEndpoint
from core.api.classes.api_endpoint_collection import APIEndpointCollection
from core.client.enums.http_method import HTTPMethod
from core.client.types import HTTPMethodLiteral, JSONFilter, JSONSchema

if TYPE_CHECKING:
    from core.client.classes.http_request import HTTPRequest


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CHANNEL EVENT
# └─────────────────────────────────────────────────────────────────────────────────────


# Define a channel event type alias
class ChannelEvent(TypedDict):
    data: NotRequired[JSONSchema]
    json_path: NotRequired[str]
    json_filter: NotRequired[JSONFilter]
    json_schema: NotRequired[JSONSchema]


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
        json: NotRequired[dict[str, Any]]
        json_path: NotRequired[str]
        json_filter: NotRequired[JSONFilter]
        json_schema: NotRequired[JSONSchema]
        params: NotRequired[dict[str, Any]]
        params_schema: NotRequired[dict[str, str]]
        weight: NotRequired[int]
        authenticate: NotRequired[bool]

    # Define an endpoint list type alias
    Endpoints = list[Endpoint] | None

    # Define a channel type alias
    class Channel(TypedDict):
        subscribe: ChannelEvent
        unsubscribe: ChannelEvent

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of API base URL
    API_BASE_URL: str

    # Declare type of API weight per second
    API_WEIGHT_PER_SECOND: int | float | None

    # Declare type of API WS URI
    API_WS_URI: str | None

    # Declare type of API WS ping data
    API_WS_PING_DATA: str | dict[str, Any] | None

    # Declare type of API WS ping interval ms
    API_WS_PING_INTERVAL_MS: int | None

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

        # Return if API instance is cached
        if self._api is not None:
            return self._api

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ ENDPOINTS
        # └─────────────────────────────────────────────────────────────────────────────

        # Get logger key
        logger_key = f"{self.__class__.__name__}.{hex(id(self))}.api"

        # Initialize and set API instance
        self._api = API(
            base_url=self.API_BASE_URL,
            weight_per_second=getattr(self, "API_WEIGHT_PER_SECOND", None),
            ws_uri=getattr(self, "API_WS_URI", None),
            ws_ping_data=getattr(self, "API_WS_PING_DATA", None),
            ws_ping_interval_ms=getattr(self, "API_WS_PING_INTERVAL_MS", 30000),
            logger_key=logger_key,
            authenticate_request=self.authenticate_request,
        )

        # Get endpoint attributes
        endpoint_attrs = [
            attr
            for attr in dir(self)
            if attr.startswith("API_") and attr.endswith("_ENDPOINT")
        ]

        # Iterate over endpoint attributes
        for endpoint_attr in endpoint_attrs:
            # Get endpoint
            endpoint = getattr(self, endpoint_attr)

            # Continue if null
            if not endpoint:
                continue

            # Get endpoint kwargs
            endpoint_kwargs = {**endpoint}

            # Add API to kwargs
            endpoint_kwargs["api"] = self._api

            # Initialize endpoint
            endpoint = APIEndpoint(**endpoint_kwargs)

            # Add endpoint to API endpoints
            self._api.endpoints.find_or_add(endpoint)

            # Set endpoint
            setattr(self._api, endpoint_attr.lower()[4:], endpoint)

        # Get endpoint attributes
        endpoint_attrs = [
            attr
            for attr in dir(self)
            if attr.startswith("API_") and attr.endswith("_ENDPOINTS")
        ]

        # Iterate over endpoint attributes
        for endpoint_attr in endpoint_attrs:
            # Initialize endpoint collection
            endpoint_collection = APIEndpointCollection()

            # Create endpoint collection
            setattr(
                self._api,
                endpoint_attr.lower()[4:],
                endpoint_collection,
            )

            # Get endpoints
            endpoints = getattr(self, endpoint_attr)

            # Contine if not an iterable
            if not isinstance(endpoints, Iterable):
                continue

            # Iterate over endpoints
            for endpoint in endpoints:
                # Continue if null
                if not endpoint:
                    continue

                # Get endpoint kwargs
                endpoint_kwargs = {**endpoint}

                # Add API to kwargs
                endpoint_kwargs["api"] = self._api

                # Initialize endpoint
                endpoint = APIEndpoint(**endpoint_kwargs)

                # Add endpoint to API endpoints
                self._api.endpoints.find_or_add(endpoint)

                # Add endpoint to endpoint collection
                endpoint_collection.add(endpoint)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CHANNELS
        # └─────────────────────────────────────────────────────────────────────────────

        # Get channel attributes
        channel_attrs = [
            attr
            for attr in dir(self)
            if attr.startswith("API_") and attr.endswith("_CHANNEL")
        ]

        # Iterate over channel attributes
        for channel_attr in channel_attrs:
            # Get events
            events = getattr(self, channel_attr)

            # Continue if null
            if not events:
                continue

            # Initialize channel
            channel = APIChannel(api=self._api)

            # Add channel to API channels
            self._api.channels.find_or_add(channel)

            # Iterate over events
            for event_key, event_kwargs in events.items():
                # Add key and channel to kwargs
                event_kwargs["key"] = event_key
                event_kwargs["channel"] = channel

                # Initialize event
                event = APIChannelEvent(**event_kwargs)

                # Add channel to API channels
                channel.events.find_or_add(event)

            # Set channel
            setattr(self._api, channel_attr.lower()[4:], channel)

        # Return cached API instance
        return self._api

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ AUTHENTICATE REQUEST
    # └─────────────────────────────────────────────────────────────────────────────────

    def authenticate_request(self, request: HTTPRequest) -> HTTPRequest:
        """Authenticates a request before being sent"""

        # Return request
        return request
