# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from datetime import datetime, timezone


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DTNOW
# └─────────────────────────────────────────────────────────────────────────────────────


def dtnow() -> datetime:
    """Returns a datetime object with the current date and time"""

    # Return datetime
    return datetime.now()


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DTNOW UTC
# └─────────────────────────────────────────────────────────────────────────────────────


def dtnow_utc() -> datetime:
    """Returns a datetime object with the current date and time in UTC"""

    # Return datetime
    return datetime.now(timezone.utc)
