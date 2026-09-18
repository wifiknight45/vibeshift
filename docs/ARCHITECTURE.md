# vibeshift architecture

## Goals
1. Import listening context (Spotify + Apple Music / iCloud library export)
2. Suggest adjacent genres & artists
3. Materialize playlists on Spotify (and later Apple Music)

## Honest API notes
- **Spotify**: Web API supports OAuth, playlists, related artists, audio features (where available).
- **iCloud.com**: no official scrape API. Prefer **Apple MusicKit** / MusicKit JS, or user-provided library export.
- Keep secrets in `.env` only.

## Next milestones
1. Spotify Auth Code + create playlist from draft
2. Related-artists enrichment for `suggest_adjacent`
3. Apple MusicKit library read (optional)
4. CLI `vibeshift sync` dry-run → apply


## Perplexity research
- Use the **official Perplexity API** (`sonar` / Sonar models) for web-grounded adjacent genre & artist research.
- Do **not** scrape perplexity.com HTML — against ToS and fragile.
- Set `PERPLEXITY_API_KEY`; discovery falls back to local heuristics when unset or on API errors.
- CLI: `vibeshift suggest "indie pop"` (API if keyed) or `vibeshift suggest "indie pop" --offline`.
