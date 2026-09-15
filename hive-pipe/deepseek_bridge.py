#!/usr/bin/env python3
"""DeepSeek function tools -> Hive Pipe MCP -> Jetson terminal.

This is the external harness needed when DeepSeek is called through its API.
It does not require DeepSeek's hosted chat product to expose MCP directly.

Required environment:
  DEEPSEEK_API_KEY

Hive Pipe authentication, in order:
  HIVE_PIPE_TOKEN
  HIVE_PIPE_TOKEN_FILE
  ~/.config/hive-pipe/tokens/deepseek.token

Hive Pipe endpoint:
  HIVE_PIPE_MCP_URL defaults to http://127.0.0.1:8765/mcp.
  For an off-Jetson client, set it to the authenticated tunnel URL ending /mcp.
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


DEFAULT_DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_DEEPSEEK_MODEL = "deepseek-v4-pro"
DEFAULT_MCP_URL = "http://127.0.0.1:8765/mcp"
DEFAULT_TOKEN_FILE = Path.home() / ".config/hive-pipe/tokens/deepseek.token"
MAX_TOOL_ROUNDS = 24

DEEPSEEK_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "jetson_pwd",
            "description": "Return the Jetson working directory available through Hive Pipe.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cwd": {
                        "type": "string",
                        "description": "Optional authorized Jetson working directory.",
                    }
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "jetson_which",
            "description": "Locate an executable on the Jetson PATH through Hive Pipe.",
            "parameters": {
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "jetson_run",
            "description": (
                "Run a structured argv command on the Jetson through the canonical Hive Pipe "
                "terminal parser. Server-side access boundaries remain authoritative."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "argv": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                    },
                    "cwd": {"type": "string"},
                    "timeout": {"type": "integer", "minimum": 1, "maximum": 300},
                },
                "required": ["argv"],
                "additionalProperties": False,
            },
        },
    },
]


def _json_post(
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str],
    timeout: int,
) -> dict[str, Any]:
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
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


def _load_hive_token() -> str:
    direct = os.environ.get("HIVE_PIPE_TOKEN", "").strip()
    if direct:
        return direct
    token_file = Path(
        os.environ.get("HIVE_PIPE_TOKEN_FILE", str(DEFAULT_TOKEN_FILE))
    ).expanduser()
    try:
        token = token_file.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise RuntimeError(
            "Hive Pipe token not found. Run `bash hive-pipe/create_client_token.sh deepseek` "
            "on the Jetson, or set HIVE_PIPE_TOKEN/HIVE_PIPE_TOKEN_FILE."
        ) from exc
    if not token:
        raise RuntimeError(f"Hive Pipe token file is empty: {token_file}")
    return token


def _normalize_mcp_url(url: str) -> str:
    value = url.strip().rstrip("/")
    if not value:
        raise ValueError("Hive Pipe MCP URL is empty")
    if not value.endswith("/mcp"):
        value += "/mcp"
    return value


class HivePipeClient:
    def __init__(
        self,
        *,
        url: str | None = None,
        token: str | None = None,
        post_json: Callable[[str, dict[str, Any], dict[str, str], int], dict[str, Any]] = _json_post,
    ) -> None:
        self.url = _normalize_mcp_url(
            url or os.environ.get("HIVE_PIPE_MCP_URL", DEFAULT_MCP_URL)
        )
        self.token = token or _load_hive_token()
        self._post_json = post_json
        self._request_id = 0

    def call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name not in {"terminal_pwd", "terminal_which", "terminal_run"}:
            raise ValueError(f"DeepSeek bridge refuses unknown Hive Pipe tool: {name}")
        self._request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        }
        envelope = self._post_json(
            self.url,
            payload,
            {"Authorization": f"Bearer {self.token}"},
            330,
        )
        if "error" in envelope:
            raise RuntimeError(
                f"Hive Pipe MCP error: {json.dumps(envelope['error'], sort_keys=True)}"
            )
        result = envelope.get("result")
        if not isinstance(result, dict):
            raise RuntimeError("Hive Pipe MCP response is missing result")
        structured = result.get("structuredContent")
        if not isinstance(structured, dict):
            raise RuntimeError("Hive Pipe MCP response is missing structuredContent")
        return structured


def _validate_tool_call(name: str, arguments: Any) -> tuple[str, dict[str, Any]]:
    if not isinstance(arguments, dict):
        raise ValueError("tool arguments must be a JSON object")

    if name == "jetson_pwd":
        if set(arguments) - {"cwd"}:
            raise ValueError("jetson_pwd accepts only cwd")
        if "cwd" in arguments and not isinstance(arguments["cwd"], str):
            raise ValueError("jetson_pwd cwd must be a string")
        return "terminal_pwd", arguments

    if name == "jetson_which":
        if set(arguments) != {"name"} or not isinstance(arguments.get("name"), str):
            raise ValueError("jetson_which requires exactly one string field: name")
        return "terminal_which", arguments

    if name == "jetson_run":
        if set(arguments) - {"argv", "cwd", "timeout"}:
            raise ValueError("jetson_run received unknown fields")
        argv = arguments.get("argv")
        if not isinstance(argv, list) or not argv or not all(
            isinstance(item, str) and item for item in argv
        ):
            raise ValueError("jetson_run argv must be a non-empty string array")
        if "cwd" in arguments and not isinstance(arguments["cwd"], str):
            raise ValueError("jetson_run cwd must be a string")
        if "timeout" in arguments:
            timeout = arguments["timeout"]
            if (
                not isinstance(timeout, int)
                or isinstance(timeout, bool)
                or not 1 <= timeout <= 300
            ):
                raise ValueError("jetson_run timeout must be an integer from 1 to 300")
        return "terminal_run", arguments

    raise ValueError(f"unknown DeepSeek tool: {name}")


def dispatch_tool(mcp: HivePipeClient, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    mcp_name, mcp_arguments = _validate_tool_call(name, arguments)
    return mcp.call(mcp_name, mcp_arguments)


class DeepSeekAgent:
    def __init__(
        self,
        mcp: HivePipeClient,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        thinking: bool = True,
        reasoning_effort: str = "high",
        post_json: Callable[[str, dict[str, Any], dict[str, str], int], dict[str, Any]] = _json_post,
    ) -> None:
        self.mcp = mcp
        self.api_key = (api_key or os.environ.get("DEEPSEEK_API_KEY", "")).strip()
        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY is required")
        self.base_url = (
            base_url or os.environ.get("DEEPSEEK_BASE_URL", DEFAULT_DEEPSEEK_BASE_URL)
        ).rstrip("/")
        self.model = model or os.environ.get("DEEPSEEK_MODEL", DEFAULT_DEEPSEEK_MODEL)
        self.thinking = thinking
        self.reasoning_effort = reasoning_effort
        self._post_json = post_json

    def _chat(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "tools": DEEPSEEK_TOOLS,
            "thinking": {"type": "enabled" if self.thinking else "disabled"},
        }
        if self.thinking:
            payload["reasoning_effort"] = self.reasoning_effort
        response = self._post_json(
            f"{self.base_url}/chat/completions",
            payload,
            {"Authorization": f"Bearer {self.api_key}"},
            180,
        )
        choices = response.get("choices")
        if not isinstance(choices, list) or not choices:
            raise RuntimeError("DeepSeek response is missing choices")
        message = choices[0].get("message")
        if not isinstance(message, dict):
            raise RuntimeError("DeepSeek response is missing assistant message")
        return message

    def run(self, prompt: str, *, max_tool_rounds: int = MAX_TOOL_ROUNDS) -> str:
        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are operating the One-Wave Jetson through explicit tools. "
                    "Reference the repository before interpretation. Use the smallest concrete "
                    "command, inspect returned stdout/stderr/exit_code, and never claim a command "
                    "ran unless a tool result confirms it."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        for _ in range(max_tool_rounds):
            message = self._chat(messages)

            # DeepSeek thinking-mode tool calls require reasoning_content to be
            # replayed on subsequent requests. Keep the assistant turn intact.
            assistant_message: dict[str, Any] = {
                "role": "assistant",
                "content": message.get("content") or "",
            }
            if "reasoning_content" in message:
                assistant_message["reasoning_content"] = message.get("reasoning_content") or ""
            if message.get("tool_calls") is not None:
                assistant_message["tool_calls"] = message.get("tool_calls")
            messages.append(assistant_message)

            tool_calls = message.get("tool_calls") or []
            if not tool_calls:
                return assistant_message["content"]

            for tool_call in tool_calls:
                if not isinstance(tool_call, dict):
                    raise RuntimeError("DeepSeek returned a malformed tool call")
                call_id = tool_call.get("id")
                function = tool_call.get("function")
                if not isinstance(call_id, str) or not isinstance(function, dict):
                    raise RuntimeError("DeepSeek returned malformed function metadata")
                name = function.get("name")
                raw_arguments = function.get("arguments", "{}")
                if not isinstance(name, str) or not isinstance(raw_arguments, str):
                    raise RuntimeError("DeepSeek returned malformed function metadata")
                try:
                    arguments = json.loads(raw_arguments or "{}")
                    output = dispatch_tool(self.mcp, name, arguments)
                except Exception as exc:
                    # Send the failure back to the model; do not hide or reinterpret it.
                    output = {"ok": False, "bridge_error": str(exc)}

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call_id,
                        "content": json.dumps(output, sort_keys=True),
                    }
                )

        raise RuntimeError(f"DeepSeek exceeded {max_tool_rounds} tool-call rounds")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run DeepSeek as a client of the One-Wave Hive Pipe Jetson terminal."
    )
    parser.add_argument("prompt", nargs="*", help="Task for DeepSeek; reads stdin when omitted.")
    parser.add_argument("--model", default=None, help="DeepSeek model override.")
    parser.add_argument("--no-thinking", action="store_true", help="Disable thinking mode.")
    parser.add_argument(
        "--reasoning-effort",
        choices=("low", "high", "max"),
        default="high",
    )
    parser.add_argument("--max-tool-rounds", type=int, default=MAX_TOOL_ROUNDS)
    parser.add_argument(
        "--mcp-smoke",
        action="store_true",
        help="Test Hive Pipe terminal_pwd without calling DeepSeek.",
    )
    args = parser.parse_args(argv)

    mcp = HivePipeClient()
    if args.mcp_smoke:
        print(json.dumps(mcp.call("terminal_pwd", {}), indent=2, sort_keys=True))
        return 0

    prompt = " ".join(args.prompt).strip()
    if not prompt:
        if sys.stdin.isatty():
            parser.error("provide a prompt or pipe one on stdin")
        prompt = sys.stdin.read().strip()
    if not prompt:
        parser.error("prompt is empty")

    agent = DeepSeekAgent(
        mcp,
        model=args.model,
        thinking=not args.no_thinking,
        reasoning_effort=args.reasoning_effort,
    )
    print(agent.run(prompt, max_tool_rounds=max(1, args.max_tool_rounds)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
