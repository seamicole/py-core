# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from datetime import datetime, tzinfo
from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.datetime.functions.dtto_utc import dtto_utc
from core.object.functions.olower import olower


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OTO DATETIME
# └─────────────────────────────────────────────────────────────────────────────────────


def oto_datetime(instance: Any, unit: str = "ms", tz: tzinfo | None = None) -> datetime:
    """Converts an arbitrary object to a datetime object"""

    # Initialize datetime
    dt = None

    # Check if instance is already a datetime
    if isinstance(instance, datetime):
        dt = instance

    # Check if string
    if isinstance(instance, str):
        # Check if is digit
        if instance.isdigit():
            # Convert to int
            instance = int(instance)

    # Check if instance is int
    if isinstance(instance, int) or isinstance(instance, float):
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

    # Otherwise, check if instance is str
    elif isinstance(instance, str):
        # Iterate over common datetime formats
        for fmt in [
            "%Y-%m-%d %H:%M:%S.%f%z",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d %H",
            "%Y-%m-%d",
            "%Y-%m",
            "%Y",
        ]:
            try:
                # Set datetime
                dt = datetime.strptime(instance, fmt)
                break
            except ValueError:
                dt = None

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


def oto_datetime_utc(
    instance: Any, unit: str = "ms", tz: tzinfo | None = None
) -> datetime:
    """Converts an arbitrary object to a datetime object with a UTC timezone"""

    # Return datetime
    return dtto_utc(oto_datetime(instance=instance, unit=unit, tz=tz))
