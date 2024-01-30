# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OHASATTR
# └─────────────────────────────────────────────────────────────────────────────────────


def ohasattr(
    instance: object | dict[Any, Any], path: str, delimiter: str = "."
) -> bool:
    """Returns a boolean of whether or not an object has an attribute"""

    # Iterate over keys
    for key in path.split(delimiter):
        # Check if dict
        if isinstance(instance, dict):
            # Return if key does not exist
            if key not in instance:
                return False

            # Set instance
            instance = instance[key]

        # Otherwise handle object
        else:
            # Return if attribute does not exist
            if not hasattr(instance, key):
                return False

            # Set instance
            instance = getattr(instance, key)

    # Return True
    return True
