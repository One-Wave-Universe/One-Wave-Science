from onewave_mapper.cli import run


def test_cli_end_to_end_smoke(tmp_path):
    root = run(str(tmp_path))
    assert (root / "session.json").exists()
    assert (root / "audio" / "raw_multichannel.wav").exists()
    exports = list((root / "exports").glob("*.json"))
    assert len(exports) == 1
