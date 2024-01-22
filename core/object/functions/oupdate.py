# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

if TYPE_CHECKING:
    from core.dict.types import DictSchema


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OUPDATE
# └─────────────────────────────────────────────────────────────────────────────────────


def oupdate(
    instance_dst: object,
    instance_src: object,
    schema: DictSchema | None = None,
) -> None:
    """Updates an instance with the values from another instance"""

    # Get source dictionary
    src_dict = {
        k: v
        for k, v in instance_src.__dict__.items()
        if k in instance_dst.__dict__ and (schema is None or k in schema)
    }

    # Update destination instance
    instance_dst.__dict__.update(src_dict)
