# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import itertools

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
# │ RING COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class RingCollection(Collection[ItemBound]):
    """A ring buffer for caching deltas"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of cursor
    _cursor: int

    # Declare type of length
    _length: int

    # Declare type of size
    _size: int

    # Declare type of ring
    _ring: list[ItemBound | None]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, size: int) -> None:
        """Init Method"""

        # Initialize cursor
        self._cursor = 0

        # Initialize length
        self._length = 0

        # Initialize max size
        self._size = size

        # Initialize ring
        self._ring = [None] * size

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __GETITEM__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __getitem__(self, item: Any) -> Any:
        """Get Item Method"""

        # Check if item is an integer
        if isinstance(item, int):
            return self.get(item)

        # Check if item is a slice
        return (
            self._ring[self._cursor :] + self._ring[: self._cursor]  # noqa: E203
        ).__getitem__(item)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[ItemBound]:
        """Iter Method"""

        # Iterate over data
        for i in itertools.chain(
            range(self._cursor, self._length), range(self._cursor)
        ):
            # Get item
            item = self._ring[i]

            # Continue if item is None
            if item is None:
                continue

            # Yield data
            yield item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __LEN__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __len__(self) -> int:
        """Length Method"""

        # Return length
        return self._length

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REVERSED__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __reversed__(self) -> Iterator[ItemBound]:
        """Reversed Method"""

        # Calculate the starting points for the reversed iteration
        start1 = (self._cursor - 1) if self._cursor > 0 else (self._length - 1)
        end1 = -1  # The end index is exclusive in range(), so use -1 to include 0
        start2 = self._length - 1
        end2 = self._cursor - 1

        # Iterate over data in reverse
        for i in itertools.chain(range(start1, end1, -1), range(start2, end2, -1)):
            # Get item
            item = self._ring[i]

            # Continue if item is None
            if item is None:
                continue

            # Yield data
            yield item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ NEW
    # └─────────────────────────────────────────────────────────────────────────────────

    def New(self, *args: Any, **kwargs: Any) -> Collection[ItemBound]:
        """Returns a new collection"""

        # Check if size not in kwargs
        if "size" not in kwargs:
            # Add size to kwargs
            kwargs["size"] = self._size

        # Return new collection
        return RingCollection(*args, **kwargs)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ADD
    # └─────────────────────────────────────────────────────────────────────────────────

    def add(self, *items: ItemBound) -> int:
        """Adds an item to the collection"""

        # Initialize count
        count = 0

        # Iterate over items
        for item in items:
            # Add item to buffer
            self._ring[self._cursor] = item

            # Increment cursor
            self._cursor = (self._cursor + 1) % self._size

            # Check if length is less than size
            if self._length < self._size:
                # Increment length
                self._length += 1

            # Increment count
            count += 1

        # Return count
        return count

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIND
    # └─────────────────────────────────────────────────────────────────────────────────

    def find(self, item: Any | ItemBound) -> ItemBound | None:
        """Finds an item in the collection"""

        # Get item ID
        id_item = id(item)

        # Iterate over items
        for i in range(self._length):
            # Get index
            index = (self._cursor + i) % self._size

            # Get item
            current = self._ring[index]

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

        # Get item from buffer
        item = self._ring[(self._cursor + key) % self._size]

        # Raise IndexError if item is None
        if item is None:
            raise IndexError("list index out of range")

        # Return item
        return item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REMOVE
    # └─────────────────────────────────────────────────────────────────────────────────

    def remove(self, *items: ItemBound) -> int:
        """Removes an item from the collection"""

        # Raise NotImplementedError
        raise NotImplementedError("RingCollection does not support remove")
