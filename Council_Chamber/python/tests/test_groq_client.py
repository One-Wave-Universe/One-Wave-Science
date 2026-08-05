import io
import json
import urllib.error

import pytest

from council_chamber.models import Message
from council_chamber.seats.groq_client import (
    GroqAPIError,
    GroqNotConfiguredError,
    make_groq_client,
)


def test_missing_api_key_raises_without_making_a_request(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with pytest.raises(GroqNotConfiguredError):
        make_groq_client()


def test_successful_response_returns_text_and_real_usage(monkeypatch):
    class FakeResponse:
        def read(self):
            return json.dumps({
                "choices": [{"message": {"content": "hello from groq"}}],
                "usage": {"prompt_tokens": 9, "completion_tokens": 3},
            }).encode()

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(request, timeout=None):
        assert request.full_url == "https://api.groq.com/openai/v1/chat/completions"
        assert request.get_header("Authorization") == "Bearer fake-key-for-test"
        return FakeResponse()

    monkeypatch.setattr("council_chamber.seats.groq_client.urllib.request.urlopen", fake_urlopen)

    client = make_groq_client(api_key="fake-key-for-test")
    reply, usage = client([Message.create(None, "hi there")])

    assert reply == "hello from groq"
    assert usage.input_tokens == 9
    assert usage.output_tokens == 3
    assert usage.requests == 1


def test_http_error_raises_groq_api_error_not_a_fabricated_reply(monkeypatch):
    error_body = json.dumps({"error": {"message": "invalid api key"}}).encode()

    def fake_urlopen(request, timeout=None):
        raise urllib.error.HTTPError(
            request.full_url, 401, "Unauthorized", hdrs=None, fp=io.BytesIO(error_body)
        )

    monkeypatch.setattr("council_chamber.seats.groq_client.urllib.request.urlopen", fake_urlopen)

    client = make_groq_client(api_key="fake-key-for-test")
    with pytest.raises(GroqAPIError, match="invalid api key"):
        client([Message.create(None, "hi there")])


def test_api_key_env_var_is_used_when_not_passed_explicitly(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "env-key")
    captured = {}

    class FakeResponse:
        def read(self):
            return json.dumps({"choices": [{"message": {"content": "ok"}}]}).encode()

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(request, timeout=None):
        captured["auth"] = request.get_header("Authorization")
        return FakeResponse()

    monkeypatch.setattr("council_chamber.seats.groq_client.urllib.request.urlopen", fake_urlopen)

    client = make_groq_client()
    client([Message.create(None, "hi")])

    assert captured["auth"] == "Bearer env-key"


def test_empty_context_still_sends_a_valid_message(monkeypatch):
    captured = {}

    class FakeResponse:
        def read(self):
            return json.dumps({"choices": [{"message": {"content": "ok"}}]}).encode()

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(request, timeout=None):
        captured["body"] = json.loads(request.data)
        return FakeResponse()

    monkeypatch.setattr("council_chamber.seats.groq_client.urllib.request.urlopen", fake_urlopen)

    client = make_groq_client(api_key="fake-key-for-test")
    client([])

    assert captured["body"]["messages"] == [{"role": "user", "content": "(no context yet)"}]
