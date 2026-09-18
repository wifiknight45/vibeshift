"""Apple MusicKit / Music API scaffold.

Developer token = JWT signed with your MusicKit .p8 key (Team ID + Key ID).
Music User Token = obtained via MusicKit JS / native auth in a browser or app
(cannot be minted server-side from Apple ID password).
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
import jwt

from vibeshift.config import Settings, get_settings

API = "https://api.music.apple.com/v1"


def developer_token(settings: Settings | None = None, ttl_seconds: int = 60 * 60 * 12) -> str:
    s = settings or get_settings()
    if not (s.apple_team_id and s.apple_key_id and s.apple_private_key_path):
        raise RuntimeError(
            "Set APPLE_TEAM_ID, APPLE_KEY_ID, and APPLE_PRIVATE_KEY_PATH (.p8) in .env"
        )
    key_path = Path(s.apple_private_key_path)
    if not key_path.exists():
        raise RuntimeError(f"Apple private key not found: {key_path}")
    private_key = key_path.read_text()
    now = int(time.time())
    payload = {
        "iss": s.apple_team_id,
        "iat": now,
        "exp": now + ttl_seconds,
    }
    headers = {"alg": "ES256", "kid": s.apple_key_id}
    return jwt.encode(payload, private_key, algorithm="ES256", headers=headers)


@dataclass
class AppleMusicClient:
    settings: Settings

    def configured_developer(self) -> bool:
        return bool(
            self.settings.apple_team_id
            and self.settings.apple_key_id
            and self.settings.apple_private_key_path
        )

    def configured_user(self) -> bool:
        return bool(self.settings.apple_music_user_token)

    def status(self) -> dict[str, Any]:
        return {
            "developer_token_ready": self.configured_developer(),
            "music_user_token_set": self.configured_user(),
            "storefront": self.settings.apple_storefront,
            "note": (
                "Music User Token must come from MusicKit authorization in a browser/app; "
                "paste into APPLE_MUSIC_USER_TOKEN. See docs/APPLE_MUSIC.md."
            ),
        }

    def _headers(self, user: bool = False) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {developer_token(self.settings)}",
            "Music-User-Token": self.settings.apple_music_user_token or "",
        }
        if user and not self.settings.apple_music_user_token:
            raise RuntimeError("Set APPLE_MUSIC_USER_TOKEN (from MusicKit user auth)")
        return headers

    def storefront_charts(self, limit: int = 10) -> dict[str, Any]:
        """Catalog call (developer token only) — good connectivity smoke test."""
        sf = self.settings.apple_storefront
        with httpx.Client(timeout=30.0) as client:
            r = client.get(
                f"{API}/catalog/{sf}/charts",
                headers=self._headers(user=False),
                params={"types": "songs", "limit": limit},
            )
            r.raise_for_status()
            return r.json()

    def library_playlists(self, limit: int = 20) -> dict[str, Any]:
        """Requires Music User Token."""
        with httpx.Client(timeout=30.0) as client:
            r = client.get(
                f"{API}/me/library/playlists",
                headers=self._headers(user=True),
                params={"limit": limit},
            )
            r.raise_for_status()
            return r.json()


def get_apple_music_client() -> AppleMusicClient:
    return AppleMusicClient(settings=get_settings())
