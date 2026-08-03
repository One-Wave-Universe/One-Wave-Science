"""Per-seat resource/usage reporting -- the spec's "the system must not
invent token counts when they are not reported."

UsageReport is deliberately all-optional: a seat reports whatever its
connection actually exposes (tokens, price, request count, context-window
use, ...) and leaves the rest None rather than have the system guess. A
seat with no real accounting (MockSeat, or a RemoteAPISeat whose client
didn't report anything) uses UsageReport.unavailable() so that's visible
in the chamber as a genuine unknown, never a fabricated zero.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class UsageReport:
    input_tokens: int | None = None
    output_tokens: int | None = None
    requests: int | None = None
    estimated_price_usd: float | None = None
    context_window_used: int | None = None
    note: str | None = None  # e.g. "usage unavailable", "subscription access", "local CPU/GPU"

    @classmethod
    def unavailable(cls, note: str = "usage unavailable") -> "UsageReport":
        return cls(note=note)

    def to_dict(self) -> dict:
        return asdict(self)


def summarize(reports: list[UsageReport]) -> dict:
    """Sum whichever numeric fields were actually reported; never treat a
    missing value as zero. `reports_without_data` counts reports that
    contributed neither input nor output tokens, so a caller can tell
    "zero tokens used" apart from "usage wasn't reported"."""
    known_input = [r.input_tokens for r in reports if r.input_tokens is not None]
    known_output = [r.output_tokens for r in reports if r.output_tokens is not None]
    known_price = [r.estimated_price_usd for r in reports if r.estimated_price_usd is not None]
    return {
        "input_tokens": sum(known_input) if known_input else None,
        "output_tokens": sum(known_output) if known_output else None,
        "estimated_price_usd": sum(known_price) if known_price else None,
        "total_requests": len(reports),
        "reports_without_data": sum(
            1 for r in reports if r.input_tokens is None and r.output_tokens is None
        ),
    }
