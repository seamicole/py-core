# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.api.classes.api_channel_event import APIChannelEvent
from core.collection.classes.dict_collection import DictCollection


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ API CHANNEL EVENT COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class APIChannelEventCollection(DictCollection[APIChannelEvent]):
    """A dict-based collection utility class for APIChannelEvent instances"""
