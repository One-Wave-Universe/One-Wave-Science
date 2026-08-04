import io
import json
import urllib.error

import pytest

from council_chamber.models import Message
from council_chamber.seats.gemini_client import (
    GeminiAPIError,
    GeminiNotConfiguredError,
    make_gemini_client,
)


def test_missing_api_key_raises_without_making_a_request(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(GeminiNotConfiguredError):
        make_gemini_client()


def test_successful_response_returns_text_and_real_usage(monkeypatch):
    class FakeResponse:
        def read(self):
            return json.dumps({
                "candidates": [{"content": {"parts": [{"text": "hello from gemini"}]}}],
                "usageMetadata": {"promptTokenCount": 12, "candidatesTokenCount": 4},
            }).encode()

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(request, timeout=None):
        assert "generativelanguage.googleapis.com" in request.full_url
        return FakeResponse()

    monkeypatch.setattr("council_chamber.seats.gemini_client.urllib.request.urlopen", fake_urlopen)

    client = make_gemini_client(api_key="fake-key-for-test")
    reply, usage = client([Message.create(None, "hi there")])

    assert reply == "hello from gemini"
    assert usage.input_tokens == 12
    assert usage.output_tokens == 4
    assert usage.requests == 1


def test_http_error_raises_gemini_api_error_not_a_fabricated_reply(monkeypatch):
    error_body = json.dumps({"error": {"code": 429, "message": "quota exceeded"}}).encode()

    def fake_urlopen(request, timeout=None):
        raise urllib.error.HTTPError(
            request.full_url, 429, "Too Many Requests", hdrs=None, fp=io.BytesIO(error_body)
        )

    monkeypatch.setattr("council_chamber.seats.gemini_client.urllib.request.urlopen", fake_urlopen)

    client = make_gemini_client(api_key="fake-key-for-test")
    with pytest.raises(GeminiAPIError, match="quota exceeded"):
        client([Message.create(None, "hi there")])


def test_api_key_env_var_is_used_when_not_passed_explicitly(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "env-key")
    captured = {}

    class FakeResponse:
        def read(self):
            return json.dumps({"candidates": [{"content": {"parts": [{"text": "ok"}]}}]}).encode()

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(request, timeout=None):
        captured["url"] = request.full_url
        return FakeResponse()

    monkeypatch.setattr("council_chamber.seats.gemini_client.urllib.request.urlopen", fake_urlopen)

    client = make_gemini_client()
    client([Message.create(None, "hi")])

    assert "key=env-key" in captured["url"]
