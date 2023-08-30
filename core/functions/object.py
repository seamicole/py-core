# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any, Generator, TypeVar

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.functions.dict import dfrom_schema, dget
from core.placeholders import Nothing
from core.types import JSONSchema

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TYPE VARIABLES
# └─────────────────────────────────────────────────────────────────────────────────────

T = TypeVar("T")


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OFROM DICT
# └─────────────────────────────────────────────────────────────────────────────────────


def ofrom_dict(Class: type[T], data: dict[Any, Any]) -> T:
    """Initializes an item from a dictionary"""

    # Initialize item
    item = Class(**data)

    # Return item
    return item


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OFROM JSON
# └─────────────────────────────────────────────────────────────────────────────────────


def ofrom_json(
    Class: type[T], data: Any, path: str | None = None, schema: JSONSchema | None = None
) -> Generator[T, None, None]:
    """Initializes an item from a JSON object"""

    # Check if should get data from path
    if isinstance(data, dict) and path is not None:
        # Get data from path
        data = dget(data, path, delimiter=".")

    # Check if data is a dictionary
    if isinstance(data, dict):
        # Convert to list
        data = [data]

    # Check if data is a list
    if isinstance(data, list):
        # Iterate over data
        for item in data:
            # Check if schema is not None
            if schema is not None:
                # Get item from schema
                item = dfrom_schema(item, schema=schema)

            # Yield item from dictionary
            yield ofrom_dict(Class=Class, data=item)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OGET
# └─────────────────────────────────────────────────────────────────────────────────────


def oget(obj: Any, path: str, default: Any = Nothing, delimiter: str = ".") -> Any:
    """Gets a nest value from a Python object using a path string"""

    # Initialize value
    value = default

    # Iterate over attributes
    for attr in path.split(delimiter):
        # Check if object has attribute or no default is given
        if hasattr(obj, attr) or default is Nothing:
            # Get attribute and set object
            value = obj = getattr(obj, attr)

        # Otherwise return default
        else:
            return default

    # Return value
    return value
