# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.placeholders import nothing


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OGET
# └─────────────────────────────────────────────────────────────────────────────────────


def oget(
    instance: object | dict[Any, Any],
    path: str,
    default: Any = nothing,
    delimiter: str = ".",
) -> Any:
    """Gets a value from a nested object instance using a path string"""

    # Initialize value
    value = default

    # Iterate over keys
    for key in path.split(delimiter):
        # Check if dict
        if isinstance(instance, dict):
            # Check if key exists or no default is given
            if key in instance or default is nothing:
                # Get value by key and set dictionary
                value = instance = instance[key]

            # Otherwise return default
            else:
                return default

        # Otherwise handle object
        else:
            # Check if attribute exists or no default is given
            if hasattr(instance, key) or default is nothing:
                # Get value by attribute and set instance
                value = instance = getattr(instance, key)

            # Otherwise return default
            else:
                return default

    # Return value
    return value
