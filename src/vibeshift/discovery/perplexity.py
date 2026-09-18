"""Perplexity Sonar API for adjacent genre/artist research.

Uses the official chat/completions API — do not scrape perplexity.com.
Docs: https://docs.perplexity.ai/
"""
from __future__ import annotations

import json
import logging
import os
import re
from typing import Any

import httpx

logger = logging.getLogger(__name__)

PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"
DEFAULT_MODEL = "sonar"


def _api_key() -> str | None:
    return (os.environ.get("PERPLEXITY_API_KEY") or "").strip() or None


def configured() -> bool:
    return _api_key() is not None


def research_adjacent(seed: str, limit: int = 8, model: str | None = None) -> list[str]:
    """Ask Perplexity for adjacent genres/artists; return a clean string list."""
    key = _api_key()
    if not key:
        raise RuntimeError("PERPLEXITY_API_KEY is not set")

    prompt = (
        f"You help music discovery. Seed: {seed!r}.\n"
        f"Return ONLY a JSON array of up to {limit} strings — adjacent genres "
        f"and/or similar artists (no explanations, no markdown)."
    )
    payload: dict[str, Any] = {
        "model": model or os.environ.get("PERPLEXITY_MODEL") or DEFAULT_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Reply with valid JSON only. Prefer music-industry genre and artist names.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    with httpx.Client(timeout=45.0) as client:
        resp = client.post(PERPLEXITY_URL, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

    content = (
        data.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )
    return _parse_list(content, limit=limit)


def _parse_list(content: str, limit: int) -> list[str]:
    text = (content or "").strip()
    # Strip fenced code if the model wraps JSON
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(x).strip() for x in parsed if str(x).strip()][:limit]
    except json.JSONDecodeError:
        pass
    # Fallback: bullet / comma lines
    items: list[str] = []
    for line in re.split(r"[\n,]", text):
        cleaned = re.sub(r"^[\-\*\d\.\)\s]+", "", line).strip().strip('"')
        if cleaned:
            items.append(cleaned)
    return items[:limit]
