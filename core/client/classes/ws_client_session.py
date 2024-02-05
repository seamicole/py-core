# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from multiprocessing import Manager
from multiprocessing.managers import SyncManager


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ WS CLIENT SESSION
# └─────────────────────────────────────────────────────────────────────────────────────


class WSClientSession:
    """An websocket client session utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, manager: SyncManager | None = None) -> None:
        """Init Method"""

        # Initialize a manager
        self._manager = manager or Manager()

        # Initialize lock
        self._lock = self._manager.Lock()
