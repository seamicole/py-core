# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from datetime import datetime
from typing import Any, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collections.classes.collection import Collection
from core.collections.dict_collection import DictCollection

if TYPE_CHECKING:
    from core.collections.classes.item_metaclass import ItemMetaclass
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
    ITEMS: Collection[Any] | Items[Any] | None = None

    # Initialize keys
    KEYS: tuple[str | tuple[str, ...], ...] = ()

    # Initialize indexes
    INDEXES: tuple[str | tuple[str, ...], ...] = ()

    # Initialize parents and children
    PARENTS: tuple[ItemMetaclass, ...] = ()
    CHILDREN: tuple[ItemMetaclass, ...] = ()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of items
    items: Items[Any]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        """Init Method"""

        # Get items
        items = self.ITEMS

        # Check if items is None
        if items is None:
            # Initialize collection
            items = DictCollection()

        # Check if items is a collection
        if isinstance(items, Collection):
            # Get items
            items = items.all()

        # Set items
        self.items = items

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLEAN KEYS
    # └─────────────────────────────────────────────────────────────────────────────────

    def clean_keys(self, keys: tuple[Any, ...]) -> tuple[Any, ...]:
        """Cleans a series of key lookups"""

        # Return keys
        return keys


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
