# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.collections.classes.item_meta import ClassMeta, InstanceMeta
from core.collections.classes.items import Items

if TYPE_CHECKING:
    from core.collections.classes.item import Item


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ITEM METACLASS
# └─────────────────────────────────────────────────────────────────────────────────────


class ItemMetaclass(type):
    """A metaclass for the Item class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of Meta
    Meta: type[ClassMeta]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of class meta
    _cmeta: ClassMeta

    # Declare type of instance meta
    _imeta: InstanceMeta

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __CALL__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __call__(cls, *args: Any, **kwargs: Any) -> Item:
        """Call Method"""

        # Create instance
        instance: Item = super().__call__(*args, **kwargs)

        # Initialize meta
        instance._imeta = InstanceMeta()

        # Return instance
        return instance

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]
    ) -> None:
        """Init Method"""

        # Call super method
        super().__init__(name, bases, attrs)

        # Check if Meta is not a subclass of ClassMeta
        if not issubclass(cls.Meta, ClassMeta):
            # Define a new Meta class
            class Meta(ClassMeta):
                """Meta Class"""

            # Iterate over attributes of Meta
            for attr in dir(cls.Meta):
                # Skip private attributes
                if attr.startswith("__"):
                    continue

                # Set attribute
                setattr(Meta, attr, getattr(cls.Meta, attr))

            # Set Meta
            cls.Meta = Meta

        # Ensure that keys is a tuple
        cls.Meta.KEYS = tuple(cls.Meta.KEYS)

        # Ensure that indexes is a tuple
        cls.Meta.INDEXES = tuple(cls.Meta.INDEXES)

        # Initialize meta
        cls._cmeta = cls.Meta()

        # Initialize parents
        PARENTS = []

        # Iterate over bases
        for Base in cls.__bases__:
            # Continue if base is not of type ItemMetaclass
            if not isinstance(Base, ItemMetaclass):
                continue

            # Append base to parents
            PARENTS.append(Base)

        # Set parents
        cls._cmeta.PARENTS = tuple(PARENTS)

        # Iterate over parents
        for Parent in cls._cmeta.PARENTS:
            # Add child to parent children
            Parent._cmeta.CHILDREN += (cls,)

            # Add child to parent items
            Parent._cmeta.items._children += (cls._cmeta.items,)

        # Add clean keys method to items
        cls._cmeta.items._clean_keys = cls._cmeta.clean_keys

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ITEMS
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def items(cls) -> Items:
        """Returns the items of the item's meta instance"""

        # Return meta items
        return cls._cmeta.items
