"""
Thread — Local memory vault for your digital life.
Watches browser history, terminal commands, and files.
Feeds everything into Supermemory Local for persistent,
searchable memory.

Usage:
    python -m thread.server          # Start the API server + watchers
    python -m thread.ingest          # One-shot ingestion from all sources
    python -m thread.search "query"  # Search your memory
"""

__version__ = "0.1.0"
