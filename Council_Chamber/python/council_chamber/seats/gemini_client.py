"""A real Gemini client for RemoteAPISeat -- calls Google's
generativelanguage.googleapis.com REST API directly (no extra SDK
dependency, just the standard library).

make_gemini_client() returns a callable(context) -> (reply_text,
UsageReport) suitable for RemoteAPISeat(seat, client=...). It reads the
API key from the GEMINI_API_KEY environment variable by default and
raises GeminiNotConfiguredError if none is available, rather than
falling back to a fake reply. A real API error (bad key, quota
exhausted, ...) is raised as GeminiAPIError with the provider's own
message -- never swallowed into a fabricated "success."
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Callable

from council_chamber.models import Message
from council_chamber.usage import UsageReport

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class GeminiNotConfiguredError(RuntimeError):
    pass


class GeminiAPIError(RuntimeError):
    pass


def _context_to_prompt(context: list[Message]) -> str:
    lines = []
    for m in context:
        who = m.sender_seat_id or "user"
        lines.append(f"{who}: {m.content}")
    return "\n".join(lines)


def make_gemini_client(
    model: str = "gemini-2.0-flash", api_key: str | None = None
) -> Callable[[list[Message]], tuple[str, UsageReport]]:
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise GeminiNotConfiguredError(
            "set the GEMINI_API_KEY environment variable (or pass api_key=) to use the real Gemini client"
        )

    def client(context: list[Message]) -> tuple[str, UsageReport]:
        prompt = _context_to_prompt(context)
        body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
        url = GEMINI_API_URL.format(model=model) + f"?key={key}"
        request = urllib.request.Request(
            url, data=body, headers={"Content-Type": "application/json"}, method="POST"
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read())
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode(errors="replace")
            raise GeminiAPIError(f"Gemini API request failed ({exc.code}): {error_body}") from exc

        reply_text = data["candidates"][0]["content"]["parts"][0]["text"]
        usage_meta = data.get("usageMetadata", {})
        usage = UsageReport(
            input_tokens=usage_meta.get("promptTokenCount"),
            output_tokens=usage_meta.get("candidatesTokenCount"),
            requests=1,
        )
        return reply_text, usage

    return client
