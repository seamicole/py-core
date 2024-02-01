# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any, Iterable, TypeVar

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.dict.functions.dset import dset
from core.object.functions.oget import oget

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TYPE VARIABLES
# └─────────────────────────────────────────────────────────────────────────────────────

T = TypeVar("T")


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OAGG
# └─────────────────────────────────────────────────────────────────────────────────────


def oagg(
    InstanceClass: type[T],
    instances: Iterable[object | dict[Any, Any]],
    agg_schema: dict[str, Iterable[str]],
    kwargs: dict[str, Any] | None = None,
) -> T:
    """Initialized and returns an aggregate instance from a list of object instances"""

    # Initialize instance kwargs
    instance_kwargs = kwargs or {}

    # Iterate over the aggregate schema
    for key, attrs in agg_schema.items():
        # Iterate over attributes
        for attr in attrs:
            # Initialize values
            values = []

            # Iterate over instances
            for instance in instances:
                # Get value
                value = oget(instance, attr, default=None)

                # Append if value is not None
                if value is not None:
                    values.append(value)

            # Check if values is empty
            if not values:
                value = None

            # Otherwise check if key is first
            elif key == "first":
                value = values[0]

            # Otherwise check if key is last
            elif key == "last":
                value = values[-1]

            # Otherwise check if key is sum
            elif key == "sum":
                value = sum(values)

            # Otherwise check if key is mean
            elif key == "mean":
                value = sum(values) / len(values)

            # Otherwise check if key is min
            elif key == "min":
                value = min(values)

            # Otherwise check if key is max
            elif key == "max":
                value = max(values)

            # Otherwise check if any
            elif key == "any":
                value = any(values)

            # Otherwise check if all
            elif key == "all":
                value = all(values)

            # Otherwise check if concat unique
            elif key.startswith("concat-unique-"):
                # Get separator
                sep = key.split("concat-unique-")[1]

                # Get unique values
                value = sep.join(sorted(set(values)))

            # Otherwise check if concat
            elif key.startswith("concat-"):
                # Get separator
                sep = key.split("concat-")[1]

                # Get unique values
                value = sep.join(values)

            # Otherwise raise error
            else:
                raise ValueError(f"Invalid aggregate key: {key}")

            # Add value to instance kwargs
            dset(instance_kwargs, attr, value, insert=True)

    # Return instance
    return InstanceClass(**instance_kwargs)
