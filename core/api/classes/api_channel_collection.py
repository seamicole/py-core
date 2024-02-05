# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.api.classes.api_channel import APIChannel
from core.collection.classes.dict_collection import DictCollection


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ API CHANNEL COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class APIChannelCollection(DictCollection[APIChannel]):
    """A dict-based collection utility class for APIChannel instances"""
