# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.object.functions.oset import oset


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DSET
# └─────────────────────────────────────────────────────────────────────────────────────


def dset(
    dictionary: dict[Any, Any],
    path: Any,
    value: Any,
    delimiter: str = ".",
    insert: bool = False,
) -> None:
    """Sets a value in a nested dictionary using a path string"""

    # Return value
    return oset(dictionary, path=path, value=value, delimiter=delimiter, insert=insert)
