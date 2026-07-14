<img align="center" src="https://img.shields.io/badge/THREAD-memory_vault-FFB7B2?style=for-the-badge" alt="Thread" />

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue?style=flat-square" alt="Python" />
  <img src="https://img.shields.io/badge/fastapi-0.139-009688?style=flat-square" alt="FastAPI" />
  <img src="https://img.shields.io/badge/supermemory-3.50-6366f1?style=flat-square" alt="Supermemory" />
  <img src="https://img.shields.io/badge/vite-8.1-646cff?style=flat-square" alt="Vite" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License" />
</p>

<h1 align="center">Thread</h1>
<h3 align="center"><i>Your digital life, woven together.</i></h3>

<p align="center"><strong>Thread watches your browser, terminal, and files — building a personal knowledge graph so you never lose a thought again.</strong></p>

<p align="center">
  <a href="#the-problem">Problem</a> •
  <a href="#the-solution">Solution</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#api">API</a> •
  <a href="#faq">FAQ</a> •
  <a href="#powered-by">Powered By</a>
</p>

---

## The Problem

| Problem | Impact |
|---------|--------|
| You work across 5+ tools daily — browser, terminal, editor, chats, docs | Each tool has its own isolated history. Nothing connects them. |
| AI coding agents forget everything between sessions | You waste 10 minutes re-explaining your codebase to Claude / Cursor / Codex every time. |
| You found something important last week but can't remember where | Browser history is a flat list. Terminal history is a flat file. No semantic search. |
| Existing solutions require manual effort | Note-taking, bookmarking, copy-pasting — all require you to remember to save things. |

## The Solution

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Browser    │    │   Terminal   │    │    Files     │
│   History    │    │   History    │    │   (recent)   │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │   Thread    │
                    │  Backend    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Supermemory │
                    │    Graph    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──┐  ┌──────▼──┐  ┌─────▼─────┐
       │  Search │  │ Profile │  │  Dynamic  │
       │  (RAG)  │  │ (facts) │  │ Dreaming  │
       └─────────┘  └─────────┘  └───────────┘
```

**What you get:**
- Continuous ingestion from browser, terminal, and file changes
- Semantic search across your entire digital history
- Auto-built knowledge graph connecting related facts across sources
- User profile that learns what you care about
- Compatible with any AI coding agent via REST API
- Everything runs locally — your data stays on your machine

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Thread Server                     │
│                  (FastAPI :8000)                     │
├─────────────────┬─────────────────┬─────────────────┤
│  BrowserWatcher │ TerminalWatcher │  FileWatcher    │
│  (sqlite3 read) │  (history tail) │  (os.walk +     │
│  Firefox/Chrome │  .zsh/.bash     │   mtime check)  │
├─────────────────┴─────────────────┴─────────────────┤
│                  sm_client.py                        │
│         ┌─────────────────────────────┐             │
│         │     Supermemory Cloud       │             │
│         │     (api.supermemory.ai)    │             │
│         └─────────────┬───────────────┘             │
│                       │                             │
│         ┌─────────────▼───────────────┐             │
│         │    Groq Fallback (optional) │             │
│         │    Enriches low-confidence  │             │
│         │    search results           │             │
│         └─────────────────────────────┘             │
└─────────────────────────────────────────────────────┘
```

| Layer | Technology |
|-------|-----------|
| Memory Engine | [Supermemory](https://supermemory.ai) — graph memory + SuperRAG + dynamic dreaming |
| Backend | Python 3.11+ / FastAPI / uvicorn |
| Watchers | sqlite3 (browser), os + file I/O (terminal/files), watchdog |
| Fallback LLM | Groq (llama-3.3-70b) — optional enrichment |
| Landing Page | Vite + React + TypeScript + Tailwind CSS v4 + GSAP + Lenis |

## Quick Start

**Prerequisites:** Python 3.11+, Node.js 18+

```bash
# 1. Clone
git clone https://github.com/subheeksh5599/thread-memory.git
cd thread-memory

# 2. Install backend deps
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Add your SUPERMEMORY_API_KEY from https://console.supermemory.ai
# Optional: add GROQ_API_KEY for fallback enrichment

# 4. One-shot ingestion
python -m backend.ingest --all

# 5. Start the server + continuous watchers
python -m backend.server
# → http://localhost:8000

# 6. Search your memory
curl "http://localhost:8000/search?q=deployment+fix+from+last+week"

# 7. Run the demo (for hackathon video)
python demo.py
```

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Server status + active watcher count |
| `/search?q=...&limit=10` | GET | Semantic search across all ingested memories |
| `/profile?q=...` | GET | Learned user profile (static + dynamic facts) |
| `/ingest` | POST | Manually ingest content into the memory vault |

**POST /ingest**

| Parameter | Type | Description |
|-----------|------|-------------|
| `content` | string | Text content to ingest |
| `source` | string | Source label: `browser`, `terminal`, `files`, or `manual` |
| `url` | string | Optional URL for traceability |

## How It Uses Supermemory

| Feature | Integration |
|---------|------------|
| **Content Extraction** | All ingested content flows through Supermemory's extraction pipeline — browser URLs, shell commands, and file snippets are parsed into structured facts |
| **Graph Memory** | Connected facts across sources: "that CSS trick" → "this component" → "last week's bug fix" — all linked in a single knowledge graph |
| **Dynamic Dreaming** | Auto-discovers relationships: "you researched rate limiting 3 times this month — here's what you've learned" |
| **SuperRAG** | Semantic search across your entire digital history, not just one tool — finds the deployment fix you ran 3 days ago |
| **User Profiles** | Learns which sources and topics you return to most, building a persistent profile of your interests and expertise |

## FAQ

<details>
<summary><strong>What does Thread watch?</strong></summary>

Thread connects to your browser history (Firefox/Chrome SQLite databases), terminal history (`.zsh_history` / `.bash_history`), and recently modified files in your watched directories. Everything stays local — your raw data never leaves your machine.
</details>

<details>
<summary><strong>Do I need to run a server?</strong></summary>

Thread runs as a lightweight background process on `localhost:8000`. Start it once and it continuously watches your activity. The REST API is available for search and queries from any tool.
</details>

<details>
<summary><strong>Is my data private?</strong></summary>

Yes. Thread runs entirely on your machine. Only extracted memories (not raw browsing data or file contents) are synced to Supermemory when you choose to use the cloud API. For full privacy, use Supermemory Local — the self-hosted version that runs on `localhost:6767`.
</details>

<details>
<summary><strong>Can I use it with AI coding agents?</strong></summary>

Absolutely. Thread exposes a standard REST API. Pipe your Thread memories into Claude Code, Cursor, Codex, or any tool that can make HTTP requests. Persistent project context across sessions.
</details>

<details>
<summary><strong>What's the Groq fallback for?</strong></summary>

When Supermemory returns search results below a confidence threshold, Thread can optionally enrich them using Groq's LLM. This provides a synthesized answer even when the source fragments are fragmented. Groq is optional — Thread works fine without it.
</details>

<details>
<summary><strong>How is this different from browser history search?</strong></summary>

Browser history is a flat, chronological list. Thread builds a semantic knowledge graph — you search by meaning, not by URL. "What was that deployment fix?" finds the right terminal command, even if the word "deployment" wasn't in the command.
</details>

## Powered By

<p align="center">
  <strong>Supermemory</strong> — <i>State-of-the-art memory and context infrastructure for AI agents</i><br />
  <strong>FastAPI</strong> — <i>Modern Python web framework</i><br />
  <strong>Vite + React</strong> — <i>Next-generation frontend tooling</i>
</p>

## License

MIT. Build whatever you want with it.
