# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, Generic, Hashable, Iterable, Iterator, TypeVar

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collection.exceptions import DuplicateKeyError, NonExistentKeyError


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

    # Declare type of keys
    _keys: tuple[str, ...]

    # Declare type of items by ID
    _items_by_id: dict[int, AnyBound]

    # Declare type of item IDs by key
    _item_ids_by_key: dict[Hashable, int]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        items: AnyBound | Iterable[AnyBound] | None = None,
        keys: Iterable[str] | None = None,
    ) -> None:
        """Init Method"""

        # Set keys
        self._keys = tuple(keys or ())

        # Initialize items by ID
        self._items_by_id = {}

        # Initialize item IDs by key
        self._item_ids_by_key = {}

        # Add items
        self.add(items)

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
                # Check if key is not in item
                if key not in item.__dict__:
                    continue

                # Get key value
                key_value = item.__dict__[key]

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
                # Check if key is not in item
                if key not in item.__dict__:
                    continue

                # Get key value
                key_value = item.__dict__[key]

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
