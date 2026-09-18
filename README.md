# vibeshift

Python toolkit that connects **iCloud** and **Spotify** to:

- build and sync playlists across services
- discover **adjacent genres / artists** from what you already like
- generate “vibe shift” mixes (same energy, new territory)
- optional **Perplexity AI** research for adjacent genres/artists (official API)

> Status: early scaffold. Spotify Web API first; iCloud Music / Apple Music paths documented with honest API limits.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # Spotify + optional PERPLEXITY_API_KEY
vibeshift --help
```

## Layout

```
src/vibeshift/
  spotify/     # Spotify OAuth + playlist APIs
  icloud/      # iCloud / Apple Music bridge (scaffold)
  discovery/   # adjacent genre & artist suggestions
  playlist/    # playlist build / merge / export
```

## Privacy

Tokens stay in local env / encrypted at rest. Never commit `.env`.

## License

MIT
