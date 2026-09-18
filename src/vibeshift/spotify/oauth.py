from __future__ import annotations

import json
import secrets
import threading
import time
import urllib.parse
import webbrowser
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

import httpx

from vibeshift.config import Settings, get_settings, token_dir

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"


@dataclass
class SpotifyTokens:
    access_token: str
    refresh_token: str | None
    expires_at: float
    token_type: str = "Bearer"
    scope: str | None = None

    def expired(self, skew: int = 60) -> bool:
        return time.time() >= (self.expires_at - skew)

    def to_dict(self) -> dict[str, Any]:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at,
            "token_type": self.token_type,
            "scope": self.scope,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SpotifyTokens":
        return cls(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            expires_at=float(data["expires_at"]),
            token_type=data.get("token_type") or "Bearer",
            scope=data.get("scope"),
        )


def _token_path(settings: Settings) -> Path:
    return token_dir(settings) / "spotify_tokens.json"


def save_tokens(tokens: SpotifyTokens, settings: Settings | None = None) -> Path:
    s = settings or get_settings()
    path = _token_path(s)
    path.write_text(json.dumps(tokens.to_dict(), indent=2))
    return path


def load_tokens(settings: Settings | None = None) -> SpotifyTokens | None:
    s = settings or get_settings()
    path = _token_path(s)
    if not path.exists():
        return None
    return SpotifyTokens.from_dict(json.loads(path.read_text()))


def auth_url(settings: Settings, state: str) -> str:
    q = urllib.parse.urlencode(
        {
            "client_id": settings.spotify_client_id,
            "response_type": "code",
            "redirect_uri": settings.spotify_redirect_uri,
            "scope": settings.spotify_scopes,
            "state": state,
            "show_dialog": "false",
        }
    )
    return f"{AUTH_URL}?{q}"


def exchange_code(settings: Settings, code: str) -> SpotifyTokens:
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.spotify_redirect_uri,
    }
    with httpx.Client(timeout=30.0) as client:
        resp = client.post(
            TOKEN_URL,
            data=data,
            auth=(settings.spotify_client_id or "", settings.spotify_client_secret or ""),
        )
        resp.raise_for_status()
        body = resp.json()
    return SpotifyTokens(
        access_token=body["access_token"],
        refresh_token=body.get("refresh_token"),
        expires_at=time.time() + int(body.get("expires_in", 3600)),
        token_type=body.get("token_type") or "Bearer",
        scope=body.get("scope"),
    )


def refresh(settings: Settings, tokens: SpotifyTokens) -> SpotifyTokens:
    if not tokens.refresh_token:
        raise RuntimeError("No Spotify refresh_token; run `vibeshift spotify-login` again")
    data = {
        "grant_type": "refresh_token",
        "refresh_token": tokens.refresh_token,
    }
    with httpx.Client(timeout=30.0) as client:
        resp = client.post(
            TOKEN_URL,
            data=data,
            auth=(settings.spotify_client_id or "", settings.spotify_client_secret or ""),
        )
        resp.raise_for_status()
        body = resp.json()
    return SpotifyTokens(
        access_token=body["access_token"],
        refresh_token=body.get("refresh_token") or tokens.refresh_token,
        expires_at=time.time() + int(body.get("expires_in", 3600)),
        token_type=body.get("token_type") or "Bearer",
        scope=body.get("scope") or tokens.scope,
    )


def get_valid_tokens(settings: Settings | None = None) -> SpotifyTokens:
    s = settings or get_settings()
    tokens = load_tokens(s)
    if not tokens:
        raise RuntimeError("Not logged in. Run: vibeshift spotify-login")
    if tokens.expired():
        tokens = refresh(s, tokens)
        save_tokens(tokens, s)
    return tokens


def login_interactive(settings: Settings | None = None, open_browser: bool = True) -> SpotifyTokens:
    """Localhost redirect OAuth (Authorization Code)."""
    s = settings or get_settings()
    if not s.spotify_client_id or not s.spotify_client_secret:
        raise RuntimeError("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env")

    parsed = urllib.parse.urlparse(s.spotify_redirect_uri)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 8080
    path = parsed.path or "/callback"

    state = secrets.token_urlsafe(16)
    result: dict[str, str] = {}
    error_box: dict[str, str] = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            u = urllib.parse.urlparse(self.path)
            if u.path != path:
                self.send_response(404)
                self.end_headers()
                return
            qs = urllib.parse.parse_qs(u.query)
            if qs.get("state", [None])[0] != state:
                error_box["error"] = "state mismatch"
            elif "error" in qs:
                error_box["error"] = qs["error"][0]
            else:
                result["code"] = qs.get("code", [""])[0]
            body = b"<html><body><h1>vibeshift</h1><p>You can close this tab.</p></body></html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):  # noqa: A003
            return

    server = HTTPServer((host, port), Handler)
    thread = threading.Thread(target=server.handle_request, daemon=True)
    thread.start()

    url = auth_url(s, state)
    if open_browser:
        webbrowser.open(url)
    else:
        print(url)

    thread.join(timeout=180)
    server.server_close()

    if error_box.get("error"):
        raise RuntimeError(f"Spotify auth error: {error_box['error']}")
    if not result.get("code"):
        raise RuntimeError("No auth code received (timed out?). Re-run spotify-login.")

    tokens = exchange_code(s, result["code"])
    save_tokens(tokens, s)
    return tokens
