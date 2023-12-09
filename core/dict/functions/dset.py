# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DSET
# └─────────────────────────────────────────────────────────────────────────────────────


def dset(
    dictionary: dict[Any, Any], path: Any, value: Any, delimiter: str = "."
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
            dset(dictionary, path_i, value_i)

    # Otherwise, handle case of string path
    elif isinstance(path, str):
        # Split the path into keys
        keys = path.split(delimiter)

        # Iterate over keys
        for key in keys[:-1]:
            # Check if key exists
            if key not in dictionary:
                # Set key to empty dictionary
                dictionary[key] = {}

            # Get value by key
            dictionary = dictionary[key]

        # Set value by last key
        dictionary[keys[-1]] = value

    # Otherwise, handle general case
    else:
        # Set value by path
        dictionary[path] = value
