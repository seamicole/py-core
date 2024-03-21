# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ LABEL EXCEPTION
# └─────────────────────────────────────────────────────────────────────────────────────


class LabelException(Exception):
    """An exception class for labeled exceptions"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize adjective
    ADJECTIVE: str = "Unknown"

    # Initialize label
    LABEL: str | None = None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, message: Any = None):
        """Init Method"""

        # Initialize message
        self.message = self.ADJECTIVE

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
# │ INVALID ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class InvalidError(LabelException):
    """An exception class for invalid inputs"""

    # Define adjective
    ADJECTIVE: str = "Invalid"


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ INVALID ARGUMENT ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class InvalidArgumentError(InvalidError):
    """An exception class for invalid arguments"""

    # Define label
    LABEL: str = "Argument"


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ INVALID SCHEMA ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class InvalidSchemaError(InvalidError):
    """An exception class for invalid schemas"""

    # Define label
    LABEL: str = "Schema"


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ UNSUCCESSFUL ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class UnsuccessfulError(LabelException):
    """An exception class for unsuccessful events"""

    # Define adjective
    ADJECTIVE: str = "Unsuccessful"


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ UNSUCCESSFUL ACTION ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class UnsuccessfulActionError(UnsuccessfulError):
    """An exception class for unsuccessful actions"""

    # Define label
    LABEL: str | None = "Action"


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ UNSUPPORTED ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class UnsupportedError(LabelException):
    """An exception class for unsupported inputs"""

    # Define adjective
    ADJECTIVE: str = "Unsupported"


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ UNSUPPORTED ACTION ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class UnsupportedActionError(UnsupportedError):
    """An exception class for unsupported actions"""

    # Define label
    LABEL: str | None = "Action"
