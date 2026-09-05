"""Connect two OpenAI-compatible models to the shared One-Wave coding loop.

Designed for local servers such as Ollama/LM Studio that expose
``/v1/chat/completions``. Dream performs bounded repo work. Administrator sees
compressed measurements and returns oversight/override guidance. The host,
not either model, owns state and tools.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
from urllib import request

from .shared_loop_mvp import AdminDecision, LoopStep, M4Host, SharedState, ToolAction


class OpenAICompatibleWorker:
    def __init__(self, base_url: str, model: str, api_key: str = "local"):
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.model = model
        self.api_key = api_key

    def ask(self, system: str, payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
        body = {
            "model": self.model,
            "temperature": 0.1,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(payload, indent=2)},
            ],
        }
        req = request.Request(
            self.url,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        with request.urlopen(req, timeout=300) as response:
            data = json.loads(response.read().decode("utf-8"))
        text = data["choices"][0]["message"]["content"]
        usage = data.get("usage") or {}
        tokens = int(usage.get("total_tokens") or 0)
        return _extract_json(text), tokens


def _extract_json(text: str) -> dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise ValueError(f"model did not return JSON: {text[:300]!r}")
    return json.loads(text[start : end + 1])


DREAM_SYSTEM = """You are the Dream coding role inside a deterministic One-Wave host.
The root reference is immutable. You do not declare success and you do not
change the target. During BUILD, inspect only what is needed, then make one
bounded code change. Return JSON only:
{
  "action": {
    "kind": "read" | "search" | "write",
    "path": "relative/path",
    "query": "search text",
    "content": "complete UTF-8 file contents for write",
    "note": "short reason"
  }
}
Use read/search until you have enough evidence. Use write for one concrete
change. Never invent a different target because it is easier.
"""


ADMIN_SYSTEM = """You are the Administrator role inside a deterministic One-Wave host.
You share one memory/reference with Dream. You do not replace the target and
you do not perform normal coding. Read the measured consequence relative to
the immutable reference and return JSON only:
{
  "direction": "-" | "0" | "+",
  "relation": "short four-way/relational description",
  "dimensional_view": "the compact view the next loop stage needs",
  "oversight": "short oversight note",
  "override": true | false,
  "override_instruction": "bounded correction for Dream, or empty"
}
Override only when the measured result is drifting, stuck, or breaks a required
relationship. Keep the packet small.
"""


class LocalPairRunner:
    def __init__(
        self,
        host: M4Host,
        dream: OpenAICompatibleWorker,
        admin: OpenAICompatibleWorker,
        check_command: str,
        max_inspections: int = 8,
    ):
        self.host = host
        self.dream = dream
        self.admin = admin
        self.check_command = check_command
        self.max_inspections = max_inspections

    def _build(self) -> None:
        last_tool_result = ""
        for _ in range(self.max_inspections + 1):
            packet = self.host.state.dream_view()
            packet["last_tool_result"] = last_tool_result[-5000:]
            response, tokens = self.dream.ask(DREAM_SYSTEM, packet)
            self.host.add_token_use("local", tokens)
            action_data = response.get("action") or {}
            action = ToolAction(
                kind=str(action_data.get("kind", "")),
                path=str(action_data.get("path", "")),
                query=str(action_data.get("query", "")),
                content=str(action_data.get("content", "")),
                note=str(action_data.get("note", "")),
            )
            if action.kind not in {"read", "search", "write"}:
                raise ValueError(f"Dream returned unsupported action {action.kind!r}")
            result = self.host.dream_tool(action)
            last_tool_result = result.output
            if action.kind == "write":
                return
        raise RuntimeError("Dream exhausted inspection budget without making a bounded change")

    def _measure(self) -> str:
        # Measurement is a host-owned operation; the AI cannot substitute its opinion.
        result = self.host.tools.execute(ToolAction(kind="command", command=self.check_command))
        return result.output

    def _admin(self, measurement: str) -> AdminDecision:
        packet = self.host.state.admin_view()
        packet["measured_consequence"] = measurement[-7000:]
        response, tokens = self.admin.ask(ADMIN_SYSTEM, packet)
        self.host.add_token_use("oversight", tokens)
        return AdminDecision(
            direction=str(response.get("direction", "0")),
            relation=str(response.get("relation", "")),
            dimensional_view=str(response.get("dimensional_view", "")),
            oversight=str(response.get("oversight", "")),
            override=bool(response.get("override", False)),
            override_instruction=str(response.get("override_instruction", "")),
        )

    def run_one_loop(self) -> SharedState:
        state = self.host.state
        if state.step is LoopStep.BEGIN:
            self.host.begin("New coding cycle opened against the immutable root reference.")

        if state.step is LoopStep.BUILD_1:
            self._build()

        if state.step is LoopStep.HOLD:
            measurement = self._measure()
            self.host.hold(measurement, self._admin(measurement))

        if state.step is LoopStep.BUILD_2:
            self._build()

        if state.step is LoopStep.BREAK:
            measurement = self._measure()
            self.host.break_step(measurement, self._admin(measurement))

        if state.step is LoopStep.LOOP:
            compressed = (
                f"cycle {state.cycle}: direction={state.direction}; "
                f"relation={state.quadratic_relation}; view={state.dimensional_view}; "
                f"last_measurement={(state.measurements[-1] if state.measurements else '')[-1200:]}"
            )
            self.host.complete_loop(compressed, unresolved=state.unresolved[-6:])

        return self.host.state


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one shared Dream/Admin coding loop")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--reference", required=True)
    parser.add_argument("--dream-url", default="http://127.0.0.1:11434/v1")
    parser.add_argument("--dream-model", required=True)
    parser.add_argument("--admin-url", default="http://127.0.0.1:11434/v1")
    parser.add_argument("--admin-model", required=True)
    parser.add_argument("--check", required=True, help="Host-owned measurement/test command")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    state_path = workspace / ".onewave" / "shared_state.json"
    if state_path.exists():
        state = SharedState.load(state_path)
        if state.root_reference != args.reference:
            raise SystemExit("Existing shared state has a different immutable reference")
    else:
        state = SharedState(root_reference=args.reference)

    host = M4Host(state, workspace, state_path)
    runner = LocalPairRunner(
        host,
        OpenAICompatibleWorker(args.dream_url, args.dream_model),
        OpenAICompatibleWorker(args.admin_url, args.admin_model),
        args.check,
    )
    final_state = runner.run_one_loop()
    print(json.dumps(final_state.dream_view(), indent=2))


if __name__ == "__main__":
    main()
