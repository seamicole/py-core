# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

try:
    import pytz
except ImportError:
    pytz = None  # type: ignore

from datetime import datetime


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DTTO UTC
# └─────────────────────────────────────────────────────────────────────────────────────


def dtto_utc(dt: datetime) -> datetime:
    """Converts a datetime object to a timezone-aware datetime object in UTC"""

    # Check if requester is None
    if pytz is None:
        # Raise an ImportError
        raise ImportError("pytz is required to use this function")

    # Check if timezone is None
    if dt.tzinfo is None:
        return pytz.utc.localize(dt)

    # Return converted datetime
    return dt.astimezone(pytz.utc)
