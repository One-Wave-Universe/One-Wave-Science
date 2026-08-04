"""Worker ant: one local, file-driven relay round over a saved Council
session -- "the local computer does the actual work" (spec).

This is pure local file I/O and orchestration. It does not call any AI
provider itself and is not a loop: it loads a saved session, asks
exactly the seats you name (one round, via the same Council.ask() gate
everything else uses), and saves the result back to the same file.
Whether that round costs real API tokens depends entirely on whether
the seats you named are wired to a real RemoteAPISeat client
(gemini_client.py, for example) or are MockSeat placeholders -- the ant
itself never makes a network call.

Run it again (by hand, or from your own shell loop with your own delay)
for the next round. This module will never start an autonomous loop on
its own: the spec is explicit that "the system must not allow the AIs
to generate an uncontrolled endless conversation," so every round here
is one deliberate, bounded invocation.
"""

from __future__ import annotations

import sys
from pathlib import Path

from council_chamber.models import Message, SeatKind
from council_chamber.orchestrator import Council
from council_chamber.seats.ai_seat import MockSeat
from council_chamber.storage import load_session, save_session
from council_chamber.workers.patch_worker import PatchWorker

_PLACEHOLDER_REPLY = "(demo seat -- no real provider connected; see RemoteAPISeat in seats/ai_seat.py)"


def _resolve_seat_id(council: Council, token: str) -> str:
    if token in council.chat.seats:
        return token
    for seat in council.chat.seats.values():
        if seat.name.lower() == token.lower():
            return seat.seat_id
    raise ValueError(f"no seat named or id'd {token!r}")


def reattach_placeholder_seats(council: Council) -> int:
    """After loading a session, every AI-kind seat exists as an identity
    in the chat but has no live client behind it (live connections were
    never serialized). Re-attach a MockSeat placeholder for any that
    aren't already registered so they're immediately usable; a caller
    who wants a *real* connection should register a RemoteAPISeat for
    that specific seat_id before calling run_one_round instead."""
    reattached = 0
    for seat in council.chat.seats.values():
        if seat.kind == SeatKind.AI and seat.seat_id not in council.ai_seats:
            council.register_ai_seat(MockSeat(seat, reply=_PLACEHOLDER_REPLY))
            reattached += 1
    return reattached


def run_one_round(
    session_path: str | Path,
    project_dir: str | Path,
    seat_tokens: list[str],
    prompt: str,
    reattach_placeholders: bool = True,
) -> list[Message]:
    """Load `session_path`, ask the named seats (by name or seat_id) one
    round, save the updated session back to the same file, and return
    the replies. Raises if a named seat isn't registered and
    reattach_placeholders is False -- same as Council.ask()."""
    council = load_session(session_path, PatchWorker(project_dir))
    if reattach_placeholders:
        reattach_placeholder_seats(council)

    seat_ids = [_resolve_seat_id(council, tok) for tok in seat_tokens]
    replies = council.ask(seat_ids, prompt)
    save_session(council, session_path)
    return replies


def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) < 4:
        print(
            "usage: python -m council_chamber.worker_ant "
            "<session.json> <project_dir> <seat[,seat...]> <prompt...>"
        )
        raise SystemExit(1)

    session_path, project_dir, seat_arg, *prompt_words = argv
    replies = run_one_round(session_path, project_dir, seat_arg.split(","), " ".join(prompt_words))
    for reply in replies:
        print(f"[{reply.sender_seat_id}] {reply.content}")


if __name__ == "__main__":
    main()
