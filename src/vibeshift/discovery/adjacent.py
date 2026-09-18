from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

# Lightweight adjacency map for offline demos; enrich with Perplexity / Spotify later.
_GRAPH: dict[str, list[str]] = {
    "indie pop": ["dream pop", "synth pop", "bedroom pop", "art pop", "jangle pop"],
    "house": ["deep house", "tech house", "disco", "garage", "ambient house"],
    "hip hop": ["boom bap", "alt hip hop", "r&b", "trap", "jazz rap"],
    "metal": ["post-metal", "shoegaze", "prog metal", "hardcore", "doom"],
    "jazz": ["neo-soul", "broken beat", "nu jazz", "lo-fi hip hop", "fusion"],
}


def suggest_adjacent(seed: str, limit: int = 8, use_perplexity: bool = True) -> list[str]:
    """Suggest adjacent genres/artists. Tries Perplexity API when configured."""
    if use_perplexity:
        try:
            from vibeshift.discovery import perplexity as pplx

            if pplx.configured():
                ideas = pplx.research_adjacent(seed, limit=limit)
                if ideas:
                    return ideas
        except Exception as exc:  # noqa: BLE001 — soft fallback
            logger.warning("Perplexity research failed, using heuristic: %s", exc)

    key = seed.strip().lower()
    base = _GRAPH.get(key)
    if base:
        return base[:limit]
    return [
        f"{seed} × lo-fi",
        f"ambient {seed}",
        f"alt {seed}",
        f"{seed} adjacent pop",
        f"neo-{seed}",
        f"{seed} remix culture",
        f"crossover {seed}",
        f"late-night {seed}",
    ][:limit]
