#!/usr/bin/env python3
"""Gemini free web session -> Dell relay -> Hive Pipe MCP -> Jetson."""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any
from urllib.request import Request, urlopen

from deepseek_bridge import DEEPSEEK_TOOLS, HivePipeClient, MAX_TOOL_ROUNDS, dispatch_tool

DEFAULT_BASE = "http://192.168.55.100:3001"

def post_json(url: str, payload: dict[str, Any], timeout: int = 330) -> dict[str, Any]:
    raw = json.dumps(payload).encode("utf-8")
    req = Request(
        url,
        data=raw,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer usb-local",
        },
        method="POST",
    )
    with urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read().decode("utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("Gemini relay returned non-object JSON")
    return data

def get_json(url: str, timeout: int = 15) -> dict[str, Any]:
    with urlopen(url, timeout=timeout) as r:
        data = json.loads(r.read().decode("utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("Gemini relay returned non-object JSON")
    return data

def textual_tool_calls(message: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize Gemini web replies that emit a tool call as JSON text."""
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        return []
    try:
        obj = json.loads(content)
    except json.JSONDecodeError:
        return []
    if not isinstance(obj, dict):
        return []
    call = obj.get("tool_call")
    if not isinstance(call, dict):
        return []
    name = call.get("name")
    arguments = call.get("arguments", {})
    if not isinstance(name, str) or not name:
        return []
    if not isinstance(arguments, (dict, str)):
        return []
    return [{
        "id": "gemini-text-tool-1",
        "function": {
            "name": name,
            "arguments": arguments if isinstance(arguments, str) else json.dumps(arguments),
        },
    }]


class GeminiWebAgent:
    def __init__(self, mcp: HivePipeClient, base_url: str | None = None) -> None:
        self.mcp = mcp
        self.base_url = (base_url or os.environ.get("GEMINI_WEB_BASE_URL", DEFAULT_BASE)).rstrip("/")

    def chat(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        payload = {"messages": messages, "tools": DEEPSEEK_TOOLS}
        response = post_json(f"{self.base_url}/v1/chat/completions", payload)
        choices = response.get("choices")
        if not isinstance(choices, list) or not choices:
            raise RuntimeError("Gemini relay response missing choices")
        message = choices[0].get("message")
        if not isinstance(message, dict):
            raise RuntimeError("Gemini relay response missing message")
        return message

    def run(self, prompt: str, max_tool_rounds: int = MAX_TOOL_ROUNDS) -> str:
        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are Gemini Brain Buddy operating through bounded One-Wave tools. "
                    "Reference the canonical repo before interpretation. Never claim a tool ran "
                    "without its returned receipt. Keep external research distinct from repo metadata."
                ),
            },
            {"role": "user", "content": prompt},
        ]
        for _ in range(max_tool_rounds):
            message = self.chat(messages)
            assistant = {
                "role": "assistant",
                "content": message.get("content") or "",
            }
            if message.get("tool_calls") is not None:
                assistant["tool_calls"] = message["tool_calls"]
            messages.append(assistant)
            calls = message.get("tool_calls") or textual_tool_calls(message)
            if calls and message.get("tool_calls") is None:
                assistant["tool_calls"] = calls
                messages[-1] = assistant
            if not calls:
                return assistant["content"]
            for call in calls:
                fn = call.get("function") if isinstance(call, dict) else None
                call_id = call.get("id") if isinstance(call, dict) else None
                if not isinstance(fn, dict) or not isinstance(call_id, str):
                    raise RuntimeError("Malformed Gemini relay tool call")
                name = fn.get("name")
                raw_args = fn.get("arguments", "{}")
                if isinstance(raw_args, str):
                    args = json.loads(raw_args or "{}")
                elif isinstance(raw_args, dict):
                    args = raw_args
                else:
                    raise RuntimeError("Malformed Gemini tool arguments")
                try:
                    result = dispatch_tool(self.mcp, name, args)
                except Exception as exc:
                    result = {"ok": False, "bridge_error": str(exc)}
                messages.append({
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": json.dumps(result, sort_keys=True),
                })
        raise RuntimeError(f"Gemini web relay exceeded {max_tool_rounds} tool rounds")

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", nargs="*")
    ap.add_argument("--max-tool-rounds", type=int, default=MAX_TOOL_ROUNDS)
    ap.add_argument("--relay-health", action="store_true")
    ap.add_argument("--mcp-smoke", action="store_true")
    args = ap.parse_args(argv)

    base = os.environ.get("GEMINI_WEB_BASE_URL", DEFAULT_BASE).rstrip("/")
    did_smoke = False
    if args.relay_health:
        print(json.dumps({"relay": get_json(base + "/health")}, indent=2, sort_keys=True))
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
            ap.error("provide prompt")
        prompt = sys.stdin.read().strip()
    if not prompt:
        ap.error("prompt is empty")

    print(GeminiWebAgent(mcp, base).run(prompt, max(1, args.max_tool_rounds)))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())