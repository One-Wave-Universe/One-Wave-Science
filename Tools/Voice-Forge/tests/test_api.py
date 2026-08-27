"""End-to-end tests for the HTTP API a Custom GPT Action (or any other
external caller) plugs into: create a voice profile from an upload,
find it again, and combine two voices into a rendered, saveable third."""
import importlib
import io
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

fastapi = pytest.importorskip("fastapi")

from engine import io_utils  # noqa: E402
from tools.make_sample_voices import synth_voice  # noqa: E402

SR = 16000


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("VOICE_FORGE_LIBRARY", str(tmp_path / "library"))
    monkeypatch.delenv("VOICE_FORGE_API_KEY", raising=False)
    import api.main as main_module

    importlib.reload(main_module)
    from fastapi.testclient import TestClient

    return TestClient(main_module.app)


def _voice_bytes(seed, f0):
    y = synth_voice(SR, duration=0.8, f0=f0, formants=[(700, 12, 3.0), (1400, 10, 3.0)], breath=0.02, seed=seed)
    buf = io.BytesIO()
    import soundfile as sf

    sf.write(buf, y, SR, format="WAV")
    buf.seek(0)
    return buf


def test_create_find_get_delete_voice(client):
    r = client.post(
        "/voices",
        files={"file": ("voice.wav", _voice_bytes(1, 120.0), "audio/wav")},
        data={"name": "Test Voice", "description": "a test", "tags": "alpha, beta"},
    )
    assert r.status_code == 200
    voice = r.json()
    assert voice["name"] == "Test Voice"
    assert voice["tags"] == ["alpha", "beta"]
    assert voice["duration_sec"] > 0

    r = client.get("/voices", params={"query": "test"})
    assert r.status_code == 200
    assert any(v["id"] == voice["id"] for v in r.json())

    r = client.get(f"/voices/{voice['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == voice["id"]

    r = client.delete(f"/voices/{voice['id']}")
    assert r.status_code == 200
    assert client.get(f"/voices/{voice['id']}").status_code == 404


def test_combine_voices_and_fetch_render(client):
    r_a = client.post(
        "/voices",
        files={"file": ("a.wav", _voice_bytes(10, 110.0), "audio/wav")},
        data={"name": "Voice A"},
    )
    r_b = client.post(
        "/voices",
        files={"file": ("b.wav", _voice_bytes(11, 200.0), "audio/wav")},
        data={"name": "Voice B"},
    )
    voice_a, voice_b = r_a.json(), r_b.json()

    r = client.post(
        "/voices/combine",
        json={
            "voice_id_a": voice_a["id"],
            "voice_id_b": voice_b["id"],
            "amount_a": 0.6,
            "amount_b": 0.4,
            "pitch_semitones": 1.0,
            "save_as_name": "Combined Voice",
            "save_as_tags": ["blend"],
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["audio_url"].endswith(".wav")
    assert body["saved_voice"]["name"] == "Combined Voice"
    assert set(body["saved_voice"]["parent_ids"]) == {voice_a["id"], voice_b["id"]}

    path = "/" + body["audio_url"].split("://", 1)[1].split("/", 1)[1]
    file_resp = client.get(path)
    assert file_resp.status_code == 200
    assert len(file_resp.content) > 1000


def test_combine_unknown_voice_404(client):
    r = client.post("/voices/combine", json={"voice_id_a": "nope", "voice_id_b": "also-nope"})
    assert r.status_code == 404


def test_api_key_enforced_when_set(client, monkeypatch):
    monkeypatch.setenv("VOICE_FORGE_API_KEY", "secret123")
    import api.main as main_module

    importlib.reload(main_module)
    from fastapi.testclient import TestClient

    protected_client = TestClient(main_module.app)

    r = protected_client.get("/voices")
    assert r.status_code == 401

    r = protected_client.get("/voices", headers={"X-API-Key": "secret123"})
    assert r.status_code == 200
