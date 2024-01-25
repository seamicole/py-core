# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.object.functions.lowercase import lowercase


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CHECK EQ
# └─────────────────────────────────────────────────────────────────────────────────────


def check_eq(actual: Any, expected: Any) -> bool:
    """Checks weather an actual value is equal to an expected value"""

    # Initialize try-except block
    try:
        return True if actual == expected else False

    # Handle TypeError
    except TypeError:
        return False


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CHECK GT
# └─────────────────────────────────────────────────────────────────────────────────────


def check_gt(actual: Any, expected: Any) -> bool:
    """Checks weather an actual value is greater than an expected value"""

    # Initialize try-except block
    try:
        return True if actual > expected else False

    # Handle TypeError
    except TypeError:
        return False


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CHECK GTE
# └─────────────────────────────────────────────────────────────────────────────────────


def check_gte(actual: Any, expected: Any) -> bool:
    """Checks weather an actual value is greater or equal to an expected value"""

    # Initialize try-except block
    try:
        return True if actual >= expected else False

    # Handle TypeError
    except TypeError:
        return False


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CHECK LT
# └─────────────────────────────────────────────────────────────────────────────────────


def check_lt(actual: Any, expected: Any) -> bool:
    """Checks weather an actual value is less than an expected value"""

    # Initialize try-except block
    try:
        return True if actual < expected else False

    # Handle TypeError
    except TypeError:
        return False


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CHECK LTE
# └─────────────────────────────────────────────────────────────────────────────────────


def check_lte(actual: Any, expected: Any) -> bool:
    """Checks weather an actual value is less than or equal to an expected value"""

    # Initialize try-except block
    try:
        return True if actual <= expected else False

    # Handle TypeError
    except TypeError:
        return False


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CHECK IN
# └─────────────────────────────────────────────────────────────────────────────────────


def check_in(actual: Any, expected: Any) -> bool:
    """Checks weather an actual value is in an expected value"""

    # Initialize try-except block
    try:
        return True if actual in expected else False

    # Handle TypeError
    except TypeError:
        return False


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CHECK IIN
# └─────────────────────────────────────────────────────────────────────────────────────


def check_iin(actual: Any, expected: Any) -> bool:
    """Checks weather an actual value is in an expected value"""

    # Lowercase expected and actual
    expected, actual = (lowercase(expected), lowercase(actual))

    # Initialize try-except block
    try:
        return True if actual in expected else False

    # Handle TypeError
    except TypeError:
        return False
