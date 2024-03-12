# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

try:
    import pytz
except ImportError:
    pytz = None  # type: ignore

try:
    from tzlocal import get_localzone
except ImportError:
    get_localzone = None  # type: ignore

from datetime import datetime


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DTTO UTC
# └─────────────────────────────────────────────────────────────────────────────────────


def dtto_utc(dt: datetime) -> datetime:
    """Converts a datetime object to a timezone-aware datetime object in UTC"""

    # Check if pytz is None
    if pytz is None:
        # Raise an ImportError
        raise ImportError("pytz is required to use this function")

    # Check if timezone is None
    if dt.tzinfo is None:
        # Check if get localzone is None
        if get_localzone is None:
            # Raise an ImportError
            raise ImportError("pytz is required to use this function")

        # Convert to UTC
        return get_localzone().localize(dt).astimezone(pytz.utc)

    # Return converted datetime
    return dt.astimezone(pytz.utc)
