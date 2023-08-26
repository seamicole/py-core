# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.placeholders import Nothing


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
