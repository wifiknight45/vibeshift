from __future__ import annotations

import json

import typer
from rich import print

from vibeshift import __version__
from vibeshift.config import get_settings
from vibeshift.discovery.adjacent import suggest_adjacent

app = typer.Typer(help="vibeshift — Spotify + Apple Music playlist & genre discovery")
spotify_app = typer.Typer(help="Spotify OAuth + API")
apple_app = typer.Typer(help="Apple MusicKit / Music API")
app.add_typer(spotify_app, name="spotify")
app.add_typer(apple_app, name="apple")


@app.command()
def version() -> None:
    """Print package version."""
    print(f"vibeshift {__version__}")


@app.command("suggest")
def suggest(
    seed: str = typer.Argument(..., help="Seed genre or artist, e.g. 'indie pop'"),
    limit: int = typer.Option(8, help="How many adjacent ideas to return"),
    offline: bool = typer.Option(False, help="Skip Perplexity; use local heuristics only"),
) -> None:
    """Suggest adjacent genres/artists (Perplexity if keyed, else heuristics)."""
    ideas = suggest_adjacent(seed, limit=limit, use_perplexity=not offline)
    for i, idea in enumerate(ideas, 1):
        print(f"[cyan]{i}.[/cyan] {idea}")


@app.command("playlist-draft")
def playlist_draft(
    name: str = typer.Option("Vibe Shift Mix", help="Playlist title"),
    seeds: list[str] = typer.Argument(..., help="Seed tracks/artists/genres"),
) -> None:
    """Print a local playlist draft (no Spotify write until OAuth is configured)."""
    from vibeshift.playlist.builder import draft_playlist

    draft = draft_playlist(name=name, seeds=seeds)
    print(draft)


@app.command("status")
def status() -> None:
    """Show which integrations are configured."""
    s = get_settings()
    from vibeshift.icloud.musickit import get_apple_music_client
    from vibeshift.spotify.client import get_spotify_client
    from vibeshift.spotify import oauth as spotify_oauth

    print(
        {
            "spotify": {
                "client_configured": get_spotify_client().configured(),
                "logged_in": spotify_oauth.load_tokens(s) is not None,
            },
            "apple_music": get_apple_music_client().status(),
            "perplexity": bool(s.perplexity_api_key),
        }
    )


@spotify_app.command("login")
def spotify_login(
    no_browser: bool = typer.Option(False, help="Print URL instead of opening a browser"),
) -> None:
    """OAuth login (Authorization Code + localhost callback)."""
    from vibeshift.spotify.oauth import login_interactive

    tokens = login_interactive(open_browser=not no_browser)
    print(f"[green]Spotify login OK[/green] (expires_at={tokens.expires_at:.0f})")


@spotify_app.command("me")
def spotify_me() -> None:
    """Show the logged-in Spotify profile."""
    from vibeshift.spotify.client import get_spotify_client

    me = get_spotify_client().me()
    print({"id": me.get("id"), "display_name": me.get("display_name"), "product": me.get("product")})


@spotify_app.command("playlists")
def spotify_playlists(limit: int = typer.Option(20)) -> None:
    """List playlists for the logged-in user."""
    from vibeshift.spotify.client import get_spotify_client

    items = get_spotify_client().my_playlists(limit=limit)
    for p in items:
        print(f"- {p.get('name')} ({p.get('id')})")


@apple_app.command("status")
def apple_status() -> None:
    """Show Apple MusicKit configuration status."""
    from vibeshift.icloud.musickit import get_apple_music_client

    print(get_apple_music_client().status())


@apple_app.command("token")
def apple_token() -> None:
    """Mint a MusicKit developer JWT (does not print full token by default)."""
    from vibeshift.icloud.musickit import developer_token

    tok = developer_token()
    print(f"[green]Developer token minted[/green] (len={len(tok)}; not printed)")


@apple_app.command("charts")
def apple_charts(limit: int = typer.Option(5)) -> None:
    """Smoke-test catalog charts with the developer token."""
    from vibeshift.icloud.musickit import get_apple_music_client

    data = get_apple_music_client().storefront_charts(limit=limit)
    print(json.dumps(data, indent=2)[:2000])


@apple_app.command("library-playlists")
def apple_library_playlists(limit: int = typer.Option(20)) -> None:
    """List Apple Music library playlists (needs APPLE_MUSIC_USER_TOKEN)."""
    from vibeshift.icloud.musickit import get_apple_music_client

    data = get_apple_music_client().library_playlists(limit=limit)
    print(json.dumps(data, indent=2)[:3000])


if __name__ == "__main__":
    app()
