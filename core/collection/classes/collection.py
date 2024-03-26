# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import random

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Callable, Generator, Generic, Hashable, Iterator, TypeVar

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collection.exceptions import MultipleItemsError, NoItemsError
from core.collection.functions.filter_conditions import get_filter_conditions
from core.dict.types import DictSchema
from core.object.functions.oget import oget
from core.object.functions.oupdate import oupdate

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TYPE VARIABLES
# └─────────────────────────────────────────────────────────────────────────────────────

ItemBound = TypeVar("ItemBound", bound=Any)

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class Collection(Generic[ItemBound], ABC):
    """A collection utility class for Python object instances"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TYPE VARIABLES
    # └─────────────────────────────────────────────────────────────────────────────────

    CollectionBound = TypeVar("CollectionBound", bound="Collection[ItemBound]")

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __GETITEM__
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def __getitem__(self, key_value: Hashable) -> ItemBound:
        """Get Item Method"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def __iter__(self) -> Iterator[ItemBound]:
        """Iterate Method"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __LEN__
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def __len__(self) -> int:
        """Length Method"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REVERSED__
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def __reversed__(self) -> Iterator[ItemBound]:
        """Reversed Method"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ NEW
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def New(self: CollectionBound, *args: Any, **kwargs: Any) -> CollectionBound:
        """Returns a new collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ADD
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def add(self, *items: ItemBound) -> int:
        """Adds an item to the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIND
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def find(self, item: ItemBound) -> ItemBound | None:
        """Finds an item in the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ GET
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def get(self, key: Hashable, default: ItemBound | None = None) -> ItemBound | None:
        """Gets an item from the collection by key"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ NEXT
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def next(self) -> ItemBound | None:
        """Returns the next item in the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REMOVE
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def remove(self, *items: Any | ItemBound) -> int:
        """Removes an item from the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __AND__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __and__(self: CollectionBound, other: Any) -> CollectionBound:
        """And Method"""

        # Check if other is not a Collection instance
        if not isinstance(other, Collection):
            # Raise TypeError
            raise TypeError(
                "Unsupported operand type(s) for &: 'Collection' and '{}'".format(
                    type(other).__name__
                )
            )

        # Initialize collection
        collection = self.New()

        # Iterate over collection
        for item in self:
            # Continue if item is in other collection
            if item in other:
                # Add item to collection
                collection.add(item)

        # Return collection
        return collection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __CONTAINS__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __contains__(self, item: Any) -> bool:
        """Contains Method"""

        # Return whether item is in collection
        return self.find(item) is not None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __OR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __or__(self: CollectionBound, other: Any) -> CollectionBound:
        """Or Method"""

        # Check if other is not a Collection instance
        if not isinstance(other, Collection):
            # Raise TypeError
            raise TypeError(
                "Unsupported operand type(s) for |: 'Collection' and '{}'".format(
                    type(other).__name__
                )
            )

        # Make a shallow copy of the collection
        collection = self.copy_shallow()

        # Iterate over other collection
        for item in other:
            # Continue if item already in collection
            if item in collection:
                continue

            # Add to collection
            collection.add(item)

        # Return collection
        return collection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        """Representation Method"""

        # Return __reprstr__ with repr
        return self.__reprstr__(repr)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPRSTR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __reprstr__(self, func: Callable[[ItemBound], str]) -> str:
        """A utility function to be used with __repr__ and __str__"""

        # Get item count
        item_count = len(self)

        # Initialize representation
        representation = f"{self.__class__.__name__}: {item_count} ["

        # Iterate over items
        for i, item in enumerate(self):
            # Add item representation to representation
            representation += func(item)

            # Check if should truncate
            if i > 19:
                representation += " ...(remaining elements truncated)... "
                break

            # Check if should add a comma
            if i < item_count - 1:
                representation += ", "

        # Close square brackets
        representation += "]"

        # Add angle brackets to the representation
        representation = f"<{representation}>"

        # Return representation
        return representation

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __STR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __str__(self) -> str:
        """String Method"""

        # Return __reprstr__ with str
        return self.__reprstr__(str)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __SUB__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __sub__(self: CollectionBound, other: Any) -> CollectionBound:
        """Subtract Method"""

        # Check if other is not a Collection instance
        if not isinstance(other, Collection):
            # Raise TypeError
            raise TypeError(
                "Unsupported operand type(s) for -: 'Collection' and '{}'".format(
                    type(other).__name__
                )
            )

        # Make a shallow copy of the collection
        collection = self.copy_shallow(exclude=other)  # type: ignore

        # Return collection
        return collection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __TRUEDIV__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __truediv__(
        self: CollectionBound, other: int
    ) -> Generator[CollectionBound, None, None]:
        """True Division Method"""

        # Check if invalid
        if other <= 0:
            return

        # Get item count
        item_count = len(self)

        # Calculate the number of items in most collections (minimum size)
        min_items_per_collection = item_count // other

        # Calculate how many collections need one extra item
        extra_item_collections = item_count % other

        # Initialize variables
        collection = None
        current_count = 0

        # Iterate over the collection
        for item in self:
            # Check current count
            if current_count == 0:
                if collection is not None:
                    yield collection
                collection = self.New()

            # Add to collection
            if collection is not None:
                collection.add(item)
                current_count += 1

            # Determine if we should start a new collection
            limit = min_items_per_collection + (1 if extra_item_collections > 0 else 0)
            if current_count == limit:
                current_count = 0
                if extra_item_collections > 0:
                    extra_item_collections -= 1

        # Yield the last collection if it exists and has items
        if collection is not None and len(collection) > 0:
            yield collection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COPY DEEP
    # └─────────────────────────────────────────────────────────────────────────────────

    def copy_deep(
        self: CollectionBound, exclude: CollectionBound | None = None
    ) -> CollectionBound:
        """Returns a deep copy of the collection"""

        # Initialize collection
        collection = self.New()

        # Iterate over the collection
        for item in self:
            # Add item to collection
            if exclude is None or item not in exclude:
                collection.add(deepcopy(item))

        # Return collection
        return collection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COPY SHALLOW
    # └─────────────────────────────────────────────────────────────────────────────────

    def copy_shallow(
        self: CollectionBound, exclude: CollectionBound | None = None
    ) -> CollectionBound:
        """Returns a shallow copy of the collection"""

        # Initialize collection
        collection = self.New()

        # Iterate over the collection
        for item in self:
            # Add item to collection
            if exclude is None or item not in exclude:
                # Add item to collection
                collection.add(item)

        # Return collection
        return collection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    def count(self) -> int:
        """Returns the number of items in the collection"""

        # Return length
        return len(self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FILTER
    # └─────────────────────────────────────────────────────────────────────────────────

    def filter(self: CollectionBound, **kwargs: Any) -> CollectionBound:
        """Filters the collection by keyword args"""

        # Initialize collection
        collection = self.New()

        # Initialize conditions
        conditions = list(get_filter_conditions(kwargs))

        # Iterate over items
        for item in self:
            # Iterate over keyword arguments
            for key, value, operator, checker in conditions:
                # Initialize try-except block
                try:
                    # Get value
                    value_actual = oget(item, key, delimiter="__")

                # Break on KeyError
                except KeyError:
                    break

                # Break if condition not met
                if checker(value_actual, value) is False:
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

    def filter_only(self, **kwargs: Any) -> ItemBound:
        """Filters the collection by keyword args and returns the only item"""

        # Return item
        return self.filter(**kwargs).only()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FILTER ONLY OR NONE
    # └─────────────────────────────────────────────────────────────────────────────────

    def filter_only_or_none(self, **kwargs: Any) -> ItemBound | None:
        """Filters the collection by keyword args and returns the only item or None"""

        # Return item
        return self.filter(**kwargs).only_or_none()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIND AND UPDATE
    # └─────────────────────────────────────────────────────────────────────────────────

    def find_and_update(self, item: ItemBound, schema: DictSchema | None = None) -> int:
        """Finds an item in the collection and updates it"""

        # Get item
        item_found = self.find(item)

        # Check if item was found
        if item_found is None:
            return 0

        # Check if item is the same
        if id(item_found) == id(item):
            return 1

        # Update item
        oupdate(item_found, item, schema=schema)

        # Return 1
        return 1

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIND AND UPDATE OR ADD
    # └─────────────────────────────────────────────────────────────────────────────────

    def find_and_update_or_add(
        self, item: ItemBound, schema: DictSchema | None = None
    ) -> int:
        """Finds an item in the collection and updates it or adds it"""

        # Find and update
        result = self.find_and_update(item, schema=schema)

        # Check if no item was updated
        if result == 0:
            # Add item
            result = self.add(item)

        # Return result
        return result

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIND OR ADD
    # └─────────────────────────────────────────────────────────────────────────────────

    def find_or_add(self, item: ItemBound) -> int:
        """Finds an item in the collection or adds it"""

        # Find item
        result = self.find(item)

        # Check if item was found
        if result is not None:
            return 0

        # Add item
        return self.add(item)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIRST
    # └─────────────────────────────────────────────────────────────────────────────────

    def first(self) -> ItemBound | None:
        """Returns the first item in the collection"""

        # Check if collection is empty
        if self.count() == 0:
            return None

        # Return first item
        return next(iter(self))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ HEAD
    # └─────────────────────────────────────────────────────────────────────────────────

    def head(self: CollectionBound, n: int = 5) -> CollectionBound:
        """Returns a new collection of the first n items of the collection"""

        # Initialize collection
        collection = self.New()

        # Get n
        n = max(0, min(n, len(self)))

        # Get reverse iterator
        iterator = reversed(self)

        # Iterate over items
        for i in range(n):
            # Add item to collection
            collection.add(next(iterator))

        # Return collection
        return collection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LAST
    # └─────────────────────────────────────────────────────────────────────────────────

    def last(self) -> ItemBound | None:
        """Returns the last item in the collection"""

        # Check if collection is empty
        if self.count() == 0:
            return None

        # Return last item
        return next(reversed(self))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ONLY
    # └─────────────────────────────────────────────────────────────────────────────────

    def only(self) -> ItemBound:
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

    def only_or_none(self) -> ItemBound | None:
        """Returns the only item in the collection or None"""

        # Get item count
        item_count = self.count()

        # Check if collection has more than one item
        if item_count > 1:
            raise MultipleItemsError(item_count)

        # Return item if collection has only one item
        if item_count == 1:
            return self.first()

        # Return None
        return None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SAMPLE
    # └─────────────────────────────────────────────────────────────────────────────────

    def sample(self: CollectionBound, n: int) -> CollectionBound:
        """Returns a random sample of n items in the collection"""

        # Convert collection to list
        items = list(self)

        # Get sample
        items = random.sample(items, n)

        # Initialize sample
        sample = self.New()

        # Add items to sample
        sample.add(*items)

        # Return sample
        return sample

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TAIL
    # └─────────────────────────────────────────────────────────────────────────────────

    def tail(self: CollectionBound, n: int = 5) -> CollectionBound:
        """Returns a new collection of the last n items of the collection"""

        # Initialize collection
        collection = self.New()

        # Get n
        n = max(0, min(n, len(self)))

        # Get reverse iterator
        iterator = reversed(self)

        # Create new iterator
        for item in reversed([next(iterator) for i in range(n)]):
            # Add item to collection
            collection.add(item)

        # Return collection
        return collection
