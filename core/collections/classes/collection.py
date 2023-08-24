# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generator, Iterable, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collections.classes.items import Items

if TYPE_CHECKING:
    from core.collections.classes.item import Item


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class Collection(ABC):
    """An abstract class that represents a collection of items"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ALL
    # └─────────────────────────────────────────────────────────────────────────────────

    def all(self) -> Items:
        """Returns all items in the collection"""

        # Return all items
        return Items(collection=self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ APPLY
    # └─────────────────────────────────────────────────────────────────────────────────

    def apply(self, items: Items | None, *operations: Any) -> Items:
        """Applies a series of operations to a collection of items"""

        # Initialize items
        items = items._copy() if items is not None else self.all()

        # Append head operation to operations
        items._operations += operations

        # Return items
        return items

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COLLECT
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def collect(
        self,
        items: Items | None = None,
        subset: Iterable[Item] | None = None,
        quick: bool = False,
    ) -> Generator[Item, None, None]:
        """Yields items in the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def count(self, items: Items | None = None) -> int:
        """Returns a count of items in the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FILTER
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def filter(
        self,
        conditions: tuple[tuple[str, str, Any], ...],
        items: Items | None = None,
    ) -> Items:
        """Filters items in the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIRST
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def first(self, items: Items | None = None) -> Item | None:
        """Returns the first item in the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ HEAD
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def head(self, n: int, items: Items | None = None) -> Items:
        """Returns the first n items in the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def key(self, key: Any, items: Items | None = None) -> Item:
        """Returns an item by key lookup"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LAST
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def last(self, items: Items | None = None) -> Item | None:
        """Returns the last item in the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PUSH
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def push(self, item: Item) -> None:
        """Pushes an item to the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SLICE
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def slice(self, start: int, stop: int, items: Items | None = None) -> Items:
        """Returns a slice of items in the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TAIL
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def tail(self, n: int, items: Items | None = None) -> Items:
        """Returns the last n items in the collection"""
