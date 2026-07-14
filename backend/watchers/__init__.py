"""Watcher — common base and registry."""
import threading
import logging
from abc import ABC, abstractmethod
from pathlib import Path

logger = logging.getLogger(__name__)


class BaseWatcher(ABC):
    """Every watcher ingests content into the shared memory client."""

    def __init__(self, memory_client):
        self.memory = memory_client
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()

    name: str = "base"  # Override in subclass: 'browser', 'terminal', 'files'

    @abstractmethod
    def _poll(self) -> list[dict]:
        """Return list of {'content': str, 'url': str} items to ingest."""
        ...

    def _loop(self):
        """Poll-loop: fetch new items → ingest → sleep."""
        seen = set()
        while not self._stop.is_set():
            try:
                for item in self._poll():
                    fingerprint = item["content"][:200]
                    if fingerprint not in seen:
                        seen.add(fingerprint)
                        self.memory.ingest(
                            content=item["content"],
                            source=self.name,
                            url=item.get("url", ""),
                        )
            except Exception as e:
                logger.error(f"[{self.name}] poll error: {e}")

            self._stop.wait(timeout=30)

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True, name=f"watcher-{self.name}")
        self._thread.start()
        logger.info(f"[{self.name}] watcher started")

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=5)
        logger.info(f"[{self.name}] watcher stopped")


def start_all_watchers(memory_client, sources: list[str]):
    """Start watchers for the requested sources. Returns list of running watchers."""
    watchers = []

    if "browser" in sources:
        from .browser import BrowserWatcher
        w = BrowserWatcher(memory_client)
        w.start()
        watchers.append(w)

    if "terminal" in sources:
        from .terminal import TerminalWatcher
        w = TerminalWatcher(memory_client)
        w.start()
        watchers.append(w)

    if "files" in sources:
        from .files import FileWatcher
        w = FileWatcher(memory_client)
        w.start()
        watchers.append(w)

    return watchers
