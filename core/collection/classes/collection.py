# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Generic, Hashable, Iterator, TypeVar

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

AnyBound = TypeVar("AnyBound", bound=Any)

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class Collection(Generic[AnyBound], ABC):
    """A collection utility class for Python object instances"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __GETITEM__
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def __getitem__(self, key_value: Hashable) -> AnyBound:
        """Get Item Method"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def __iter__(self) -> Iterator[AnyBound]:
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
    def __reversed__(self) -> Iterator[AnyBound]:
        """Reversed Method"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ NEW
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def New(self, *args: Any, **kwargs: Any) -> Collection[AnyBound]:
        """Returns a new collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ADD
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def add(self, *items: AnyBound) -> int:
        """Adds an item to the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIND
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def find(self, item: AnyBound) -> AnyBound | None:
        """Finds an item in the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ GET
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def get(self, key: Hashable, default: AnyBound | None = None) -> AnyBound | None:
        """Gets an item from the collection by key"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REMOVE
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def remove(self, *items: AnyBound) -> int:
        """Removes an item from the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __CONTAINS__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __contains__(self, item: AnyBound) -> bool:
        """Contains Method"""

        # Return whether item is in collection
        return self.find(item) is not None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __OR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __or__(self, other: AnyBound) -> Collection[AnyBound]:
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
        collection: Collection[AnyBound] = self.copy_shallow()

        # Iterate over other collection
        for item in other:
            # Add to collection
            collection.add(item)

        # Return collection
        return collection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        """Representation Method"""

        # Get item count
        item_count = len(self)

        # Initialize representation
        representation = f"{self.__class__.__name__}: {item_count} ["

        # Iterate over items
        for i, item in enumerate(self):
            # Add item representation to representation
            representation += repr(item)

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
    # │ COPY DEEP
    # └─────────────────────────────────────────────────────────────────────────────────

    def copy_deep(self) -> Collection[AnyBound]:
        """Returns a deep copy of the collection"""

        # Initialize collection
        collection: Collection[AnyBound] = self.New()

        # Iterate over the collection
        for item in self:
            # Add item to collection
            collection.add(deepcopy(item))

        # Return collection
        return collection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COPY SHALLOW
    # └─────────────────────────────────────────────────────────────────────────────────

    def copy_shallow(self) -> Collection[AnyBound]:
        """Returns a shallow copy of the collection"""

        # Initialize collection
        collection: Collection[AnyBound] = self.New()

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

    def filter(self, **kwargs: Any) -> Collection[AnyBound]:
        """Filters the collection by keyword args"""

        # Initialize collection
        collection: Collection[AnyBound] = self.New()

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
    # │ FIND AND UPDATE
    # └─────────────────────────────────────────────────────────────────────────────────

    def find_and_update(self, item: AnyBound, schema: DictSchema | None = None) -> int:
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
        self, item: AnyBound, schema: DictSchema | None = None
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

    def find_or_add(self, item: AnyBound) -> int:
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

    def first(self) -> AnyBound | None:
        """Returns the first item in the collection"""

        # Check if collection is empty
        if self.count() == 0:
            return None

        # Return first item
        return next(iter(self))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LAST
    # └─────────────────────────────────────────────────────────────────────────────────

    def last(self) -> AnyBound | None:
        """Returns the last item in the collection"""

        # Check if collection is empty
        if self.count() == 0:
            return None

        # Return last item
        return next(reversed(self))

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
        item_count = self.count()

        # Check if collection has more than one item
        if item_count > 1:
            raise MultipleItemsError(item_count)

        # Return item if collection has only one item
        if item_count == 1:
            return self.first()

        # Return None
        return None
