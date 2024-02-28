# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ INVALID LOG LEVEL ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class InvalidLogLevelError(Exception):
    """Raised when an invalid log level is detected"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, level: int) -> None:
        """Init Method"""

        # Initialize the exception
        super().__init__(f"Invalid log level: {level}")

        # Set the level
        self.level = level
