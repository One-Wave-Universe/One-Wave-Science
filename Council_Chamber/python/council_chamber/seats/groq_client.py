"""A real Groq client for RemoteAPISeat -- calls Groq's OpenAI-compatible
REST API directly (no extra SDK dependency, just the standard library).
Groq's free tier requires no credit card, unlike a Google Cloud project
without billing enabled.

make_groq_client() returns a callable(context) -> (reply_text,
UsageReport) suitable for RemoteAPISeat(seat, client=...). It reads the
API key from the GROQ_API_KEY environment variable by default and
raises GroqNotConfiguredError if none is available, rather than falling
back to a fake reply. A real API error (bad key, rate limit, ...) is
raised as GroqAPIError with the provider's own message -- never
swallowed into a fabricated "success."
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Callable

from council_chamber.models import Message
from council_chamber.usage import UsageReport

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


class GroqNotConfiguredError(RuntimeError):
    pass


class GroqAPIError(RuntimeError):
    pass


def _context_to_messages(context: list[Message]) -> list[dict]:
    return [
        {"role": "user" if m.sender_seat_id is None else "assistant", "content": m.content}
        for m in context
    ] or [{"role": "user", "content": "(no context yet)"}]


def make_groq_client(
    model: str = "llama-3.3-70b-versatile", api_key: str | None = None
) -> Callable[[list[Message]], tuple[str, UsageReport]]:
    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        raise GroqNotConfiguredError(
            "set the GROQ_API_KEY environment variable (or pass api_key=) to use the real Groq client -- "
            "get a free key at https://console.groq.com/keys, no billing required"
        )

    def client(context: list[Message]) -> tuple[str, UsageReport]:
        body = json.dumps({"model": model, "messages": _context_to_messages(context)}).encode()
        request = urllib.request.Request(
            GROQ_API_URL, data=body,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read())
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode(errors="replace")
            raise GroqAPIError(f"Groq API request failed ({exc.code}): {error_body}") from exc

        reply_text = data["choices"][0]["message"]["content"]
        usage_meta = data.get("usage", {})
        usage = UsageReport(
            input_tokens=usage_meta.get("prompt_tokens"),
            output_tokens=usage_meta.get("completion_tokens"),
            requests=1,
        )
        return reply_text, usage

    return client


from council_chamber.client_registry import register_client  # noqa: E402

register_client("groq", "Groq", make_groq_client)
