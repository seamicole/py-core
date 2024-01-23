# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.dict.functions.dset import dset


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OSET
# └─────────────────────────────────────────────────────────────────────────────────────


def oset(
    instance: object, path: Any, value: Any, delimiter: str = ".", insert: bool = False
) -> None:
    """Sets a value in a nested object using a path string"""

    # Return value
    return dset(
        instance.__dict__, path=path, value=value, delimiter=delimiter, insert=insert
    )
