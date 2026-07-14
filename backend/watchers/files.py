"""File system watcher — monitors directories for changes."""
import time
from pathlib import Path

from . import BaseWatcher
from ..config import config


class FileWatcher(BaseWatcher):
    name = "files"

    # File extensions we care about
    _TEXT_EXTENSIONS = {
        ".py", ".js", ".ts", ".tsx", ".jsx", ".rs", ".go", ".java",
        ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".cfg",
        ".html", ".css", ".scss", ".sol", ".vy", ".sh", ".bash",
        ".env", ".gitignore", ".dockerignore", "Dockerfile",
        ".c", ".cpp", ".h", ".hpp", ".rb", ".php", ".swift",
        ".kt", ".sql", ".graphql", ".r", ".m", ".mm",
    }
    _SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv",
                   "dist", "build", ".next", ".turbo", "target", ".supermemory"}

    def _poll(self) -> list[dict]:
        items = []
        now = time.time()
        one_hour_ago = now - 3600

        for watch_dir in config.WATCH_DIRS:
            p = Path(watch_dir)
            if not p.exists():
                continue

            for file_path in p.rglob("*"):
                if not file_path.is_file():
                    continue

                # Skip hidden/binary/build dirs
                if any(part in self._SKIP_DIRS for part in file_path.parts):
                    continue
                if file_path.suffix.lower() not in self._TEXT_EXTENSIONS:
                    continue

                # Only recently modified
                try:
                    mtime = file_path.stat().st_mtime
                    if mtime < one_hour_ago:
                        continue
                except OSError:
                    continue

                # Read file snippet (first 500 chars)
                try:
                    snippet = file_path.read_text(encoding="utf-8", errors="replace")[:500]
                except Exception:
                    continue

                if snippet.strip():
                    rel = str(file_path.relative_to(watch_dir))
                    items.append({
                        "content": f"File [{rel}]: {snippet}",
                        "url": f"file://{file_path}",
                    })

        return items[:30]  # Cap at 30 per poll
