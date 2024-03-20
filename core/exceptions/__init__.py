# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ INVALID SCHEMA ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class InvalidSchemaError(Exception):
    """An exception class for invalid schemas"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, message: str | None = None):
        """Init Method"""

        # Initialize message
        self.message = "Invalid Schema"

        # Check if message
        if message:
            self.message = f"{self.message}: {message}"

        # Call super init
        super().__init__(self.message)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ UNSUCCESSFUL ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class UnsuccessfulError(Exception):
    """An exception class for unsuccessful events"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize label
    LABEL: str | None = None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, message: Any = None):
        """Init Method"""

        # Initialize message
        self.message = "Unsuccessful"

        # Check if label is not None
        if self.LABEL is not None:
            self.message = f"{self.message} {self.LABEL}"

        # Check if message is not None
        if message is not None:
            message = message if isinstance(message, str) else repr(message)
            self.message = f"{self.message}: {message}"

        # Call super init
        super().__init__(self.message)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ UNSUCCESSFUL ACTION ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class UnsuccessfulActionError(UnsuccessfulError):
    """An exception class for unsuccessful actions"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Define label
    LABEL: str | None = "Action"


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ UNSUPPORTED ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class UnsupportedError(Exception):
    """An exception class for unsupported inputs"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize label
    LABEL: str | None = None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, message: Any = None):
        """Init Method"""

        # Initialize message
        self.message = "Unsupported"

        # Check if label is not None
        if self.LABEL is not None:
            self.message = f"{self.message} {self.LABEL}"

        # Check if message is not None
        if message is not None:
            message = message if isinstance(message, str) else repr(message)
            self.message = f"{self.message}: {message}"

        # Call super init
        super().__init__(self.message)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ UNSUPPORTED ACTION ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class UnsupportedActionError(UnsupportedError):
    """An exception class for unsupported actions"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Define label
    LABEL: str | None = "Action"
