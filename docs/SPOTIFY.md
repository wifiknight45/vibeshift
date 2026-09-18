# Spotify OAuth setup

1. Create an app at https://developer.spotify.com/dashboard
2. Add redirect URI exactly: `http://127.0.0.1:8080/callback`
3. Put credentials in `.env`:
```
SPOTIFY_CLIENT_ID=...
SPOTIFY_CLIENT_SECRET=...
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8080/callback
```

## CLI
```bash
vibeshift spotify login
vibeshift spotify me
vibeshift spotify playlists
vibeshift status
```

Tokens are stored locally in `.vibeshift/spotify_tokens.json` (gitignored).
