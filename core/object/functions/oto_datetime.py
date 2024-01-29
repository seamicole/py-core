# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

try:
    import pytz
except ImportError:
    pytz = None  # type: ignore

from datetime import datetime, tzinfo
from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.object.functions.olower import olower


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OTO DATETIME
# └─────────────────────────────────────────────────────────────────────────────────────


def oto_datetime(
    instance: Any,
    unit: str = "ms",
    tz: tzinfo | None = None,
) -> datetime:
    """Converts an arbitrary object to a datetime object"""

    # Initialize datetime
    dt = None

    # Check if instance is already a datetime
    if isinstance(instance, datetime):
        dt = instance

    # Check if instance is int
    if isinstance(instance, int):
        # Initialize seconds
        seconds: float = float(instance)

        # Get unit lower
        unit_lower = olower(unit)

        # Convert if unit is ms
        if unit_lower == "ms":
            # Convert to seconds
            seconds = instance / 1000.0

        # Set datetime
        dt = datetime.fromtimestamp(seconds)

    # Check if datetime is None
    if dt is None:
        # Raise a TypeError
        raise TypeError("Unsupported type for conversion to datetime")

    # Check if timezone is not None
    if tz is not None:
        # Set timezone
        dt = dt.replace(tzinfo=tz)

    # Return datetime
    return dt


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OTO DATETIME UTC
# └─────────────────────────────────────────────────────────────────────────────────────


def oto_datetime_utc(instance: Any, unit: str = "ms") -> datetime:
    """Converts an arbitrary object to a datetime object with a UTC timezone"""

    # Check if requester is None
    if pytz is None:
        # Raise an ImportError
        raise ImportError("pytz is required to use this function")

    # Return datetime
    return oto_datetime(instance=instance, unit=unit, tz=pytz.utc)
