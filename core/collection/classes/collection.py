# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, Generic, Iterable, Iterator, TypeVar


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TYPE VARIABLES
# └─────────────────────────────────────────────────────────────────────────────────────

AnyBound = TypeVar("AnyBound", bound=Any)

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class Collection(Generic[AnyBound]):
    """A collection utility class for Python object instances"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of items by ID
    _items_by_id: dict[int, AnyBound]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, items: AnyBound | Iterable[AnyBound] | None = None) -> None:
        """Init Method"""

        # Initialize items by ID
        self._items_by_id = {}

        # Add items
        self.add(items)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[AnyBound]:
        """Iterate Method"""

        return iter(self._items_by_id.values())

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ADD
    # └─────────────────────────────────────────────────────────────────────────────────

    def add(self, items: AnyBound | Iterable[AnyBound] | None) -> int:
        """Adds an item to the collection"""

        # Return 0 if items is None
        if items is None:
            return 0

        # Get items
        items = items if isinstance(items, Iterable) else [items]

        # Initialize count
        count = 0

        # Iterate over items
        for item in items:
            # Get item ID
            item_id = id(item)

            # Continue if item is already in collection
            if item is None or item_id in self._items_by_id:
                continue

            # Add item to collection
            self._items_by_id[item_id] = item

            # Increment count
            count += 1

        # Return count
        return count

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REMOVE
    # └─────────────────────────────────────────────────────────────────────────────────

    def remove(self, items: AnyBound | Iterable[AnyBound] | None) -> int:
        """Removes an item from the collection"""

        # Return 0 if items is None
        if items is None:
            return 0

        # Get items
        items = items if isinstance(items, Iterable) else [items]

        # Initialize count
        count = 0

        # Iterate over items
        for item in items:
            # Get item ID
            item_id = id(item)

            # Continue if item is not in collection
            if item is None or item_id not in self._items_by_id:
                continue

            # Remove item from collection
            del self._items_by_id[item_id]

            # Increment count
            count += 1

        # Return count
        return count
