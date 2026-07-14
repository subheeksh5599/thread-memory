"""Browser history watcher — reads Firefox/Chrome history databases."""
import sqlite3
import time
from pathlib import Path

from . import BaseWatcher
from ..config import config


class BrowserWatcher(BaseWatcher):
    name = "browser"

    # Common browser history DB locations
    _FIREFOX_PATTERN = "places.sqlite"
    _CHROME_PATTERN = "History"

    def _poll(self) -> list[dict]:
        items = []
        db_path = self._find_history_db()
        if not db_path:
            return items

        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=2)
            cursor = conn.cursor()

            # Get URLs from the last hour
            one_hour_ago = int((time.time() - 3600) * 1_000_000)  # microseconds
            cursor.execute(
                """
                SELECT url, title, visit_count
                FROM moz_places
                WHERE last_visit_date > ?
                ORDER BY last_visit_date DESC
                LIMIT 30
                """,
                (one_hour_ago,),
            )
            for url, title, visits in cursor.fetchall():
                if url and not url.startswith("about:") and not url.startswith("place:"):
                    items.append({
                        "content": f"Visited: {title or url} — {url}",
                        "url": url,
                    })
            conn.close()
        except Exception:
            pass

        return items

    def _find_history_db(self) -> str | None:
        """Find Firefox or Chrome history database."""
        candidates = []

        # Firefox
        ff_base = Path(config.BROWSER_DB).expanduser()
        for profile in ff_base.glob("*.default*"):
            db = profile / self._FIREFOX_PATTERN
            if db.exists():
                candidates.append(str(db))

        # Chrome
        chrome_paths = [
            Path.home() / ".config/google-chrome/Default/History",
            Path.home() / ".config/chromium/Default/History",
            Path.home() / ".config/brave/Default/History",
        ]
        for p in chrome_paths:
            if p.exists():
                candidates.append(str(p))

        return candidates[0] if candidates else None
