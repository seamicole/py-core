# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DICT SCHEMA CONTEXT
# └─────────────────────────────────────────────────────────────────────────────────────


class DictSchemaContext:
    """A context class for the DictSchema callable"""

    # Declare type of data
    data: Any

    # Declare type of item
    item: dict[Any, Any]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, data: Any, item: dict[Any, Any] | None = None):
        """Init Method"""

        # Set data
        self.data = data

        # Set item
        self.item = item or {}
