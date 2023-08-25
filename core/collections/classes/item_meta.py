# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collections.classes.collection import Collection

if TYPE_CHECKING:
    from core.collections.classes.items import Items


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CLASS META
# └─────────────────────────────────────────────────────────────────────────────────────


class ClassMeta:
    """A meta class for an Item class definition"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize items
    ITEMS: Collection | Items | None = None

    # Initialize keys
    KEYS: tuple[str | tuple[str, ...], ...] = ()

    # Initialize indexes
    INDEXES: tuple[str | tuple[str, ...], ...] = ()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of _items
    _items: Items | None = None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        """Init Method"""

        # Initialize items
        self._items = (
            self.ITEMS.all() if isinstance(self.ITEMS, Collection) else self.ITEMS
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ITEMS
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def items(self) -> Items:
        """Returns the items of the meta instance"""

        # Get items
        items = self._items

        # Check if items is None
        if items is None:
            # Raise AttributeError
            raise AttributeError(f"{self.__class__.__name__}.Meta.ITEMS is undefined.")

        # Return items
        return items


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ INSTANCE META
# └─────────────────────────────────────────────────────────────────────────────────────


class InstanceMeta:
    """A meta class for an Item instance"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of ID
    id: str | None

    # Declare type of pushed at
    pushed_at: datetime | None

    # Declare type of pulled at
    pulled_at: datetime | None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        """Init Method"""

        # Initialize ID
        self.id = None

        # Initialize pushed at
        self.pushed_at = None

        # Initialize pulled at
        self.pulled_at = None
