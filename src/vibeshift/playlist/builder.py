from __future__ import annotations

from vibeshift.discovery.adjacent import suggest_adjacent


def draft_playlist(name: str, seeds: list[str]) -> dict:
    lanes: list[dict] = []
    for seed in seeds:
        lanes.append({"seed": seed, "adjacent": suggest_adjacent(seed, limit=5)})
    return {
        "name": name,
        "seeds": seeds,
        "lanes": lanes,
        "note": "Draft only — connect Spotify OAuth to create a real playlist.",
    }
