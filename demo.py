#!/usr/bin/env python3
"""
Thread demo script — showcases ingestion + search for the hackathon video.
Run this after setting SUPERMEMORY_API_KEY in .env.

Usage:
    python demo.py
"""
import sys
import time
import subprocess

# Simulated content from different sources
DEMO_CONTENT = [
    # Browser visits
    ("browser", "Visited: Next.js 15 Documentation — https://nextjs.org/docs", "https://nextjs.org/docs"),
    ("browser", "Visited: Tailwind CSS v4 Migration Guide — https://tailwindcss.com/docs/v4", "https://tailwindcss.com/docs/v4"),
    ("browser", "Visited: Supermemory API Docs — https://supermemory.ai/docs", "https://supermemory.ai/docs"),
    ("browser", "Visited: Solana RPC Methods — https://solana.com/docs/rpc", "https://solana.com/docs/rpc"),

    # Terminal commands
    ("terminal", "Terminal command: git push origin main", "shell://.zsh_history"),
    ("terminal", "Terminal command: npm install @supermemory/tools", "shell://.zsh_history"),
    ("terminal", "Terminal command: docker-compose up -d postgres redis", "shell://.zsh_history"),
    ("terminal", "Terminal command: curl -X POST https://api.example.com/deploy -d '{\"env\":\"prod\"}'", "shell://.zsh_history"),
    ("terminal", "Terminal command: pytest backend/tests/ -x --tb=short", "shell://.zsh_history"),

    # File changes
    ("files", "File [config.py]: class Config: DEBUG = False; DATABASE_URL = 'postgresql://...'", "file:///projects/app/config.py"),
    ("files", "File [middleware.ts]: export function rateLimit(req: Request) { const ip = req.headers.get('x-forwarded-for') }", "file:///projects/app/middleware.ts"),
    ("files", "File [deploy.sh]: #!/bin/bash; rsync -avz ./dist/ user@server:/var/www/app/; ssh user@server 'systemctl restart app'", "file:///projects/app/deploy.sh"),
    ("files", "File [README.md]: # Thread — Local memory vault for your digital life. Built for Supermemory Localhost:6767.", "file:///projects/thread/README.md"),
]


def demo_ingest():
    """Feed demo content into the Thread API."""
    print("=" * 60)
    print("  THREAD DEMO — Ingesting digital footprint")
    print("=" * 60)

    for source, content, url in DEMO_CONTENT:
        emoji = {"browser": "🌐", "terminal": "💻", "files": "📁"}.get(source, "📌")
        print(f"\n{emoji} [{source}] {content[:80]}...")

        # Send to API
        result = subprocess.run(
            [
                "curl", "-s", "-X", "POST",
                f"http://localhost:8000/ingest?content={content}&source={source}&url={url}",
            ],
            capture_output=True, text=True,
        )
        print(f"   ↳ {result.stdout.strip()}")
        time.sleep(0.3)

    print("\n✅ {0} items ingested into Supermemory".format(len(DEMO_CONTENT)))
    time.sleep(2)


def demo_search():
    """Run search queries against the Thread API."""
    queries = [
        "How do I deploy the app?",
        "What CSS framework are we migrating to?",
        "database configuration",
        "rate limiting middleware",
    ]

    print("\n" + "=" * 60)
    print("  THREAD DEMO — Searching your memory")
    print("=" * 60)

    for q in queries:
        print(f"\n🔍 {q}")
        result = subprocess.run(
            ["curl", "-s", f"http://localhost:8000/search?q={q}&limit=3"],
            capture_output=True, text=True,
        )
        print(f"   {result.stdout.strip()[:300]}")
        time.sleep(0.5)


def demo_profile():
    """Show learned user profile."""
    print("\n" + "=" * 60)
    print("  THREAD DEMO — Your learned profile")
    print("=" * 60)

    result = subprocess.run(
        ["curl", "-s", "http://localhost:8000/profile"],
        capture_output=True, text=True,
    )
    print(f"\n{result.stdout.strip()[:500]}")


if __name__ == "__main__":
    # Check if server is running
    health = subprocess.run(
        ["curl", "-s", "http://localhost:8000/health"],
        capture_output=True, text=True,
    )
    if "ok" not in health.stdout:
        print("❌ Thread server not running. Start with: python -m backend.server")
        sys.exit(1)

    demo_ingest()
    demo_search()
    demo_profile()

    print("\n" + "=" * 60)
    print("  Demo complete. Thread remembers everything. 🧵")
    print("=" * 60)
