# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, Iterator, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.functions.datetime import utc_now

if TYPE_CHECKING:
    from core.collections.classes.collection import Collection
    from core.collections.classes.item import Item


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ITEMS
# └─────────────────────────────────────────────────────────────────────────────────────


class Items:
    """A utility class that represents a collection of Item instances"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of collection
    _collection: Collection

    # Declare type of operations
    _operations: tuple[Any, ...]

    # Declare type of children
    _children: tuple["Items", ...]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        collection: Collection,
        operations: tuple[Any, ...] = (),
        children: tuple["Items", ...] = (),
    ):
        """Init Method"""

        # Set collection
        self._collection = collection

        # Set operations
        self._operations = operations

        # Set children
        self._children = children

    # ┌────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[Item]:
        """Iter Method"""

        # Yield from collection
        yield from self._collect()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        """Representation Method"""

        # Initialize representation to class name
        representation = self.__class__.__name__

        # Get item count
        count = self.count()

        # Add count to representation
        representation += f": {count}"

        # Define n
        n = 20

        # Get head
        head = self.head(n=n)

        # Get items
        items = [item.__repr__() for item in head._collect(quick=True)]

        # Check if there are more than n items total
        if count > n:
            # Add truncation message to items list
            items.append("...(remaining items truncated)... ")

        # Add items to representation
        representation = f"{representation} {'[' + ', '.join(items) + ']'}"

        # Add angle brackets to the representation
        representation = f"<{representation}>"

        # Return representation
        return representation

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _COLLECT
    # └─────────────────────────────────────────────────────────────────────────────────

    def _collect(self, quick: bool = False) -> Iterator[Item]:
        """Returns an iterator of items"""

        # Get pulled at
        pulled_at = utc_now()

        # Iterate over items
        for items in (self,) + self._children:
            # Iterate over collectio
            for item in items._collection.collect(items=items, quick=quick):
                # Set pulled at
                item._imeta.pulled_at = pulled_at

                # Yield item
                yield item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _COPY
    # └─────────────────────────────────────────────────────────────────────────────────

    def _copy(self) -> Items:
        """Returns a copy of the current collection"""

        # Initialize and return a copy of the current collection
        return Items(
            collection=self._collection,
            operations=self._operations,
            children=self._children,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    def count(self) -> int:
        """Returns a count of items in the collection"""

        # Return the number of items in the collection
        return self._collection.count(items=self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FILTER
    # └─────────────────────────────────────────────────────────────────────────────────

    def filter(self, **kwargs: Any) -> Items:
        """Returns a filtered collection of items"""

        # Define operators
        operators = {
            "contains": "contains",
            "icontains": "icontains",
            "eq": "equals",
            "ieq": "iequals",
            "equals": "equals",
            "iequals": "iequals",
            "exact": "equals",
            "iexact": "iequals",
            "gt": "gt",
            "gte": "gte",
            "in": "in",
            "iin": "iin",
            "lt": "lt",
            "lte": "lte",
        }

        # Initialize conditions
        conditions = []

        # Iterate over kwargs
        for key, value in kwargs.items():
            # Split key
            key_split = key.split("__")

            # Get operator
            operator = key_split[-1]

            # Check if operator is in operators
            if operator in operators:
                # Remove operator suffix from key
                key = key.removesuffix(f"__{operator}")

                # Append condition to conditions and break
                conditions.append((key, operators[operator], value))

            # Otherwise set default operator
            else:
                # Append condition to conditions
                conditions.append((key, "equals", value))

        # Initialize and return a filtered collection of items
        return self._collection.filter(tuple(conditions), items=self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PUSH
    # └─────────────────────────────────────────────────────────────────────────────────

    def push(self, item: Item) -> None:
        """Pushes an item to the collection"""

        # Push item to collection
        self._collection.push(item=item)

        # Update pushed at timestamp
        item._imeta.pushed_at = utc_now()
