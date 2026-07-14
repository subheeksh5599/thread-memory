# Thread

> Local memory vault for your digital life. Built for **Supermemory Localhost:6767**.

Thread watches your browser history, terminal commands, and file changes — weaving everything into a unified knowledge graph via Supermemory. Search across your entire digital history from one place.

## How it uses Supermemory Local

1. **Content extraction** — browser URLs, shell commands, and file snippets flow into Supermemory's extraction pipeline
2. **Graph memory** — connected facts across sources: "that CSS trick" → "this component" → "last week's bug fix"
3. **Dynamic dreaming** — auto-discovers relationships: "you researched rate limiting 3 times this month"
4. **SuperRAG** — semantic search across your entire digital history, not just one tool
5. **User profiles** — learns which sources and topics you return to most
6. **Groq fallback** — enriches low-confidence Supermemory results with Groq's LLM

## Quickstart

```bash
# 1. Clone & install
cd thread
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Set your API key
cp .env.example .env
# Edit .env — add your SUPERMEMORY_API_KEY from console.supermemory.ai
# Optional: add GROQ_API_KEY for fallback enrichment

# 3. One-shot ingestion
python -m backend.ingest --all

# 4. Start the continuous watcher server
python -m backend.server
# → http://localhost:8000

# 5. Search your memory
curl "http://localhost:8000/search?q=deployment+fix+from+last+week"
```

## API

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Server status + active watchers |
| `GET /search?q=...&limit=10` | Semantic search across all memories |
| `GET /profile?q=...` | Learned user profile + recent context |
| `POST /ingest` | Manually ingest content |

## Architecture

```
browser watcher ──┐
terminal watcher ─┼── Supermemory API ── Graph memory
file watcher ─────┘        │
                           ├── SuperRAG (search)
                           ├── Dynamic dreaming
                           └── Groq fallback (low confidence)
```

## Winner pattern

Based on **chief** (3rd prize, YC Call My Agent Hackathon, May 2026) — an ambient agent that proactively surfaces relevant memories during phone calls. Thread applies the same pattern to your entire desktop workflow: don't make the user search their memory, make the memory come to them.
