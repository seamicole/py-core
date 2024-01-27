# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OSET
# └─────────────────────────────────────────────────────────────────────────────────────


def oset(
    instance: object | dict[Any, Any],
    path: Any,
    value: Any,
    delimiter: str = ".",
    insert: bool = False,
) -> None:
    """Sets a value in a nested dictionary using a path string"""

    # Check if the path is a tuple
    if isinstance(path, tuple):
        # Check if the value to set is not a tuple or list
        if not isinstance(value, (tuple, list)):
            # Convert value to set to a list
            value = [value] * len(path)

        # Iterate over zip of path and value to set
        for path_i, value_i in zip(path, value):
            # Remap data
            oset(instance, path_i, value_i, insert=insert)

    # Otherwise, handle case of string path
    elif isinstance(path, str):
        # Split the path into keys
        keys = path.split(delimiter)

        # Iterate over keys
        for key in keys[:-1]:
            # Check if dict
            if isinstance(instance, dict):
                # Check if key exists
                if insert and key not in instance:
                    # Set key to empty dictionary
                    instance[key] = {}

                # Get value by key
                instance = instance[key]

            # Otherwise handle object
            else:
                # Check if key exists
                if insert and not hasattr(instance, key):
                    # Set key to empty dictionary
                    setattr(instance, key, {})

                # Get value by key
                instance = getattr(instance, key)

        # Check if dict
        if isinstance(instance, dict):
            # Check if insert is False
            if not insert:
                instance[keys[-1]]

            # Set value by last key
            instance[keys[-1]] = value

        # Otherwise handle object
        else:
            # Check if insert is False
            if not insert:
                getattr(instance, keys[-1])

            # Set value by last key
            setattr(instance, keys[-1], value)

    # Otherwise, handle general case
    else:
        # Check if dict
        if isinstance(instance, dict):
            # Set value by path
            instance[path] = value

        # Otherwise handle object
        else:
            # Set value by path
            setattr(instance, path, value)
