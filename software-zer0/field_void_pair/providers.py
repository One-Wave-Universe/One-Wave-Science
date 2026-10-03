"""AI providers for the Field/Void pair. Keys come from the environment only.

offline     deterministic stand-in, no network (tests, dry runs)
anthropic   Claude via the official `anthropic` SDK (pip install anthropic)
deepseek    OpenAI-compatible chat API, DEEPSEEK_API_KEY
openai      OpenAI-compatible chat API, OPENAI_API_KEY
ollama      local OpenAI-compatible server, no key
gemini      Google generateContent, GEMINI_API_KEY

Keys are never logged, returned to the app, or written to the run ledger.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass


class ProviderError(RuntimeError):
    pass


PRESETS = {
    "offline": {"model": "offline-zer0", "key_env": None},
    "anthropic": {"model": "claude-opus-5-5", "key_env": "ANTHROPIC_API_KEY"},
    "deepseek": {"model": "deepseek-chat", "key_env": "DEEPSEEK_API_KEY",
                 "base_url": "https://api.deepseek.com/v1"},
    "openai": {"model": "gpt-4o-mini", "key_env": "OPENAI_API_KEY",
               "base_url": "https://api.openai.com/v1"},
    "ollama": {"model": "llama3.1", "key_env": None,
               "base_url": "http://127.0.0.1:11434/v1"},
    "gemini": {"model": "gemini-2.5-flash", "key_env": "GEMINI_API_KEY"},
}


def available() -> list[dict]:
    """Provider list for the app. Reports only whether a key is present."""
    rows = []
    for name, p in PRESETS.items():
        env = p["key_env"]
        rows.append({
            "name": name,
            "default_model": p["model"],
            "key_env": env,
            "ready": env is None or bool(os.environ.get(env)),
        })
    return rows


def _post_json(url: str, body: dict, headers: dict, timeout: float = 300.0) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"content-type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:400]
        raise ProviderError(f"HTTP {e.code} from {url.split('?')[0]}: {detail}") from None
    except urllib.error.URLError as e:
        raise ProviderError(f"cannot reach {url.split('?')[0]}: {e.reason}") from None


@dataclass
class Provider:
    name: str
    model: str
    role: str = ""  # "field" or "void", used only by offline

    def complete(self, system: str, user: str) -> str:
        if self.name not in PRESETS:
            raise ProviderError(f"unknown provider {self.name!r}")
        fn = getattr(self, "_" + self.name, None) or self._openai_compat
        return fn(system, user)

    # -- Claude -----------------------------------------------------------
    def _anthropic(self, system: str, user: str) -> str:
        try:
            import anthropic
        except ImportError:
            raise ProviderError("anthropic SDK not installed: pip install anthropic") from None
        client = anthropic.Anthropic()
        try:
            # Server-side fallback reroutes a safety decline instead of stopping.
            resp = client.beta.messages.create(
                model=self.model,
                max_tokens=16000,
                system=system,
                messages=[{"role": "user", "content": user}],
                output_config={"effort": os.environ.get("FVPAIR_EFFORT", "medium")},
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            )
        except anthropic.APIStatusError as e:
            raise ProviderError(f"anthropic HTTP {e.status_code}: {e.message}") from None
        except anthropic.APIConnectionError as e:
            raise ProviderError(f"anthropic connection error: {e}") from None
        if resp.stop_reason == "refusal":
            raise ProviderError("anthropic declined the request (stop_reason=refusal)")
        return "".join(b.text for b in resp.content if b.type == "text")

    # -- OpenAI-compatible: deepseek / openai / ollama --------------------
    def _openai_compat(self, system: str, user: str) -> str:
        preset = PRESETS[self.name]
        base = os.environ.get(f"FVPAIR_{self.name.upper()}_BASE_URL", preset["base_url"])
        headers = {}
        if preset["key_env"]:
            key = os.environ.get(preset["key_env"])
            if not key:
                raise ProviderError(f"{preset['key_env']} is not set")
            headers["authorization"] = "Bearer " + key
        out = _post_json(base.rstrip("/") + "/chat/completions", {
            "model": self.model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
        }, headers)
        try:
            return out["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError):
            raise ProviderError(f"{self.name}: unexpected response shape") from None

    # -- Gemini -----------------------------------------------------------
    def _gemini(self, system: str, user: str) -> str:
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            raise ProviderError("GEMINI_API_KEY is not set")
        url = ("https://generativelanguage.googleapis.com/v1beta/models/"
               f"{self.model}:generateContent")
        out = _post_json(url, {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
        }, {"x-goog-api-key": key})
        try:
            return "".join(p.get("text", "") for p in out["candidates"][0]["content"]["parts"])
        except (KeyError, IndexError, TypeError):
            raise ProviderError("gemini: unexpected response shape") from None

    # -- Offline deterministic stand-in -----------------------------------
    def _offline(self, system: str, user: str) -> str:
        """Not an AI. Exercises the loop with repo-grounded fixed text."""
        focus_part = system.split("--- FOCUS", 1)[-1]
        focus = re.findall(r"^### (\S+/\S+|\S+\.\w+)$", focus_part, flags=re.M)[:3]
        turn = int(m.group(1)) if (m := re.search(r"TURN: (\d+)", user)) else 1
        if self.role == "field":
            cites = ", ".join(f"`{p}`" for p in focus[:2]) or "`AGENTS.md`"
            return (
                f"PROPOSAL (offline turn {turn}): one bounded step toward the goal, "
                f"grounded in {cites} and `simulations/zer0_first_cycle.py`.\n"
                "CITES: " + cites
            )
        grounded = "`" in user and "CITES:" in user
        verdict = "ALLOW" if grounded else "OVERRIDE"
        ref = 0.8 if grounded else -0.8
        goal = max(-1.0, 0.7 - 0.2 * (turn - 1))
        return (f"VERDICT: {verdict}\nREFERENCE: {ref:+.2f}\nGOAL: {goal:+.2f}\n"
                f"NOTE: offline Void, turn {turn}.")
