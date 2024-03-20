# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any, TypeVar

try:
    from beartype.door import is_bearable
except ImportError:
    is_bearable = None  # type: ignore

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TYPE VARIABLES
# └─────────────────────────────────────────────────────────────────────────────────────

T = TypeVar("T")


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ASSERT ISINSTANCE
# └─────────────────────────────────────────────────────────────────────────────────────


def assert_isinstance(obj: T, obj_type: Any, name: str | None = None) -> T:
    """Raises a TypeError if object is not an instance of a type"""

    # Initialize is instance
    is_instance = False

    # Initialize try-except block
    try:
        # Check if is instance
        is_instance = isinstance(obj, obj_type)

    # Handle TypeError
    except TypeError:
        # Check if is bearable is None
        if is_bearable is None:
            # Raise an ImportError
            raise ImportError("beartype is required to use this function")

        # Check if bearable
        is_instance = is_bearable(obj, obj_type)

    # Check if is instance is False
    if is_instance is False:
        # Raise a TypeError
        raise TypeError(
            f"{name + ': ' if name is not None else ''}"
            f"{type(obj)} is not of type {obj_type}"
        )

    # Return object
    return obj
