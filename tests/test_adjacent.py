from vibeshift.discovery.adjacent import suggest_adjacent


def test_known_seed():
    out = suggest_adjacent("indie pop", limit=3)
    assert len(out) == 3
    assert "dream pop" in out


def test_unknown_seed_still_returns():
    out = suggest_adjacent("kelpcore", limit=4)
    assert len(out) == 4
