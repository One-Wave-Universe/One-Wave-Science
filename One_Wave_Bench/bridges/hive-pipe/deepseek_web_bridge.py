#!/usr/bin/env python3
"""DeepSeek free web session -> local relay -> Hive Pipe MCP -> Jetson.

This is intentionally separate from deepseek_bridge.py, which uses the official
DeepSeek API and therefore requires DEEPSEEK_API_KEY.

This client talks only to a local OpenAI-compatible relay that automates an
already-authorized DeepSeek web session. The supported relay installation is
kept outside the One-Wave repository and is never exposed by Hive Pipe.

Relay authentication, in order:
  DEEPSEEK_WEB_API_KEY
  DEEPSEEK_WEB_API_KEY_FILE
  ~/One-Wave-Tools/deepseek-web-relay/.api-key

Relay endpoint:
  DEEPSEEK_WEB_BASE_URL defaults to http://127.0.0.1:3000

Hive Pipe authentication and command boundaries are inherited unchanged from
One_Wave_Bench/bridges/hive-pipe/deepseek_bridge.py.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from deepseek_bridge import (
    DEEPSEEK_TOOLS,
    HivePipeClient,
    MAX_TOOL_ROUNDS,
    _json_post,
    dispatch_tool,
)


DEFAULT_WEB_BASE_URL = "http://127.0.0.1:3000"
DEFAULT_RELAY_HOME = Path.home() / "One-Wave-Tools/deepseek-web-relay"
DEFAULT_WEB_KEY_FILE = DEFAULT_RELAY_HOME / ".api-key"


def _normalize_web_base_url(url: str) -> str:
    value = url.strip().rstrip("/")
    if not value:
        raise ValueError("DeepSeek web relay URL is empty")
    return value


def _load_web_key() -> str:
    direct = os.environ.get("DEEPSEEK_WEB_API_KEY", "").strip()
    if direct:
        return direct
    token_file = Path(
        os.environ.get("DEEPSEEK_WEB_API_KEY_FILE", str(DEFAULT_WEB_KEY_FILE))
    ).expanduser()
    try:
        value = token_file.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise RuntimeError(
            "Local DeepSeek web relay key not found. Run "
            "`bash One_Wave_Bench/bridges/scripts/bootstrap_deepseek_web_relay.sh` on the Jetson first, "
            "or set DEEPSEEK_WEB_API_KEY/DEEPSEEK_WEB_API_KEY_FILE. "
            "This is the relay's local key, not a DeepSeek API key."
        ) from exc
    if not value:
        raise RuntimeError(f"DeepSeek web relay key file is empty: {token_file}")
    return value


def _json_get(url: str, timeout: int = 15) -> dict[str, Any]:
    request = Request(url, headers={"Accept": "application/json"}, method="GET")
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Unable to reach {url}: {exc.reason}") from exc
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Non-JSON response from {url}: {raw[:500]}") from exc
    if not isinstance(parsed, dict):
        raise RuntimeError(f"Expected JSON object from {url}")
    return parsed


def relay_health(base_url: str | None = None) -> dict[str, Any]:
    base = _normalize_web_base_url(
        base_url or os.environ.get("DEEPSEEK_WEB_BASE_URL", DEFAULT_WEB_BASE_URL)
    )
    return _json_get(f"{base}/health")


class DeepSeekWebAgent:
    """Drive a DeepSeek web session while executing tool calls through Hive Pipe."""

    def __init__(
        self,
        mcp: HivePipeClient,
        *,
        web_api_key: str | None = None,
        base_url: str | None = None,
        deepthink: bool = True,
        web_search: bool = False,
        expert_mode: bool = False,
        post_json: Callable[[str, dict[str, Any], dict[str, str], int], dict[str, Any]] = _json_post,
    ) -> None:
        self.mcp = mcp
        self.web_api_key = (web_api_key or _load_web_key()).strip()
        if not self.web_api_key:
            raise RuntimeError("DeepSeek web relay key is empty")
        self.base_url = _normalize_web_base_url(
            base_url or os.environ.get("DEEPSEEK_WEB_BASE_URL", DEFAULT_WEB_BASE_URL)
        )
        self.deepthink = deepthink
        self.web_search = web_search
        self.expert_mode = expert_mode
        self._post_json = post_json

    def _chat(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "messages": messages,
            "tools": DEEPSEEK_TOOLS,
            "extra_body": {
                "deepthink": self.deepthink,
                "web_search": self.web_search,
                "expert_mode": self.expert_mode,
            },
        }
        response = self._post_json(
            f"{self.base_url}/v1/chat/completions",
            payload,
            {"Authorization": f"Bearer {self.web_api_key}"},
            330,
        )
        choices = response.get("choices")
        if not isinstance(choices, list) or not choices:
            raise RuntimeError("DeepSeek web relay response is missing choices")
        message = choices[0].get("message")
        if not isinstance(message, dict):
            raise RuntimeError("DeepSeek web relay response is missing assistant message")
        return message

    def run(self, prompt: str, *, max_tool_rounds: int = MAX_TOOL_ROUNDS) -> str:
        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are operating the One-Wave Jetson through explicit tools. "
                    "Reference the repository before interpretation. Use the smallest concrete "
                    "command, inspect returned stdout/stderr/exit_code, and never claim a command "
                    "ran unless a tool result confirms it. Do not redesign working access "
                    "infrastructure unless the user explicitly asks for that."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        for _ in range(max_tool_rounds):
            message = self._chat(messages)
            assistant_message: dict[str, Any] = {
                "role": "assistant",
                "content": message.get("content") or "",
            }
            if message.get("tool_calls") is not None:
                assistant_message["tool_calls"] = message.get("tool_calls")
            messages.append(assistant_message)

            tool_calls = message.get("tool_calls") or []
            if not tool_calls:
                return assistant_message["content"]

            for tool_call in tool_calls:
                if not isinstance(tool_call, dict):
                    raise RuntimeError("DeepSeek web relay returned a malformed tool call")
                call_id = tool_call.get("id")
                function = tool_call.get("function")
                if not isinstance(call_id, str) or not isinstance(function, dict):
                    raise RuntimeError("DeepSeek web relay returned malformed function metadata")
                name = function.get("name")
                raw_arguments = function.get("arguments", "{}")
                if not isinstance(name, str):
                    raise RuntimeError("DeepSeek web relay returned a tool without a function name")
                try:
                    if isinstance(raw_arguments, str):
                        arguments = json.loads(raw_arguments or "{}")
                    elif isinstance(raw_arguments, dict):
                        arguments = raw_arguments
                    else:
                        raise ValueError("tool arguments must be a JSON string or object")
                    output = dispatch_tool(self.mcp, name, arguments)
                except Exception as exc:
                    output = {"ok": False, "bridge_error": str(exc)}

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call_id,
                        "content": json.dumps(output, sort_keys=True),
                    }
                )

        raise RuntimeError(
            f"DeepSeek web relay exceeded {max_tool_rounds} tool-call rounds"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run a logged-in DeepSeek free web session as a client of the existing "
            "One-Wave Hive Pipe Jetson terminal."
        )
    )
    parser.add_argument("prompt", nargs="*", help="Task for DeepSeek; reads stdin when omitted.")
    parser.add_argument("--no-deepthink", action="store_true")
    parser.add_argument("--web-search", action="store_true")
    parser.add_argument("--expert-mode", action="store_true")
    parser.add_argument("--max-tool-rounds", type=int, default=MAX_TOOL_ROUNDS)
    parser.add_argument(
        "--relay-health",
        action="store_true",
        help="Check the local browser relay without calling DeepSeek chat.",
    )
    parser.add_argument(
        "--mcp-smoke",
        action="store_true",
        help="Test Hive Pipe terminal_pwd without calling DeepSeek chat.",
    )
    args = parser.parse_args(argv)

    did_smoke = False
    if args.relay_health:
        print(json.dumps({"relay": relay_health()}, indent=2, sort_keys=True))
        did_smoke = True

    mcp = HivePipeClient()
    if args.mcp_smoke:
        print(json.dumps({"hive_pipe": mcp.call("terminal_pwd", {})}, indent=2, sort_keys=True))
        did_smoke = True

    prompt = " ".join(args.prompt).strip()
    if not prompt and did_smoke:
        return 0
    if not prompt:
        if sys.stdin.isatty():
            parser.error("provide a prompt or pipe one on stdin")
        prompt = sys.stdin.read().strip()
    if not prompt:
        parser.error("prompt is empty")

    agent = DeepSeekWebAgent(
        mcp,
        deepthink=not args.no_deepthink,
        web_search=args.web_search,
        expert_mode=args.expert_mode,
    )
    print(agent.run(prompt, max_tool_rounds=max(1, args.max_tool_rounds)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
