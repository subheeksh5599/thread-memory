"""Browser history watcher — reads Firefox, Chrome, Chromium, Brave, Edge history databases."""
import os
import shutil
import sqlite3
import tempfile
import time
from pathlib import Path

from . import BaseWatcher
from ..config import config


class BrowserWatcher(BaseWatcher):
    name = "browser"

    # 24-hour window in microseconds (Firefox uses microseconds)
    _LOOKBACK_SECONDS = 86400  # 24 hours
    _LOOKBACK_MICRO = _LOOKBACK_SECONDS * 1_000_000
    # Chrome uses milliseconds since 1601
    _LOOKBACK_CHROME = _LOOKBACK_SECONDS * 1_000_000  # microseconds since 1601

    # Firefox profile patterns (supports default, default-release, *.default)
    _FIREFOX_PATTERNS = ["*.default", "*.default-release", "*.default-*"]

    def _poll(self) -> list[dict]:
        items = []
        seen_urls = set()

        # Firefox
        for db_path in self._find_firefox_dbs():
            items.extend(self._read_firefox(db_path, seen_urls))

        # Chrome-based browsers
        for db_path in self._find_chrome_dbs():
            items.extend(self._read_chrome(db_path, seen_urls))

        return items[:30]

    # ── Firefox ───────────────────────────────────────

    def _find_firefox_dbs(self) -> list[str]:
        """Find all Firefox profile databases."""
        dbs = []
        ff_base = Path(config.BROWSER_DB).expanduser()
        if not ff_base.exists():
            return dbs

        for pattern in self._FIREFOX_PATTERNS:
            for profile in ff_base.glob(pattern):
                db = profile / "places.sqlite"
                if db.exists():
                    dbs.append(str(db))
        return dbs

    def _read_firefox(self, db_path: str, seen: set) -> list[dict]:
        items = []
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=3)
            cursor = conn.cursor()
            threshold = int((time.time() - self._LOOKBACK_SECONDS) * 1_000_000)
            cursor.execute(
                """
                SELECT url, title, visit_count
                FROM moz_places
                WHERE last_visit_date > ?
                ORDER BY last_visit_date DESC
                LIMIT 30
                """,
                (threshold,),
            )
            for url, title, visits in cursor.fetchall():
                if url and url not in seen and self._is_meaningful_url(url):
                    seen.add(url)
                    items.append({
                        "content": f"Visited: {title or url} — {url}",
                        "url": url,
                    })
            conn.close()
        except Exception:
            pass
        return items

    # ── Chrome-based ───────────────────────────────────

    def _find_chrome_dbs(self) -> list[str]:
        """Find all Chrome-based browser history databases."""
        browsers = [
            Path.home() / ".config/google-chrome",
            Path.home() / ".config/chromium",
            Path.home() / ".config/brave",
            Path.home() / ".config/microsoft-edge",
            Path.home() / ".config/vivaldi",
        ]
        dbs = []
        for base in browsers:
            if not base.exists():
                continue
            # Check Default profile and any other profiles
            for profile in base.iterdir():
                if not profile.is_dir():
                    continue
                db = profile / "History"
                if db.exists():
                    dbs.append(str(db))
        return dbs

    def _read_chrome(self, db_path: str, seen: set) -> list[dict]:
        """Read Chrome history. Chrome locks the DB, so copy it first."""
        items = []
        tmp = None
        try:
            # Copy to temp file since Chrome locks the DB
            tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
            tmp.close()
            shutil.copy2(db_path, tmp.name)

            conn = sqlite3.connect(f"file:{tmp.name}?mode=ro", uri=True, timeout=3)
            cursor = conn.cursor()

            # Chrome timestamps are microseconds since 1601-01-01
            # Python: seconds since 1970. Offset: 11644473600 seconds
            chrome_now = int((time.time() + 11644473600) * 1_000_000)
            threshold = chrome_now - self._LOOKBACK_CHROME

            cursor.execute(
                """
                SELECT url, title, visit_count
                FROM urls
                WHERE last_visit_time > ?
                ORDER BY last_visit_time DESC
                LIMIT 30
                """,
                (threshold,),
            )
            for url, title, visits in cursor.fetchall():
                if url and url not in seen and self._is_meaningful_url(url):
                    seen.add(url)
                    items.append({
                        "content": f"Visited: {title or url} — {url}",
                        "url": url,
                    })
            conn.close()
        except Exception:
            pass
        finally:
            if tmp and os.path.exists(tmp.name):
                try:
                    os.unlink(tmp.name)
                except Exception:
                    pass
        return items

    # ── Helpers ────────────────────────────────────────

    @staticmethod
    def _is_meaningful_url(url: str) -> bool:
        skip_prefixes = (
            "about:", "place:", "chrome:", "edge:", "brave:",
            "chrome-extension:", "moz-extension:",
        )
        return not url.startswith(skip_prefixes)
