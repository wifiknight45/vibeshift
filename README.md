[![License](https://img.shields.io/github/license/wifiknight45/vibeshift)](https://github.com/wifiknight45/vibeshift)
[![GitHub stars](https://img.shields.io/github/stars/wifiknight45/vibeshift?style=social)](https://github.com/wifiknight45/vibeshift/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/wifiknight45/vibeshift)](https://github.com/wifiknight45/vibeshift/commits)
[![Top language](https://img.shields.io/github/languages/top/wifiknight45/vibeshift)](https://github.com/wifiknight45/vibeshift)
[![Issues](https://img.shields.io/github/issues/wifiknight45/vibeshift)](https://github.com/wifiknight45/vibeshift/issues)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Spotify](https://img.shields.io/badge/Spotify-OAuth-1DB954.svg)](https://developer.spotify.com/)
[![Apple Music](https://img.shields.io/badge/Apple%20Music-MusicKit-black.svg)](https://developer.apple.com/musickit/)
[![Perplexity](https://img.shields.io/badge/Perplexity-Sonar%20API-7C3AED.svg)](https://docs.perplexity.ai/)

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

## Connect accounts

```bash
# Spotify
cp .env.example .env   # fill SPOTIFY_* 
vibeshift spotify login
vibeshift spotify me

# Apple Music (MusicKit — needs Apple Developer key + Music User Token)
# see docs/APPLE_MUSIC.md and docs/SPOTIFY.md
vibeshift apple status
```

## Privacy

Tokens stay in local env / encrypted at rest. Never commit `.env`.

## License

MIT
