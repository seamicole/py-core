# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.dict.functions.dget import dget
from core.dict.functions.dset import dset
from core.dict.classes.dict_schema_context import DictSchemaContext

if TYPE_CHECKING:
    from core.dict.types import DictSchema


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DFROM SCHEMA
# └─────────────────────────────────────────────────────────────────────────────────────


def dfrom_schema(
    data: dict[Any, Any],
    schema: DictSchema,
    defaults: dict[Any, Any] | None = None,
    delimiter: str = ".",
) -> dict[Any, Any]:
    """Remaps a dictionary using a JSON schema"""

    # Initialize root data
    root_data = data

    # Initialize mapped data
    mapped_data: dict[Any, Any] = defaults or {}

    # Check if JSON schema is not None
    if schema is not None:
        # Iterate over schema
        for setter, getter in (schema or {}).items():
            # Check if getter is callable
            if callable(getter):
                # Get value to set
                value_to_set = getter(DictSchemaContext(data=root_data, item=data))

            # Otherwise handle case of string path
            else:
                # Get value to set
                value_to_set = dget(data, getter, delimiter=delimiter)

            # Set value to set to mapped data
            dset(mapped_data, setter, value_to_set, delimiter=delimiter, insert=True)

    # Return mapped data
    return mapped_data
