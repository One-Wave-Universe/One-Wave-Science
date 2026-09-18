#!/usr/bin/env python3
"""CLI bridge for AI/human Miniverse room participants."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen

DEFAULT_URL = os.environ.get("MINIVERSE_ROOM_URL", "http://127.0.0.1:8787")


def request(base: str, path: str, payload: dict | None = None) -> dict:
    url = base.rstrip("/") + path
    if payload is None:
        req = Request(url)
    else:
        req = Request(
            url,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
    with urlopen(req, timeout=10) as response:
        return json.load(response)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    sub = parser.add_subparsers(dest="command", required=True)

    join = sub.add_parser("join")
    join.add_argument("agent_id")
    join.add_argument("--name")
    join.add_argument("--role", default="AI")
    join.add_argument("--color", default="#62e6ff")

    say = sub.add_parser("say")
    say.add_argument("agent_id")
    say.add_argument("text")

    move = sub.add_parser("move")
    move.add_argument("agent_id")
    move.add_argument("direction", choices=["A+", "B+", "C+", "A-", "B-", "C-"])

    ping = sub.add_parser("ping")
    ping.add_argument("agent_id")

    bench = sub.add_parser("bench")
    bench.add_argument("agent_id")
    bench.add_argument("bench_id")
    bench.add_argument("action")
    bench.add_argument("summary")

    body = sub.add_parser("body")
    body.add_argument("agent_id")
    body.add_argument("spec", help="JSON body-spec file")

    sub.add_parser("look")

    args = parser.parse_args()
    if args.command == "look":
        result = request(args.url, "/api/state")
    elif args.command == "join":
        result = request(args.url, "/api/join", {
            "agent_id": args.agent_id,
            "name": args.name or args.agent_id,
            "role": args.role,
            "color": args.color,
        })
    elif args.command == "say":
        result = request(args.url, "/api/say", {"agent_id": args.agent_id, "text": args.text})
    elif args.command == "move":
        result = request(args.url, "/api/move", {"agent_id": args.agent_id, "direction": args.direction})
    elif args.command == "ping":
        result = request(args.url, "/api/ping", {"agent_id": args.agent_id})
    elif args.command == "body":
        spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
        result = request(args.url, "/api/body", {"agent_id": args.agent_id, "body": spec})
    else:
        result = request(args.url, "/api/bench", {
            "agent_id": args.agent_id,
            "bench_id": args.bench_id,
            "action": args.action,
            "summary": args.summary,
        })
    json.dump(result, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
