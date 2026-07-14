"""
Thread configuration — loaded from environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")


class Config:
    # Supermemory
    SUPERMEMORY_API_KEY: str = os.getenv("SUPERMEMORY_API_KEY", "")
    SUPERMEMORY_BASE_URL: str = os.getenv("SUPERMEMORY_BASE_URL", "https://api.supermemory.ai")

    # Groq fallback
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Thread settings
    CONTAINER_TAG: str = os.getenv("THREAD_CONTAINER_TAG", "thread_user")
    SOURCES: list[str] = os.getenv("THREAD_SOURCES", "browser,terminal,files").split(",")

    # Watch paths
    WATCH_DIRS: list[str] = [
        str(Path(p).expanduser())
        for p in os.getenv("THREAD_WATCH_DIRS", "~/projects,~/Documents").split(",")
    ]
    BROWSER_DB: str = str(Path(os.getenv("THREAD_BROWSER_DB", "~/.mozilla/firefox")).expanduser())
    SHELL_HISTORY: list[str] = [
        str(Path(p).expanduser())
        for p in os.getenv("THREAD_SHELL_HISTORY", "~/.bash_history,~/.zsh_history").split(",")
    ]

    # Server
    HOST: str = os.getenv("THREAD_HOST", "127.0.0.1")
    PORT: int = int(os.getenv("THREAD_PORT", "8000"))


config = Config()
