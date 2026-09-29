#!/usr/bin/env python3
"""Fetch public scientific source records without inventing or relabelling values.

This is acquisition/provenance only, not a physics interpretation layer.
The returned source document is preserved verbatim under "source_record".
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

REGISTRY = Path(__file__).resolve().parents[1] / "One_Wave_Bench/data/open_data_sources.json"
MAX_BYTES = 25 * 1024 * 1024

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))

def source_by_id(registry: dict, source_id: str) -> dict:
    for source in registry.get("sources", []):
        if source.get("id") == source_id:
            return source
    raise SystemExit(f"unknown source id: {source_id}")

def allowed_hosts(source: dict) -> set[str]:
    hosts = set()
    for key, value in source.items():
        if (key.endswith("_url") or key.endswith("_root") or key.endswith("_docs") or key in {"landing_url", "api_root", "example_endpoint", "tap_root"}):
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                host = urlparse(value).hostname
                if host:
                    hosts.add(host.lower())
    if source.get("id") == "gwosc":
        hosts.add("gwosc.org")
    return hosts

def fetch_json(url: str, hosts: set[str], timeout: int):
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https":
        raise SystemExit("only https source URLs are allowed")
    if host not in hosts:
        raise SystemExit(f"host {host!r} is not declared for this source")
    req = Request(url, headers={"Accept": "application/json", "User-Agent": "One-Wave-Science/real-data-fetch"})
    with urlopen(req, timeout=timeout) as response:
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise SystemExit(f"response exceeds {MAX_BYTES} bytes")
        content_type = response.headers.get("Content-Type", "")
        final_url = response.geturl()
        status = getattr(response, "status", None)
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"response was not JSON: {exc}") from exc
    return raw, doc, {"http_status": status, "content_type": content_type, "final_url": final_url}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_id")
    parser.add_argument("--url", help="Explicit HTTPS JSON endpoint belonging to the registered source")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    registry = load_registry()
    source = source_by_id(registry, args.source_id)
    url = args.url or source.get("example_endpoint")
    if not url:
        raise SystemExit("this source requires an explicit record/API URL or its native client/TAP tool")

    raw, record, transport = fetch_json(url, allowed_hosts(source), max(1, min(args.timeout, 120)))
    envelope = {
        "schema": "one-wave-source-record-v1",
        "source_id": args.source_id,
        "retrieved_at_utc": utc_now(),
        "requested_url": url,
        "transport": transport,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "source_record": record,
        "boundary": "Source record preserved as returned. No One-Wave physical interpretation has been applied.",
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "source_id": args.source_id,
        "output": args.output,
        "sha256": envelope["sha256"],
        "retrieved_at_utc": envelope["retrieved_at_utc"],
        "final_url": transport["final_url"],
    }, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
