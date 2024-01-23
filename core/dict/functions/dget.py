# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.object.functions.oget import oget
from core.placeholders import nothing


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DGET
# └─────────────────────────────────────────────────────────────────────────────────────


def dget(
    dictionary: dict[Any, Any],
    path: str,
    default: Any = nothing,
    delimiter: str = ".",
) -> Any:
    """Gets a value from a nested dictionary using a path string"""

    # Return value
    return oget(dictionary, path=path, default=default, delimiter=delimiter)
