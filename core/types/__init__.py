# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Union


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
