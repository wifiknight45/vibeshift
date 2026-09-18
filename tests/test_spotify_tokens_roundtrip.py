import time
from vibeshift.spotify.oauth import SpotifyTokens


def test_token_roundtrip(tmp_path, monkeypatch):
    from vibeshift import config
    from vibeshift.spotify import oauth

    monkeypatch.setenv("VIBESHIFT_TOKEN_DIR", str(tmp_path))
    # reload settings path via explicit settings
    s = config.Settings(vibeshift_token_dir=str(tmp_path))
    tokens = SpotifyTokens(
        access_token="a",
        refresh_token="r",
        expires_at=time.time() + 3600,
    )
    oauth.save_tokens(tokens, s)
    loaded = oauth.load_tokens(s)
    assert loaded is not None
    assert loaded.access_token == "a"
    assert loaded.refresh_token == "r"
