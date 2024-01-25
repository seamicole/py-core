# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ LOWERCASE
# └─────────────────────────────────────────────────────────────────────────────────────


def lowercase(instance: Any) -> Any:
    """Lowercases an object"""

    # Check if instance is a string
    if isinstance(instance, str):
        # Lowercase instance
        instance = instance.lower()

    # Otherwise check if sequence
    elif isinstance(instance, (list, tuple)):
        # Lowercase each item in the instance
        instance = type(instance)([lowercase(i) for i in instance])

    # Return instance
    return instance
