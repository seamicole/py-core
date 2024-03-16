# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DUPLICATE KEY ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class DuplicateKeyError(Exception):
    """Raised when a resource with duplicate key is detected"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, key_value: Any) -> None:
        """Init Method"""

        # Initialize the exception
        super().__init__(f"Duplicate key detected: {key_value!r}")

        # Set the key value
        self.key_value = key_value


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ MUTIPLE ITEMS ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class MultipleItemsError(Exception):
    """Raised when multiple items are detected"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, item_count: int) -> None:
        """Init Method"""

        # Initialize the exception
        super().__init__(f"Multiple items found: {item_count!r}")

        # Set the item count
        self.item_count = item_count


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ NO ITEMS ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class NoItemsError(Exception):
    """Raised when no items are detected"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        """Init Method"""

        # Initialize the exception
        super().__init__("No items found")


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ NON-EXISTENT KEY ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class NonExistentKeyError(KeyError):
    """Raised when no resource with given key is detected"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, key_value: Any) -> None:
        """Init Method"""

        # Initialize the exception
        super().__init__(f"Non-existent key detected: {key_value!r}")

        # Set the key value
        self.key_value = key_value
