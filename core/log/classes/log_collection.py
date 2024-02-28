# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collection.classes.ring_collection import RingCollection

if TYPE_CHECKING:
    from core.log.classes.log import Log  # noqa: F401


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ LOG COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class LogCollection(RingCollection["Log"]):
    """A ring collection utility class for Log instances"""
