# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.placeholders.classes.nothing import Nothing
from core.object.functions.oget import oget
from core.object.functions.oset import oset

if TYPE_CHECKING:
    from core.dict.types import DictSchema


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OUPDATE
# └─────────────────────────────────────────────────────────────────────────────────────


def oupdate(
    instance_dst: object,
    instance_src: object,
    schema: DictSchema | None = None,
    delimiter: str = ".",
) -> None:
    """Updates an instance with the values from another instance"""

    # Initialize an unfound instance
    unfound = Nothing()

    # Iterate over the schema
    for key in schema or instance_src.__dict__:
        # Get keys
        keys = key if isinstance(key, (tuple, list)) else (key,)

        # Iterate over keys
        for key in keys:
            # Get new value
            new_value = oget(
                instance_src, path=key, default=unfound, delimiter=delimiter
            )

            # Continue if new value is not found
            if new_value is unfound:
                continue

            # Get old value
            old_value = oget(
                instance_dst, path=key, default=unfound, delimiter=delimiter
            )

            # Continue if old value is not found
            if old_value is unfound:
                continue

            # Set value
            oset(
                instance_dst,
                path=key,
                value=new_value,
                delimiter=delimiter,
                insert=False,
            )
