from __future__ import annotations

import typer
from rich import print

from vibeshift import __version__
from vibeshift.discovery.adjacent import suggest_adjacent

app = typer.Typer(help="vibeshift — Spotify + iCloud playlist & genre discovery")


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
    """Suggest adjacent genres/artists (heuristic scaffold; Spotify enrich later)."""
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


if __name__ == "__main__":
    app()
