# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, Generic, Hashable, Iterable, Iterator, TypeVar

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collection.exceptions import (
    DuplicateKeyError,
    MultipleItemsError,
    NoItemsError,
    NonExistentKeyError,
)
from core.object.functions.oget import oget


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

    def __init__(self, keys: Iterable[str] | None = None) -> None:
        """Init Method"""

        # Set keys
        self._keys = tuple(keys or ())

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
    # │ FILTER
    # └─────────────────────────────────────────────────────────────────────────────────

    def filter(self, **kwargs: Any) -> Collection[AnyBound]:
        """Filters the collection by keyword args"""

        # Initialize collection
        collection: Collection[AnyBound] = Collection(keys=self._keys)

        # Get key values
        key_values = kwargs.items()

        # Iterate over items
        for item in self:
            # Iterate over keyword arguments
            for key, value in key_values:
                # Initialize try-except block
                try:
                    # Get value
                    value_actual = oget(item, key, delimiter="__")

                # Break on KeyError
                except KeyError:
                    break

                # Break if value is not equal to actual value
                if value != value_actual:
                    break

            # Otherwise, add item to collection
            else:
                # Add item to collection
                collection.add(item)

        # Return collection
        return collection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FILTER ONLY
    # └─────────────────────────────────────────────────────────────────────────────────

    def filter_only(self, **kwargs: Any) -> AnyBound:
        """Filters the collection by keyword args and returns the only item"""

        # Return item
        return self.filter(**kwargs).only()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FILTER ONLY OR NONE
    # └─────────────────────────────────────────────────────────────────────────────────

    def filter_only_or_none(self, **kwargs: Any) -> AnyBound | None:
        """Filters the collection by keyword args and returns the only item or None"""

        # Return item
        return self.filter(**kwargs).only_or_none()

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
    # │ ONLY
    # └─────────────────────────────────────────────────────────────────────────────────

    def only(self) -> AnyBound:
        """Returns the only item in the collection"""

        # Get item
        item = self.only_or_none()

        # Raise exception if item is None
        if item is None:
            raise NoItemsError()

        # Return item
        return item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ONLY OR NONE
    # └─────────────────────────────────────────────────────────────────────────────────

    def only_or_none(self) -> AnyBound | None:
        """Returns the only item in the collection or None"""

        # Get item count
        item_count = len(self)

        # Check if collection has more than one item
        if item_count > 1:
            raise MultipleItemsError(item_count)

        # Return item if collection has only one item
        if item_count == 1:
            return next(iter(self))

        # Return None
        return None

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
