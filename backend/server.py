"""
Thread API server — FastAPI app with search, profile, and ingest endpoints.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from .config import config
from .sm_client import memory
from .watchers import start_all_watchers

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("thread")

_running_watchers = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: launch watchers
    logger.info(f"Starting watchers for sources: {config.SOURCES}")
    global _running_watchers
    _running_watchers = start_all_watchers(memory, config.SOURCES)
    yield
    # Shutdown
    for w in _running_watchers:
        w.stop()


app = FastAPI(
    title="Thread API",
    description="Local memory vault — search your digital life",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    return {"status": "ok", "watchers": [w.name for w in _running_watchers]}


@app.get("/search")
async def search(q: str = Query(..., description="Search query"), limit: int = 10):
    """Search across all ingested memories."""
    results = memory.search(q, limit=limit)
    return JSONResponse(results)


@app.get("/profile")
async def profile(q: str = Query("", description="Contextual query")):
    """Get learned user profile and recent context."""
    profile_data = memory.profile(q)
    return JSONResponse(profile_data)


@app.post("/ingest")
async def ingest(content: str, source: str = "manual", url: str = ""):
    """Manually ingest content into the memory vault."""
    result = memory.ingest(content=content, source=source, url=url)
    return JSONResponse(result)


def main():
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT, log_level="info")


if __name__ == "__main__":
    main()
