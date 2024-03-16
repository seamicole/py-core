# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Callable, Generic, Hashable, Iterator, TypeVar

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
    def New(self, *args: Any, **kwargs: Any) -> Collection[ItemBound]:
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

    def __and__(self, other: ItemBound) -> Collection[ItemBound]:
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

    def __or__(self, other: ItemBound) -> Collection[ItemBound]:
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
        collection: Collection[ItemBound] = self.copy_shallow()

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
    # │ COPY DEEP
    # └─────────────────────────────────────────────────────────────────────────────────

    def copy_deep(self) -> Collection[ItemBound]:
        """Returns a deep copy of the collection"""

        # Initialize collection
        collection: Collection[ItemBound] = self.New()

        # Iterate over the collection
        for item in self:
            # Add item to collection
            collection.add(deepcopy(item))

        # Return collection
        return collection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COPY SHALLOW
    # └─────────────────────────────────────────────────────────────────────────────────

    def copy_shallow(self) -> Collection[ItemBound]:
        """Returns a shallow copy of the collection"""

        # Initialize collection
        collection: Collection[ItemBound] = self.New()

        # Iterate over the collection
        for item in self:
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

    def filter(self, **kwargs: Any) -> Collection[ItemBound]:
        """Filters the collection by keyword args"""

        # Initialize collection
        collection: Collection[ItemBound] = self.New()

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

    def head(self, n: int = 5) -> Collection[ItemBound]:
        """Returns a new collection of the first n items of the collection"""

        # Initialize collection
        collection: Collection[ItemBound] = self.New()

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
    # │ TAIL
    # └─────────────────────────────────────────────────────────────────────────────────

    def tail(self, n: int = 5) -> Collection[ItemBound]:
        """Returns a new collection of the last n items of the collection"""

        # Initialize collection
        collection: Collection[ItemBound] = self.New()

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
