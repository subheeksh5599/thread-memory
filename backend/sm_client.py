"""
Supermemory client wrapper with optional Groq fallback.
"""
import logging
from datetime import datetime, timezone
from typing import Optional

import httpx
from supermemory import Supermemory

from .config import config

logger = logging.getLogger(__name__)


class MemoryClient:
    """Wraps Supermemory API with Groq fallback for search enrichment."""

    def __init__(self):
        self.sm = Supermemory(
            api_key=config.SUPERMEMORY_API_KEY,
            base_url=config.SUPERMEMORY_BASE_URL,
        )
        self._groq_available = bool(config.GROQ_API_KEY)

    # ── Ingest ──────────────────────────────────────────────

    def ingest(self, content: str, source: str, url: str = "") -> dict:
        """
        Feed content into Supermemory. The content is tagged with
        its source type (browser/terminal/file) so search results
        are traceable.
        """
        tag = f"{config.CONTAINER_TAG}/{source}"

        metadata = {"source": source, "ingested_at": datetime.now(timezone.utc).isoformat()}
        if url:
            metadata["url"] = url

        try:
            result = self.sm.add(
                content=content,
                container_tag=tag,
            )
            logger.info(f"Ingested {source}: {content[:80]}...")
            return {"status": "ok", "source": source, "result": result}
        except Exception as e:
            logger.error(f"Ingest failed [{source}]: {e}")
            return {"status": "error", "source": source, "error": str(e)}

    # ── Search ──────────────────────────────────────────────

    def search(self, query: str, limit: int = 10) -> dict:
        """Search across all ingested memories."""
        try:
            results = self.sm.search.memories(
                q=query,
                container_tag=config.CONTAINER_TAG,
                limit=limit,
            )
            # Response is SearchMemoriesResponse with .results list
            hits = []
            for r in results.results:
                hits.append({
                    "memory": r.memory or r.chunk or "",
                    "id": r.id,
                    "similarity": r.similarity,
                    "metadata": r.metadata or {},
                    "filepath": r.filepath,
                })

            # Groq enrichment for low-confidence results
            enriched = None
            if self._groq_available and hits:
                enriched = self._groq_enrich(query, hits)

            return {
                "query": query,
                "hits": hits[:limit],
                "enriched": enriched,
            }
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {"query": query, "hits": [], "error": str(e)}

    # ── Profile ──────────────────────────────────────────────

    def profile(self, query: str = "") -> dict:
        """Get learned user profile + relevant context."""
        try:
            profile = self.sm.profile(
                container_tag=config.CONTAINER_TAG,
                q=query or "",
            )
            return {
                "static_facts": profile.profile.static or [],
                "dynamic_context": profile.profile.dynamic or [],
                "memories": [
                    {"memory": getattr(r, "memory", ""), "similarity": getattr(r, "similarity", 0)}
                    for r in (profile.search_results.results if profile.search_results else [])
                ],
            }
        except Exception as e:
            logger.error(f"Profile fetch failed: {e}")
            return {"error": str(e)}

    # ── Groq fallback ────────────────────────────────────────

    def _groq_enrich(self, query: str, hits: list[dict]) -> Optional[str]:
        """Use Groq to summarize / connect dots across low-confidence hits."""
        if not self._groq_available:
            return None

        ctx = "\n".join(
            f"- {h.get('memory', '')[:200]}" for h in hits[:5]
        )
        prompt = (
            f"User query: {query}\n\n"
            f"Relevant fragments from the user's digital history:\n{ctx}\n\n"
            "Synthesize these into a concise answer. If the fragments don't contain "
            "enough information, say so honestly. Max 3 sentences."
        )

        try:
            resp = httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {config.GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 150,
                },
                timeout=10,
            )
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"Groq enrichment failed: {e}")
            return None


# Singleton
memory = MemoryClient()
