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
import time
from pathlib import Path
from typing import Callable

from council_chamber.client_registry import build_ai_seat, discover_and_register_clients
from council_chamber.models import Message, SeatKind
from council_chamber.orchestrator import Council
from council_chamber.storage import load_session, save_session
from council_chamber.workers.patch_worker import PatchWorker

discover_and_register_clients()

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
    never serialized). Re-attach each one that isn't already registered
    -- with a real RemoteAPISeat if a matching client is registered in
    client_registry.py (e.g. GEMINI_API_KEY is set in *this* process),
    or an honestly-labeled MockSeat placeholder otherwise. A caller who
    wants to force a specific connection should register it directly
    before calling run_one_round instead."""
    reattached = 0
    for seat in council.chat.seats.values():
        if seat.kind == SeatKind.AI and seat.seat_id not in council.ai_seats:
            council.register_ai_seat(build_ai_seat(seat, _PLACEHOLDER_REPLY))
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


def run_loop(
    session_path: str | Path,
    project_dir: str | Path,
    seat_tokens: list[str],
    prompt: str,
    delay_seconds: float,
    max_rounds: int,
    reattach_placeholders: bool = True,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> list[list[Message]]:
    """Check in with the named seats every `delay_seconds`, `max_rounds`
    times -- the "ant talks to the AI when it's idle" pattern, without
    becoming an uncontrolled loop: `max_rounds` is a required, explicit
    number you choose, the prompt each round is the same one you gave,
    and Ctrl+C (or just not passing --every) stops it. This is still
    just repeated calls to run_one_round -- same local file, same
    bounded Council.ask() gate, same "no real client means no real
    call" honesty. `sleep_fn` is injectable so tests don't have to
    actually wait."""
    all_replies = []
    for round_index in range(max_rounds):
        replies = run_one_round(session_path, project_dir, seat_tokens, prompt, reattach_placeholders)
        all_replies.append(replies)
        if round_index < max_rounds - 1:
            sleep_fn(delay_seconds)
    return all_replies


def _extract_flag(argv: list[str], flag: str, cast, default):
    if flag in argv:
        idx = argv.index(flag)
        value = cast(argv[idx + 1])
        del argv[idx : idx + 2]
        return value
    return default


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    every = _extract_flag(argv, "--every", float, None)
    times = _extract_flag(argv, "--times", int, 1)

    if len(argv) < 4:
        print(
            "usage: python -m council_chamber.worker_ant "
            "<session.json> <project_dir> <seat[,seat...]> <prompt...> "
            "[--every SECONDS] [--times N]\n"
            "  --every SECONDS  check in again after this many seconds "
            "(omit for a single round)\n"
            "  --times N        how many check-ins to run (default 1; "
            "only meaningful with --every)"
        )
        raise SystemExit(1)

    session_path, project_dir, seat_arg, *prompt_words = argv
    seat_tokens = seat_arg.split(",")
    prompt = " ".join(prompt_words)

    if every is None:
        rounds = [run_one_round(session_path, project_dir, seat_tokens, prompt)]
    else:
        rounds = run_loop(session_path, project_dir, seat_tokens, prompt, delay_seconds=every, max_rounds=times)

    for round_number, replies in enumerate(rounds, start=1):
        if len(rounds) > 1:
            print(f"--- round {round_number}/{len(rounds)} ---")
        for reply in replies:
            print(f"[{reply.sender_seat_id}] {reply.content}")


if __name__ == "__main__":
    main()
