# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.types import JSONSchema
from core.dict.functions.dget import dget
from core.dict.functions.dset import dset


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DFROM SCHEMA
# └─────────────────────────────────────────────────────────────────────────────────────


def dfrom_schema(
    data: dict[Any, Any],
    schema: JSONSchema,
    defaults: dict[Any, Any] | None = None,
    delimiter: str = ".",
) -> dict[Any, Any]:
    """Remaps a dictionary using a schema"""

    # Initialize root data
    root_data = data

    # Initialize mapped data
    mapped_data: dict[Any, Any] = defaults or {}

    # Check if schema is not None
    if schema is not None:
        # Iterate over schema
        for setter, getter in (schema or {}).items():
            # Check if getter is callable
            if callable(getter):
                # Get value to set
                value_to_set = getter(root_data, data)

            # Otherwise handle case of string path
            else:
                # Get value to set
                value_to_set = dget(data, getter, delimiter=delimiter)

            # Set value to set to mapped data
            dset(mapped_data, setter, value_to_set, delimiter=delimiter)

    # Return mapped data
    return mapped_data
