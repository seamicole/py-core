# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

try:
    import pytz
except ImportError:
    pytz = None  # type: ignore

try:
    from dateutil.tz import tzlocal, tzutc
except ImportError:
    tzlocal = None  # type: ignore

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
        # Check if get tzlocal is None
        if tzlocal is None:
            # Raise an ImportError
            raise ImportError("dateutil is required to use this function")

        # Convert to UTC
        return dt.replace(tzinfo=tzlocal()).astimezone(tzutc())

    # Return converted datetime
    return dt.astimezone(pytz.utc)
