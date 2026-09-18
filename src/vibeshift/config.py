from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    spotify_client_id: str | None = None
    spotify_client_secret: str | None = None
    spotify_redirect_uri: str = "http://127.0.0.1:8080/callback"
    spotify_scopes: str = (
        "playlist-modify-public playlist-modify-private "
        "playlist-read-private user-library-read user-top-read"
    )

    # Apple MusicKit / Music API
    apple_team_id: str | None = None
    apple_key_id: str | None = None
    apple_private_key_path: str | None = None  # path to AuthKey_XXX.p8
    apple_music_user_token: str | None = None  # short-lived; from MusicKit JS/auth
    apple_storefront: str = "us"

    perplexity_api_key: str | None = None
    perplexity_model: str = "sonar"
    vibeshift_log_level: str = "INFO"
    vibeshift_token_dir: str = ".vibeshift"


def get_settings() -> Settings:
    return Settings()


def token_dir(settings: Settings | None = None) -> Path:
    s = settings or get_settings()
    path = Path(s.vibeshift_token_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path
