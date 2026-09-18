# Apple Music / MusicKit setup

Apple does **not** allow vibeshift to sign in with your Apple ID password or scrape iCloud.com.

## What you need
1. [Apple Developer](https://developer.apple.com) membership
2. A **MusicKit** key (`.p8`) + **Key ID** + **Team ID**
3. A **Music User Token** from MusicKit authorization in a browser or app (user grants Apple Music access)

## `.env`
```
APPLE_TEAM_ID=XXXXXXXXXX
APPLE_KEY_ID=YYYYYYYYYY
APPLE_PRIVATE_KEY_PATH=/absolute/path/to/AuthKey_YYYYYYYYYY.p8
APPLE_MUSIC_USER_TOKEN=  # paste after MusicKit user auth
APPLE_STOREFRONT=us
```

## CLI
```bash
vibeshift apple status
vibeshift apple token          # mints developer JWT (smoke)
vibeshift apple charts         # catalog call with developer token
vibeshift apple library-playlists   # needs Music User Token
```

## Getting a Music User Token
Use Apple’s MusicKit JS (or a tiny local HTML page) so the user authorizes Apple Music; copy the token into `APPLE_MUSIC_USER_TOKEN`. Tokens expire — refresh via MusicKit when calls start failing with 401/403.
