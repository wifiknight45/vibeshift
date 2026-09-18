from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from vibeshift.config import Settings, get_settings
from vibeshift.spotify.oauth import get_valid_tokens


API = "https://api.spotify.com/v1"


@dataclass
class SpotifyClient:
    settings: Settings

    def configured(self) -> bool:
        return bool(self.settings.spotify_client_id and self.settings.spotify_client_secret)

    def _headers(self) -> dict[str, str]:
        tokens = get_valid_tokens(self.settings)
        return {"Authorization": f"Bearer {tokens.access_token}"}

    def me(self) -> dict[str, Any]:
        with httpx.Client(timeout=30.0) as client:
            r = client.get(f"{API}/me", headers=self._headers())
            r.raise_for_status()
            return r.json()

    def my_playlists(self, limit: int = 20) -> list[dict[str, Any]]:
        with httpx.Client(timeout=30.0) as client:
            r = client.get(
                f"{API}/me/playlists",
                headers=self._headers(),
                params={"limit": limit},
            )
            r.raise_for_status()
            return list(r.json().get("items") or [])


def get_spotify_client() -> SpotifyClient:
    return SpotifyClient(settings=get_settings())
