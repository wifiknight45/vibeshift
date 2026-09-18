from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ICloudBridge:
    """Placeholder for Apple Music library import / playlist export."""

    def status(self) -> str:
        return (
            "scaffold: use Apple MusicKit for catalog/playlists; "
            "optional CSV/XML library export as an offline import path"
        )
