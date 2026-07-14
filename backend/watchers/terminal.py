"""Terminal history watcher — tails shell history files."""
import os
from pathlib import Path

from . import BaseWatcher
from ..config import config


class TerminalWatcher(BaseWatcher):
    name = "terminal"

    def _poll(self) -> list[dict]:
        items = []
        for hist_path in config.SHELL_HISTORY:
            p = Path(hist_path)
            if not p.exists():
                continue

            try:
                # Read last 50 lines of history
                lines = self._tail(p, 50)
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#") and len(line) > 5:
                        # Skip thread's own commands
                        if "thread" in line.lower() or "supermemory" in line.lower():
                            continue
                        items.append({
                            "content": f"Terminal command: {line}",
                            "url": f"shell://{p.name}",
                        })
            except Exception:
                continue

        return items

    @staticmethod
    def _tail(path: Path, n: int) -> list[str]:
        """Read last n lines of a file without loading the whole thing."""
        try:
            with open(path, "rb") as f:
                f.seek(0, os.SEEK_END)
                size = f.tell()
                # Read last 64KB, should cover n lines
                chunk_size = min(size, 65536)
                f.seek(max(0, size - chunk_size))
                data = f.read().decode("utf-8", errors="replace")
                lines = data.splitlines()
                return lines[-n:]
        except Exception:
            return []
