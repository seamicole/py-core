# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any, Callable, Union


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ARGS AND KWARGS
# └─────────────────────────────────────────────────────────────────────────────────────

# Define a generic Args type
Args = tuple[Any, ...]

# Define a generic Kwargs type
Kwargs = Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ JSON
# └─────────────────────────────────────────────────────────────────────────────────────

# Define a generic JSON value type
JSONValue = str | int | float | bool | None

# Define a generic JSON dict type
JSONDict = dict[str, Union[JSONValue, "JSON", list["JSON"]]]

# Define a generic JSON list type
JSONList = list[Union[JSONValue, "JSON", JSONDict]]

# Define a generic JSON type
JSON = JSONValue | JSONDict | JSONList

# Define a generic JSON schema type
JSONSchema = dict[str | tuple[str, ...], str | Callable[[Any, Any], Any]]
