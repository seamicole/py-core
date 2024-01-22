# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, Hashable, Iterator, TypeVar

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collection.exceptions import MultipleItemsError, NoItemsError
from core.object.functions.oget import oget


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
    # │ NEW
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def New(self) -> Collection[AnyBound]:
        """Returns a new collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ADD
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def add(self, *items: AnyBound) -> int:
        """Adds an item to the collection"""

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
