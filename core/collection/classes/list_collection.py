# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, Hashable, Iterator, TypeVar

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collection.classes.collection import Collection

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TYPE VARIABLES
# └─────────────────────────────────────────────────────────────────────────────────────

ItemBound = TypeVar("ItemBound", bound=Any)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ LIST COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class ListCollection(Collection[ItemBound]):
    """A list collection utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of items
    _items: list[ItemBound]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        """Init Method"""

        # Initialize items
        self._items = []

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __GETITEM__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __getitem__(self, item: Any) -> Any:
        """Get Item Method"""

        # Check if item is an integer
        if isinstance(item, int):
            return self.get(item)

        # Check if item is a slice
        return self._items[item]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[ItemBound]:
        """Iter Method"""

        # Iterate over items
        for item in self._items:
            yield item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __LEN__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __len__(self) -> int:
        """Length Method"""

        # Return length
        return len(self._items)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REVERSED__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __reversed__(self) -> Iterator[ItemBound]:
        """Reversed Method"""

        # Return reversed items
        return reversed(self._items)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ADD
    # └─────────────────────────────────────────────────────────────────────────────────

    def add(self, *items: ItemBound) -> int:
        """Adds an item to the collection"""

        # Initialize count
        count = 0

        # Iterate over items
        for item in items:
            # Append item to collection
            self._items.append(item)

            # Increment count
            count += 1

        # Return count
        return count

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ APPEND
    # └─────────────────────────────────────────────────────────────────────────────────

    def append(self, item: ItemBound) -> int:
        """Appends an item to the collection list"""

        # Append item to items
        self._items.append(item)

        # Return number of items appended
        return 1

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIND
    # └─────────────────────────────────────────────────────────────────────────────────

    def find(self, item: Any | ItemBound) -> ItemBound | None:
        """Finds an item in the collection"""

        # Get item ID
        id_item = id(item)

        # Iterate over items
        for current in self:
            # Return item if current is item
            if id(current) == id_item or current == item:
                return current

        # Return get
        return self.get(item)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ GET
    # └─────────────────────────────────────────────────────────────────────────────────

    def get(self, key: Hashable, default: ItemBound | None = None) -> ItemBound | None:
        """Gets an item from the ring collection"""

        # Return default if key not an int
        if not isinstance(key, int):
            return default

        # Get index
        index = key

        # Check if index exceeds length
        if index > len(self) - 1:
            # Return default
            return default

        # Get item
        item = self._items[index]

        # Return item
        return item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ NEW
    # └─────────────────────────────────────────────────────────────────────────────────

    def New(self, *args: Any, **kwargs: Any) -> Collection[ItemBound]:
        """Returns a new collection"""

        # Return new collection
        return ListCollection(*args, **kwargs)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ NEXT
    # └─────────────────────────────────────────────────────────────────────────────────

    def next(self) -> ItemBound | None:
        """Returns the next item in the collection"""

        # Raise NotImplementedError
        raise NotImplementedError

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ POP
    # └─────────────────────────────────────────────────────────────────────────────────

    def pop(self, index: int = -1) -> ItemBound:
        """Pops an item from the collection"""

        # Pop item from collection
        return self._items.pop(index)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REMOVE
    # └─────────────────────────────────────────────────────────────────────────────────

    def remove(self, *items: Any | ItemBound) -> int:
        """Removes an item from the collection"""

        # Get original length
        len0 = len(self)

        # Remove items from collection
        self._items = [i for i in self._items if i not in items]

        # Return number of items removed
        return len0 - len(self)
