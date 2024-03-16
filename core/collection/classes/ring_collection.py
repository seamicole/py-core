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
    """A ring collection utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of cursor
    _cursor: int

    # Declare type of length
    _length: int

    # Declare type of size
    _size: int | None

    # Declare type of ring
    _ring: list[ItemBound | None]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, size: int | None) -> None:
        """Init Method"""

        # Initialize cursor
        self._cursor = 0

        # Initialize length
        self._length = 0

        # Initialize max size
        self._size = size

        # Initialize ring
        self._ring = []

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
    # │ _CURSOR NEXT
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def _cursor_next(self) -> int:
        """Returns the current cursor + 1"""

        # Get cursor next
        cursor_next = self._cursor + 1

        # Check if size is not None
        if self._size is not None:
            # Wrap cursor
            cursor_next = cursor_next % self._size

        # Return next cursor
        return cursor_next

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
    # │ NEXT
    # └─────────────────────────────────────────────────────────────────────────────────

    def next(self) -> ItemBound | None:
        """Returns the next item in the collection"""

        # Return next item
        return self.get(self._cursor, default=None)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ADD
    # └─────────────────────────────────────────────────────────────────────────────────

    def add(self, *items: ItemBound) -> int:
        """Adds an item to the collection"""

        # Initialize count
        count = 0

        # Iterate over items
        for item in items:
            # Check if size is None
            if self._size is None or self._length < self._size:
                # Append item to collection
                self._ring.append(item)

            # Otherwise insert by cursor
            else:
                # Add item to buffer
                self._ring[self._cursor] = item

            # Increment cursor
            self._cursor = self._cursor_next

            # Check if no size limit or length is less than size
            if self._size is None or self._length < self._size:
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

        # Wrap if size is defined
        if self._size is not None:
            # Wrap index
            index = index % self._size

        # Check if index exceeds length
        if index > self._length - 1:
            # Return default
            return default

        # Get item
        item = self._ring[index]

        # Return item
        return item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REMOVE
    # └─────────────────────────────────────────────────────────────────────────────────

    def remove(self, *items: Any | ItemBound) -> int:
        """Removes an item from the collection"""

        # Raise NotImplementedError
        raise NotImplementedError("RingCollection does not support remove")

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ UPDATE SIZE
    # └─────────────────────────────────────────────────────────────────────────────────

    def update_size(self, size: int | None) -> None:
        """Updates the size of the collection"""

        # Check if size is lower than current size
        if size is not None and self._size is not None and size < self._size:
            # Get diff
            diff = self._size - size

            # Shrink ring by diff
            self._ring = self._ring[diff:]

            # Update cursor
            self._cursor = max(0, self._cursor - diff)

        # Set size
        self._size = size
