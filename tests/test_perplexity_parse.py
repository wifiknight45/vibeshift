from vibeshift.discovery.perplexity import _parse_list


def test_parse_json_array():
    assert _parse_list('["dream pop", "synth pop"]', limit=5) == ["dream pop", "synth pop"]


def test_parse_fenced():
    raw = '```json\n["a", "b", "c"]\n```'
    assert _parse_list(raw, limit=2) == ["a", "b"]
