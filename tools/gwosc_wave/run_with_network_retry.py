#!/usr/bin/env python3
"""Run the GWOSC pipeline with bounded retry for transport failures only.

A timeout/temporary HTTP transport failure may be retried. Parse errors,
assertion failures, numerical errors, source-format drift, and analysis failures
are returned immediately and are never turned into a retry/pass.
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
import time
from typing import List, Optional

NETWORK_MARKERS = (
    "urlopen error timed out",
    "timeouterror",
    "temporarily unavailable",
    "connection reset",
    "connection refused",
    "remote end closed connection",
    "http error 500",
    "http error 502",
    "http error 503",
    "http error 504",
)


def is_transport_failure(stderr: str) -> bool:
    text = stderr.lower()
    return any(marker in text for marker in NETWORK_MARKERS)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--attempts", type=int, default=3)
    p.add_argument("--base-delay", type=float, default=3.0)
    p.add_argument("args", nargs=argparse.REMAINDER)
    ns = p.parse_args(argv)
    if ns.attempts < 1:
        p.error("--attempts must be >= 1")
    if ns.base_delay < 0:
        p.error("--base-delay must be >= 0")
    if ns.args and ns.args[0] == "--":
        ns.args = ns.args[1:]
    if not ns.args:
        p.error("supply gwosc_strain_wave.py arguments after --")
    return ns


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    script = pathlib.Path(__file__).with_name("gwosc_strain_wave.py")
    command = [sys.executable, str(script), *args.args]

    for attempt in range(1, args.attempts + 1):
        proc = subprocess.run(command, text=True, capture_output=True)
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        if proc.returncode == 0:
            if attempt > 1:
                print(f"GWOSC transport recovered on attempt {attempt}", file=sys.stderr)
            return 0

        if not is_transport_failure(proc.stderr):
            print(
                f"GWOSC attempt {attempt} failed for a non-transport reason; not retrying.",
                file=sys.stderr,
            )
            return proc.returncode

        if attempt == args.attempts:
            print(
                f"GWOSC transport failed after {args.attempts} attempts; preserving failure.",
                file=sys.stderr,
            )
            return proc.returncode

        delay = args.base_delay * attempt
        print(
            f"GWOSC transport failure on attempt {attempt}; retrying after {delay:.1f}s.",
            file=sys.stderr,
        )
        time.sleep(delay)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
