"""Terminal history watcher — tails shell history files."""
import os
import re
from pathlib import Path

from . import BaseWatcher
from ..config import config

# Shell internals that provide zero value as memories
_SKIP_PATTERNS = [
    re.compile(r"^set\s+[+-]o\s+\w+$"),      # set +o noclobber, set -o emacs, etc.
    re.compile(r"^:\s+\d+:\d+;"),             # zsh timestamp markers like ": 1780683784:0;"
    re.compile(r"^:\s+\d+;"),                  # shorter zsh timestamps
    re.compile(r"^bindkey\s"),                 # keybinding config
    re.compile(r"^compdef\s"),                 # completion definitions
    re.compile(r"^autoload\s"),                # zsh autoload
    re.compile(r"^zstyle\s"),                  # zsh style config
    re.compile(r"^typeset\s"),                 # zsh typeset/variable declarations
    re.compile(r"^unset\s"),                   # unset vars
    re.compile(r"^export\s[A-Z_]+\s*$"),       # bare export VAR (no value)
    re.compile(r"^alias\s"),                   # alias definitions
    re.compile(r"^eval\s"),                    # eval wrapper
]

# Commands too short to be meaningful (with no arguments)
_SHORT_NOISE = {"ls", "cd", "pwd", "clear", "exit", "whoami", "date", "echo", "true", "false"}


class TerminalWatcher(BaseWatcher):
    name = "terminal"

    def _poll(self) -> list[dict]:
        items = []
        for hist_path in config.SHELL_HISTORY:
            p = Path(hist_path)
            if not p.exists():
                continue

            try:
                lines = self._tail(p, 50)
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if not self._is_meaningful(line):
                        continue
                    items.append({
                        "content": f"Terminal command: {line}",
                        "url": f"shell://{p.name}",
                    })
            except Exception:
                continue

        return items

    @staticmethod
    def _is_meaningful(line: str) -> bool:
        """Filter out shell internals and noise commands."""
        # Skip thread/supermemory internals
        if "thread" in line.lower() or "supermemory" in line.lower():
            return False

        # Skip known noise patterns
        for pat in _SKIP_PATTERNS:
            if pat.match(line):
                return False

        # Skip very short noise commands
        cmd = line.split()[0] if line.split() else ""
        if cmd in _SHORT_NOISE and len(line.split()) <= 2:
            return False

        # Must have meaningful content
        return len(line) > 10

    @staticmethod
    def _tail(path: Path, n: int) -> list[str]:
        """Read last n lines of a file without loading the whole thing."""
        try:
            with open(path, "rb") as f:
                f.seek(0, os.SEEK_END)
                size = f.tell()
                chunk_size = min(size, 65536)
                f.seek(max(0, size - chunk_size))
                data = f.read().decode("utf-8", errors="replace")
                lines = data.splitlines()
                return lines[-n:]
        except Exception:
            return []
