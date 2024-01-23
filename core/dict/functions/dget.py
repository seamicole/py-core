# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.placeholders import nothing


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DGET
# └─────────────────────────────────────────────────────────────────────────────────────


def dget(
    dictionary: dict[Any, Any], path: str, default: Any = nothing, delimiter: str = "."
) -> Any:
    """Gets a value from a nested dictionary using a path string"""

    # Initialize value
    value = default

    # Iterate over keys
    for key in path.split(delimiter):
        # Check if key exists or no default is given
        if key in dictionary or default == nothing:
            # Get value by key and set dictionary
            value = dictionary = dictionary[key]

            # Check if not a dictionary
            if not isinstance(dictionary, dict) and hasattr(dictionary, "__dict__"):
                # Set dictionary
                dictionary = dictionary.__dict__

        # Otherwise return default
        else:
            return default

    # Return value
    return value
