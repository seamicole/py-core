# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, Hashable, Iterable, Iterator, TypeVar

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collection.classes.collection import Collection
from core.collection.exceptions import DuplicateKeyError, NonExistentKeyError
from core.placeholders import nothing

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TYPE VARIABLES
# └─────────────────────────────────────────────────────────────────────────────────────

AnyBound = TypeVar("AnyBound", bound=Any)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DICT COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class DictCollection(Collection[AnyBound]):
    """A dict-based collection utility class for Python object instances"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of keys
    _keys: tuple[str | tuple[str, ...], ...]

    # Declare type of items by ID
    _items_by_id: dict[int, AnyBound]

    # Declare type of item IDs by key
    _item_ids_by_key: dict[Hashable, int]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CREATE KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    @classmethod
    def create_key(
        cls, item: AnyBound, key: str | tuple[str, ...]
    ) -> Any | tuple[Any, ...]:
        """Creates a key or tuple of keys"""

        # Return item if key is a tuple
        if isinstance(key, tuple):
            # Initialize value
            value = []

            # Iterate over keys
            for k in key:
                # Check if key is not in item
                if not hasattr(item, k):
                    # Return nothing
                    return nothing

                # Append value
                value.append(getattr(item, k))

            # Return value
            return tuple(value)

        # Check if key is not in item
        if not hasattr(item, key):
            # Return nothing
            return nothing

        # Return key
        return getattr(item, key)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, keys: Iterable[str | Iterable[str]] | None = None) -> None:
        """Init Method"""

        # Set keys
        self._keys = tuple(
            tuple(k) if isinstance(k, Iterable) and not isinstance(k, str) else k
            for k in keys or []
        )

        # Initialize items by ID
        self._items_by_id = {}

        # Initialize item IDs by key
        self._item_ids_by_key = {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __GETITEM__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __getitem__(self, key_value: Hashable) -> AnyBound:
        """Get Item Method"""

        # Raise NonExistentKeyError if key value is not in collection
        if key_value not in self._item_ids_by_key:
            raise NonExistentKeyError(key_value)

        # Get and return item
        return self._items_by_id[self._item_ids_by_key[key_value]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[AnyBound]:
        """Iterate Method"""

        # Return iterator
        return iter(self._items_by_id.values())

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __LEN__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __len__(self) -> int:
        """Length Method"""

        # Return length
        return len(self._items_by_id)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REVERSED__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __reversed__(self) -> Iterator[AnyBound]:
        """Reversed Method"""

        # Iterate over reversed keys
        for key in reversed(self._items_by_id):
            # Yield item
            yield self._items_by_id[key]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ NEW
    # └─────────────────────────────────────────────────────────────────────────────────

    def New(self) -> DictCollection[AnyBound]:
        """Returns a new collection"""

        # Return new collection
        return DictCollection(keys=self._keys)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ADD
    # └─────────────────────────────────────────────────────────────────────────────────

    def add(self, *items: AnyBound) -> int:
        """Adds an item to the collection"""

        # Initialize count
        count = 0

        # Iterate over items
        for item in items:
            # Continue if item is None
            if item is None:
                continue

            # Get item ID
            item_id = id(item)

            # Continue if item is already in collection
            if item_id in self._items_by_id:
                continue

            # Initialize item IDs by key
            item_ids_by_key = {}

            # Iterate over keys
            for key in self._keys:
                # Get key value
                key_value = self.create_key(item, key)

                # Continue if key value is nothing
                if key_value is nothing:
                    continue

                # Raise DuplicateKeyError if key value is already in collection
                if key_value in self._item_ids_by_key:
                    raise DuplicateKeyError(key_value)

                # Add key value to item IDs by key
                item_ids_by_key[key_value] = item_id

            # Update item IDs by key
            self._item_ids_by_key.update(item_ids_by_key)

            # Add item to collection
            self._items_by_id[item_id] = item

            # Increment count
            count += 1

        # Return count
        return count

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIND
    # └─────────────────────────────────────────────────────────────────────────────────

    def find(self, item: AnyBound) -> AnyBound | None:
        """Finds an item in the collection"""

        # Return if item is in items by ID
        if id(item) in self._items_by_id:
            return item

        # Return if item is in item IDs by key
        if isinstance(item, Hashable) and item in self._item_ids_by_key:
            return self._items_by_id[self._item_ids_by_key[item]]

        # Check if item has a __dict__ attribute
        if hasattr(item, "__dict__"):
            # Iterate over keys
            for key in self._keys:
                # Get value
                value = self.create_key(item, key)

                # Continue if value is nothing
                if value is nothing:
                    continue

                # Check if value is in item IDs by key
                if value in self._item_ids_by_key:
                    # Return item
                    return self._items_by_id[self._item_ids_by_key[value]]

        # Return None
        return None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ GET
    # └─────────────────────────────────────────────────────────────────────────────────

    def get(self, key: Hashable, default: AnyBound | None = None) -> AnyBound | None:
        """Gets an item from the collection by key"""

        # Return item if key is in collection
        if key in self._item_ids_by_key:
            return self._items_by_id[self._item_ids_by_key[key]]

        # Return default
        return default

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REMOVE
    # └─────────────────────────────────────────────────────────────────────────────────

    def remove(self, *items: AnyBound) -> int:
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
            # Continue if item is None
            if item is None:
                continue

            # Get item ID
            item_id = id(item)

            # Continue if item is not in collection
            if item_id not in self._items_by_id:
                continue

            # Iterate over keys
            for key in self._keys:
                # Get key value
                key_value = self.create_key(item, key)

                # Continue if key value is nothing
                if key_value is nothing:
                    continue

                # Check if key value is not in item IDs by key
                if key_value not in self._item_ids_by_key:
                    continue

                # Remove key value from item IDs by key
                del self._item_ids_by_key[key_value]

            # Remove item from collection
            del self._items_by_id[item_id]

            # Increment count
            count += 1

        # Return count
        return count
