# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from collections import deque
from copy import deepcopy
from typing import Any, Generator, Iterable, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collections.classes.collection import Collection
from core.collections.classes.item import Item
from core.collections.exceptions import DoesNotExistError, DuplicateKeyError
from core.functions.object import oget

if TYPE_CHECKING:
    from core.collections.classes.items import Items


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DICT COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class DictCollection(Collection):
    """A utility class that represents a dictionary collection of items"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize item ID
    _item_id: int

    # Declare type of items by ID
    _items_by_id: dict[int, Item]

    # Declare type of item IDs by key
    _item_ids_by_key: dict[Any, int]

    # Declare type of keys by item ID
    _keys_by_item_id: dict[int, set[Any]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        """Init Method"""

        # Initialize item ID
        self._item_id = 0

        # Initialize items by ID
        self._items_by_id = {}

        # Initialize item IDs by key
        self._item_ids_by_key = {}

        # Initialize keys by item ID
        self._keys_by_item_id = {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _COMPARE
    # └─────────────────────────────────────────────────────────────────────────────────

    def _compare(self, left: Any, right: Any, operator: str) -> bool | None:
        """Returns a boolean comparison of two values based on an operator"""

        # Initialize try-except block
        try:
            # Handle case of equal to
            if operator == "equals":
                return left == right  # type: ignore

            # Otherwise, handle case of less than
            if operator == "lt":
                return left < right  # type: ignore

            # Otherwise handle case of less than or equal to
            elif operator == "lte":
                return left <= right  # type: ignore

            # Otherwise handle case of greater than
            elif operator == "gt":
                return left > right  # type: ignore

            # Otherwise handle case of greater than or equal to
            elif operator == "gte":
                return left >= right  # type: ignore

        # Handle TypeError
        except TypeError:
            pass

        # Return None by default
        return None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _EXPOSE ITEM
    # └─────────────────────────────────────────────────────────────────────────────────

    def _expose_item(self, item: Item) -> Item:
        """Exposes an item from the collection"""

        # Check if item has an ID
        if item._imeta.id is not None:
            # Get item ID
            item_id = int(item._imeta.id)

            # Check if item ID is in items by ID
            if item_id in self._items_by_id:
                # Return item
                return self._items_by_id[item_id]

        # Return item
        return item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _INTERNALIZE ITEM
    # └─────────────────────────────────────────────────────────────────────────────────

    def _internalize_item(self, item: Item) -> Item:
        """Internalizes an item for the collection"""

        # Iterate over attributes in item
        for attr in dir(item):
            # Continue if attribute is private
            if attr.startswith("__"):
                continue

            # Continue if attribute is a method
            if callable(getattr(item, attr)):
                continue

            # Continue if attribute is a property
            if hasattr(item.__class__, attr) and isinstance(
                getattr(item.__class__, attr), property
            ):
                continue

            # Internalize value
            setattr(item, attr, self._internalize_value(getattr(item, attr)))

        # Return item
        return item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _INTERNALIZE VALUE
    # └─────────────────────────────────────────────────────────────────────────────────

    def _internalize_value(self, value: Any) -> Any:
        """Internalizes a value for the collection"""

        # Check if value is an item
        if isinstance(value, Item) and value._imeta.id is not None:
            # Check if item has the same collection type
            if isinstance(value._cmeta.items._collection, type(self)):
                # Return exposed item
                return value._cmeta.items._collection._expose_item(value)

            # Otherwie handle case of different collection type
            else:
                # Get class ID
                class_id = id(value.__class__)

                # Return internalized value
                return (class_id, value._imeta.id)

        # Return value
        return value

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COLLECT
    # └─────────────────────────────────────────────────────────────────────────────────

    def collect(
        self,
        items: Items | None = None,
        subset: Iterable[Item] | None = None,
        quick: bool = False,
    ) -> Generator[Item, None, None]:
        """Yields items in the collection"""

        # Initialize items
        items = self.apply(items)

        # Get operations
        operations = items._operations

        # Initialize collected items
        collected = subset if subset is not None else iter(self._items_by_id.values())

        # Iterate over operations
        for operation in operations:
            # Check if callable
            if callable(operation):
                # Apply operation to collected
                collected = operation(collected)

        # Iterate over collected items
        for item in collected:
            # Deepcopy and yield item
            yield item if quick else deepcopy(item)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    def count(self, items: Items | None = None) -> int:
        """Returns a count of items in the collection"""

        # Initialize items
        items = self.apply(items)

        # Check if there are no operations
        if not items._operations:
            # Return the number of items in the collection
            return len(self._items_by_id)

        # Return the number of items in the collection
        return sum(1 for _ in items._collect(quick=True))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FILTER
    # └─────────────────────────────────────────────────────────────────────────────────

    def filter(
        self,
        conditions: tuple[tuple[str, str, Any], ...],
        items: Items | None = None,
    ) -> Items:
        """Returns a filtered collection of items"""

        # Initialize items
        items = self.apply(items)

        def operation(
            items: Generator[Item, None, None]
        ) -> Generator[Item, None, None]:
            """Yields items filtered from the collection"""

            # Iterate over items
            for item in items:
                # Iterate over kwargs
                for attr, operator, expected in conditions:
                    # Get actual value
                    actual = oget(item, attr, delimiter="__")

                    # Handle case of equals
                    if operator in ("equals", "iequals"):
                        # Check if case-insensitive equals
                        if (
                            operator == "iequals"
                            and isinstance(actual, str)
                            and isinstance(expected, str)
                        ):
                            # Set actual and expected to lowercase
                            actual = actual.lower()
                            expected = expected.lower()

                        # Break if actual does not equal expected
                        if actual != expected:
                            break

                    # Otherwise handle case of less than
                    elif operator in ("lt", "lte", "gt", "gte"):
                        # Break if item comparison evaluates to False
                        if not self._compare(
                            left=actual, right=expected, operator=operator
                        ):
                            break

                    # Otherwise handle case of in
                    elif operator in ("in", "iin"):
                        # Check if case-insensitive in
                        if operator == "iin" and isinstance(actual, str):
                            # Set actual to lowercase
                            actual = actual.lower()

                            # Check if expected is a string
                            if isinstance(expected, str):
                                # Set expected to lowercase
                                expected = expected.lower()

                            # Otherwise check if expected is an iterable
                            elif isinstance(expected, Iterable):
                                # Lowercase each item in expected
                                expected = set(
                                    x.lower() if isinstance(x, str) else x
                                    for x in expected
                                )

                        # Break if actual not in expected
                        if actual not in expected:
                            break

                    # Otherwise handle case of contains
                    elif operator in ("contains", "icontains"):
                        # Check if case-insensitive contains
                        if operator == "icontains" and isinstance(expected, str):
                            # Set expected to lowercase
                            expected = expected.lower()

                            # Check if actual is a string
                            if isinstance(actual, str):
                                # Set actual to lowercase
                                actual = actual.lower()

                            # Otherwise check if actual is an iterable
                            elif isinstance(actual, Iterable):
                                # Lowercase each item in actual
                                actual = set(
                                    x.lower() if isinstance(x, str) else x
                                    for x in actual
                                )

                        # Break if expected not in actual
                        if expected not in actual:
                            break

                # Otherwise yield item
                else:
                    yield item

        # Apply filter operation to items
        return self.apply(items, lambda x: operation(x))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIRST
    # └─────────────────────────────────────────────────────────────────────────────────

    def first(self, items: Items | None = None) -> Item | None:
        """Returns the first item in the collection"""

        # Initialize items
        items = self.apply(items)

        # Return the first item in the collection
        return next(iter(items), None)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ HEAD
    # └─────────────────────────────────────────────────────────────────────────────────

    def head(self, n: int, items: Items | None = None) -> Items:
        """Returns the first n items in the collection"""

        def operation(
            items: Generator[Item, None, None]
        ) -> Generator[Item, None, None]:
            """Yields the first n items in the collection"""

            # Iterate over items
            for i, item in enumerate(items):
                # Check if i is greater than or equal to n
                if i >= n:
                    # Break
                    break
                # Yield item
                yield item

        # Apply head operation to items
        return self.apply(items, lambda x: operation(x))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    def key(self, key: Any, items: Items | None = None) -> Item:
        """Returns an item by key lookup"""

        # Define does not exist error message
        does_not_exist_error_message = f"An item with the key '{key}' does not exist"

        # Check if key is not in item IDs by key
        if key not in self._item_ids_by_key:
            # Raise DoesNotExistError
            raise DoesNotExistError(does_not_exist_error_message + ".")

        # Get item ID
        item_id = self._item_ids_by_key[key]

        # Get item
        item = self._items_by_id[item_id]

        # Collect subset
        subset = list(self.collect(items=items, subset=[item]))

        # Check if subset is null
        if not subset:
            # Raise DoesNotExistError
            raise DoesNotExistError(does_not_exist_error_message + " in this subset.")

        # Unpack subset
        [item] = subset

        # Return item
        return item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LAST
    # └─────────────────────────────────────────────────────────────────────────────────

    def last(self, items: Items | None = None) -> Item | None:
        """Returns the last item in the collection"""

        # Initialize items
        items = self.apply(items)

        # Initialize window
        window = deque(items, maxlen=1)

        # Return the last item in the collection
        return window.pop() if window else None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PUSH
    # └─────────────────────────────────────────────────────────────────────────────────

    def push(self, item: Item) -> None:
        """Pushes an item to the collection"""

        # Check if item already has an ID
        if item._imeta.id is not None:
            # Set creating to False
            is_creating = False

            # Get item ID
            item_id = int(item._imeta.id)

            # Iterate over values
            for value in self._keys_by_item_id.pop(item_id, []):
                # Remove item ID from item IDs by key
                del self._item_ids_by_key[value]

        # Otherwise, handle case of new item
        else:
            # Set creating to True
            is_creating = True

            # Increment item ID
            self._item_id += 1

            # Return item ID
            item_id = self._item_id

        # Initialize keys
        keys = []

        # Iterate over key attriubutes
        for attr in item._cmeta.KEYS:
            # Check if attr is a tuple
            if isinstance(attr, tuple):
                # Get value
                value = tuple([getattr(item, a, None) for a in attr])

                # Get key
                key = tuple([self._internalize_value(item) for item in value])

            # Otherwise handle case of single attribute
            else:
                # Get value
                value = getattr(item, attr, None)

                # Get key
                key = self._internalize_value(value)

            # Check if key is in item IDs by key
            if key in self._item_ids_by_key:
                # Raise a duplicate key error
                raise DuplicateKeyError(
                    f"An item with the key '{value}' already exists."
                )

            # Append key to keys
            keys.append(key)

        # Iterate over keys
        for key in keys:
            # Add item ID to item IDs by key
            self._item_ids_by_key[key] = item_id

            # Add value to keys by item ID
            self._keys_by_item_id.setdefault(item_id, set()).add(key)

        # Update item ID
        item._imeta.id = str(item_id)

        # Check if creating
        if is_creating:
            # Deepcopy item
            item = deepcopy(item)

        # Otherwise, handle case of updating
        else:
            # Get item dict
            item_dict = item.__dict__

            # Expose item
            item = self._expose_item(item)

            # Update item dict
            item.__dict__.update(deepcopy(item_dict))

        # Internalize item
        item = self._internalize_item(item)

        # Add item to items by ID
        self._items_by_id[item_id] = item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SLICE
    # └─────────────────────────────────────────────────────────────────────────────────

    def slice(self, start: int, stop: int, items: Items | None = None) -> Items:
        """Returns a slice of items in the collection"""

        def operation(
            items: Generator[Item, None, None]
        ) -> Generator[Item, None, None]:
            """Yields a slice of items in the collection"""

            # Check if either start or stop is less than 0
            if start < 0 or stop < 0:
                # Convert items to list and yield slice
                yield from list(items)[start:stop]

            # Iterate over items
            for i, item in enumerate(items):
                # Check if i is greater than or equal to stop
                if i >= stop:
                    # Break
                    break

                # Check if i is greater than or equal to start
                if i >= start:
                    # Yield item
                    yield item

        # Apply slice operation to items
        return self.apply(items, lambda x: operation(x))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TAIL
    # └─────────────────────────────────────────────────────────────────────────────────

    def tail(self, n: int, items: Items | None = None) -> Items:
        """Returns the last n items in the collection"""

        def operation(
            items: Generator[Item, None, None]
        ) -> Generator[Item, None, None]:
            """Yields the last n items in the collection"""

            # Initialize window
            window: deque[Item] = deque(maxlen=n)

            # Iterate over items
            for item in items:
                # Append item to window
                window.append(item)

            # Iterate over window
            for item in window:
                # Yield item
                yield item

        # Apply tail operation to items
        return self.apply(items, lambda x: operation(x))
