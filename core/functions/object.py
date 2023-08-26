# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any, TypeVar

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.placeholders import Nothing


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OFROM DICT
# └─────────────────────────────────────────────────────────────────────────────────────

T = TypeVar("T")


def ofrom_dict(Class: type[T], data: dict[Any, Any]) -> T:
    """Initializes an item from a dictionary"""

    # Initialize kwargs
    kwargs = data

    # Initialize item
    item = Class(**kwargs)

    # Return item
    return item


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
