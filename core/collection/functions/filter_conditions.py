# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any, Callable, Generator

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collection.functions.filter_checkers import (
    check_contains,
    check_icontains,
    check_eq,
    check_gt,
    check_gte,
    check_lt,
    check_lte,
    check_ieq,
    check_iin,
    check_in,
)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OPERATORS
# └─────────────────────────────────────────────────────────────────────────────────────

# Define operators
OPERATORS = (
    ("__contains", 10, check_contains),
    ("__icontains", 11, check_icontains),
    ("__eq", 4, check_eq),
    ("__gt", 4, check_gt),
    ("__gte", 5, check_gte),
    ("__lt", 4, check_lt),
    ("__lte", 5, check_lte),
    ("__ieq", 5, check_ieq),
    ("__in", 4, check_in),
    ("__iin", 5, check_iin),
)

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GET FILTER CONDITION
# └─────────────────────────────────────────────────────────────────────────────────────


def get_filter_condition(
    key: str, value: Any
) -> tuple[str, Any, str, Callable[[Any, Any], bool]]:
    """Returns a filter condition tuple based on a key and value"""

    # Iterate over operators
    for operator, char_count, checker in OPERATORS:
        # Check if key ends with operator
        if key.endswith(operator):
            # Return filter condition
            return (key[:-char_count], value, "__gte", checker)

    # Return equality condition as default
    return (key, value, "__eq", check_eq)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GET FILTER CONDITIONS
# └─────────────────────────────────────────────────────────────────────────────────────


def get_filter_conditions(key_values: dict[str, Any]) -> Generator[Any, None, None]:
    """Yields a series of filter conditions based on a dictionary of key-value pairs"""

    # Iterate over key-value pairs
    for key, value in key_values.items():
        # Yields filter condition
        yield get_filter_condition(key, value)
