from __future__ import annotations

# Lightweight adjacency map for offline demos; replace/enrich with Spotify related-artists later.
_GRAPH: dict[str, list[str]] = {
    "indie pop": ["dream pop", "synth pop", "bedroom pop", "art pop", "jangle pop"],
    "house": ["deep house", "tech house", "disco", "garage", "ambient house"],
    "hip hop": ["boom bap", "alt hip hop", "r&b", "trap", "jazz rap"],
    "metal": ["post-metal", "shoegaze", "prog metal", "hardcore", "doom"],
    "jazz": ["neo-soul", "broken beat", "nu jazz", "lo-fi hip hop", "fusion"],
}


def suggest_adjacent(seed: str, limit: int = 8) -> list[str]:
    key = seed.strip().lower()
    base = _GRAPH.get(key)
    if base:
        return base[:limit]
    # Unknown seed: invent gentle adjacency labels for scaffolding
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
