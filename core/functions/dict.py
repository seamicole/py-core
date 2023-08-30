# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.placeholders import Nothing

if TYPE_CHECKING:
    from core.types import JSONSchema


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DFROM SCHEMA
# └─────────────────────────────────────────────────────────────────────────────────────


def dfrom_schema(data: dict[Any, Any], schema: JSONSchema) -> dict[Any, Any]:
    """Remaps a dictionary using a schema"""

    # Initialize root data
    root_data = data

    # Initialize mapped data
    mapped_data: dict[Any, Any] = {}

    # Check if schema is not None
    if schema is not None:
        # Iterate over schema
        for setter, getter in (schema or {}).items():
            # Check if getter is callable
            if callable(getter):
                # Get value to set
                value_to_set = getter(root_data, data)

            # Otherwise handle case of string path
            else:
                # Get value to set
                value_to_set = dget(data, getter, delimiter=".")

            # Check if the setter is a tuple
            if isinstance(setter, tuple):
                # Check if the value to set is not a tuple or list
                if not isinstance(value_to_set, (tuple, list)):
                    # Convert value to set to a list
                    value_to_set = [value_to_set] * len(setter)

                # Iterate over zip of setter and value to set
                for setter_item, value_to_set_item in zip(setter, value_to_set):
                    # Remap data
                    dset(mapped_data, setter_item, value_to_set_item)

            # Otherwise, simply remap data
            else:
                # Remap data
                dset(mapped_data, setter, value_to_set)

    # Return mapped data
    return mapped_data


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DGET
# └─────────────────────────────────────────────────────────────────────────────────────


def dget(
    dictionary: dict[Any, Any], path: str, default: Any = Nothing, delimiter: str = "."
) -> Any:
    """Gets a value from a nested dictionary using a path string"""

    # Initialize value
    value = default

    # Iterate over keys
    for key in path.split(delimiter):
        # Check if key exists or no default is given
        if key in dictionary or default is Nothing:
            # Get value by key and set dictionary
            value = dictionary = dictionary[key]

        # Otherwise return default
        else:
            return default

    # Return value
    return value


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DPOP
# └─────────────────────────────────────────────────────────────────────────────────────


def dpop(
    dictionary: dict[Any, Any], path: str, default: Any = Nothing, delimiter: str = "."
) -> Any:
    """Pops a value from a nested dictionary using a path string"""

    # Split the path into keys
    keys = path.split(delimiter)

    # Initialize value
    value = default

    # Iterate over keys
    for key in keys[:-1]:
        # Check if key exists or no default is given
        if key in dictionary or default is Nothing:
            # Get value by key and set dictionary
            dictionary = dictionary[key]

        # Otherwise return default
        else:
            return default

    # Check if key exists or no default is given
    if keys[-1] in dictionary or default is Nothing:
        # Pop value by last key
        value = dictionary.pop(keys[-1])

    # Return value
    return value


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DSET
# └─────────────────────────────────────────────────────────────────────────────────────


def dset(
    dictionary: dict[Any, Any], path: str, value: Any, delimiter: str = "."
) -> None:
    """Sets a value in a nested dictionary using a path string"""

    # Split the path into keys
    keys = path.split(delimiter)

    # Iterate over keys
    for key in keys[:-1]:
        # Check if key exists
        if key not in dictionary:
            # Set key to empty dictionary
            dictionary[key] = {}

        # Get value by key
        dictionary = dictionary[key]

    # Set value by last key
    dictionary[keys[-1]] = value
