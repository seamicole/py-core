# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.placeholders import nothing
from core.dict.functions.dget import dget


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OGET
# └─────────────────────────────────────────────────────────────────────────────────────


def oget(
    instance: object, path: str, default: Any = nothing, delimiter: str = "."
) -> Any:
    """Gets a value from a nested object instance using a path string"""

    # Return value
    return dget(instance.__dict__, path=path, default=default, delimiter=delimiter)
