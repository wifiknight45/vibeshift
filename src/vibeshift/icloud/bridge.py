from __future__ import annotations

from vibeshift.icloud.musickit import get_apple_music_client


def status() -> dict:
    return get_apple_music_client().status()
