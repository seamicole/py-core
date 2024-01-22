# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import asyncio

from typing import Any, AsyncGenerator, Generator

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.api.classes.api_endpoint import APIEndpoint
from core.client.types import JSONDict, JSONSchema
from core.collection.classes.dict_collection import DictCollection


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ API ENDPOINT COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class APIEndpointCollection(DictCollection[APIEndpoint]):
    """A dict-based collection utility class for APIEndpoint instances"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST DICTS
    # └─────────────────────────────────────────────────────────────────────────────────

    def request_dicts(self) -> Generator[tuple[JSONDict, JSONSchema], None, None]:
        """Yields a series of object dicts for all APIEndpoints in the collection"""

        # Iterate over endpoints
        for endpoint in self:
            # Get JSON path and schema
            json_path = endpoint.json_path
            json_schema = endpoint.json_schema

            # Continue if path or JSON schema is None
            if json_schema is None:
                continue

            # Make request
            response = endpoint.request()

            # Iterate over items
            for item in response.yield_dicts(
                json_path=json_path, json_schema=json_schema
            ):
                yield (item, json_schema)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST DICTS ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_dicts_async(
        self,
    ) -> AsyncGenerator[tuple[JSONDict, JSONSchema], None]:
        """Yields a series of object dicts for all APIEndpoints in the collection"""

        # Initialize requests
        requests = []

        # Initialize JSON arguments
        json_arguments = []

        # Iterate over endpoints
        for endpoint in self:
            # Get JSON path and schema
            json_path = endpoint.json_path
            json_schema = endpoint.json_schema

            # Continue if path or JSON schema is None
            if json_schema is None:
                continue

            # Append to requests
            requests.append(endpoint.request_async())

            # Append to JSON arguments
            json_arguments.append((json_path, json_schema))

        # Iterate over requests
        for response, (json_path, json_schema) in zip(
            await asyncio.gather(*requests), json_arguments
        ):
            # Iterate over items
            for item in response.yield_dicts(
                json_path=json_path, json_schema=json_schema
            ):
                yield (item, json_schema)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST INSTANCES
    # └─────────────────────────────────────────────────────────────────────────────────

    def request_instances(
        self, InstanceClass: type
    ) -> Generator[tuple[Any, JSONSchema], None, None]:
        """Yields a series of object instances for all APIEndpoints in the collection"""

        # Iterate over items
        for item, json_schema in self.request_dicts():
            # Initialize and yield instance
            yield (InstanceClass(**item), json_schema)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REQUEST INSTANCES ASYNC
    # └─────────────────────────────────────────────────────────────────────────────────

    async def request_instances_async(
        self, InstanceClass: type
    ) -> AsyncGenerator[tuple[Any, JSONSchema], None]:
        """Yields a series of object instances for all APIEndpoints in the collection"""

        # Iterate over items
        async for item, json_schema in self.request_dicts_async():
            # Initialize and yield instance
            yield (InstanceClass(**item), json_schema)
