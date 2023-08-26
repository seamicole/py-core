from core.collections.classes.store import Store
from core.collections.classes.item import Item
from core.clients.mixins.api_mixin import APIMixin
from core.clients.classes.api_endpoint import APIEndpoint

store = Store()


class MEXC(Item, APIMixin):
    """A currency exchange class for MEXC"""

    # Set key
    KEY = "mexc"

    # Set name
    NAME = "MEXC"

    # Set API base URL
    API_BASE_URL = "https://api.mexc.com"

    # Set API endpoints
    API_ENDPOINTS = [
        {
            "kind": "currency",
            "method": "GET",
            "base_url": "https://www.mexc.com/",
            "route": "open/api/v2/market/coin/list",
            "json_root": "data",
            "json_schema": {"code": "currency", "precision": "precision"},
        },
    ]

    class Meta(Item.Meta):
        KEYS = ("KEY",)
        ITEMS = store.get_or_create("exchanges")


mexc = MEXC()

print(mexc)
print(mexc.api.endpoints)
print(APIEndpoint._cmeta.items)
print(APIEndpoint.items.filter(kind="currency_pair"))
