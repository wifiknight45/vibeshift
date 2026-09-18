from __future__ import annotations

from dataclasses import dataclass

from vibeshift.config import Settings, get_settings


@dataclass
class SpotifyClient:
    """Minimal Spotify client stub. Wire Client Credentials / Auth Code next."""

    settings: Settings

    def configured(self) -> bool:
        return bool(self.settings.spotify_client_id and self.settings.spotify_client_secret)


def get_spotify_client() -> SpotifyClient:
    return SpotifyClient(settings=get_settings())
