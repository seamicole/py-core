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
# │ NON-EXISTENT KEY ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class NonExistentKeyError(Exception):
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
