# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Callable, Literal, Union

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.client.enums.http_method import HTTPMethod as HTTPMethod  # noqa: F401
from core.dict.classes.dict_schema_context import DictSchemaContext
from core.dict.types import DictSchema


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ HTTP METHOD
# └─────────────────────────────────────────────────────────────────────────────────────

HTTPMethodLiteral = Literal["DELETE", "GET", "POST"]

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
JSONSchema = DictSchema

# Define a generic JSON filter type
JSONFilter = Callable[[DictSchemaContext], bool]
