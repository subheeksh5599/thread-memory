"""One-shot ingestion — scan all sources once and feed into Supermemory."""
import argparse
import logging

from .config import config
from .sm_client import memory
from .watchers.browser import BrowserWatcher
from .watchers.terminal import TerminalWatcher
from .watchers.files import FileWatcher

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("thread.ingest")


def run():
    parser = argparse.ArgumentParser(description="Thread — one-shot memory ingestion")
    parser.add_argument("--browser", action="store_true", help="Ingest browser history")
    parser.add_argument("--terminal", action="store_true", help="Ingest terminal history")
    parser.add_argument("--files", action="store_true", help="Ingest recent file changes")
    parser.add_argument("--all", action="store_true", help="Ingest all sources")
    parser.add_argument("--text", type=str, help="Directly ingest a text string")
    args = parser.parse_args()

    if args.all:
        args.browser = args.terminal = args.files = True

    total = 0

    if args.browser:
        w = BrowserWatcher(memory)
        items = w._poll()
        for item in items:
            memory.ingest(item["content"], source="browser", url=item.get("url", ""))
            total += 1
        logger.info(f"Browser: {len(items)} URLs ingested")

    if args.terminal:
        w = TerminalWatcher(memory)
        items = w._poll()
        for item in items:
            memory.ingest(item["content"], source="terminal", url=item.get("url", ""))
            total += 1
        logger.info(f"Terminal: {len(items)} commands ingested")

    if args.files:
        w = FileWatcher(memory)
        items = w._poll()
        for item in items:
            memory.ingest(item["content"], source="files", url=item.get("url", ""))
            total += 1
        logger.info(f"Files: {len(items)} files ingested")

    if args.text:
        memory.ingest(args.text, source="manual")
        total += 1
        logger.info("Manual text ingested")

    logger.info(f"\nDone. {total} items ingested into Supermemory.")
    logger.info(f"Container tag: {config.CONTAINER_TAG}")
    logger.info("Run 'python -m backend.server' to start the API + continuous watchers.")


if __name__ == "__main__":
    run()
