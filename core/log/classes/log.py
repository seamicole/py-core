# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from datetime import datetime

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.datetime.functions.dtnow import dtnow_utc
from core.datetime.functions.dtto_utc import dtto_utc


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ LOG
# └─────────────────────────────────────────────────────────────────────────────────────


class Log:
    """A log utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        message: str,
        level: int,
        key: str | None = None,
        timestamp: datetime | None = None,
        exception: Exception | None = None,
    ) -> None:
        """Init Method"""

        # Set key
        self.key = key

        # Check if timestamp is None
        if timestamp is None:
            # Get timestamp
            timestamp = dtnow_utc()

        # Otherwise handle existing
        else:
            # Ensure datetime is in UTC
            timestamp = dtto_utc(timestamp)

        # Set timestamp
        self.timestamp = timestamp

        # Set message
        self.message = message

        # Set level
        self.level = level

        # Set exception
        self.exception = exception
