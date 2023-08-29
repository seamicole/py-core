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
    # │ PUSH
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def push(self, item: Item) -> None:
        """Pushes an item to the collection"""
