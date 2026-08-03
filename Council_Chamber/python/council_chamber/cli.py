"""End-to-end demo reproducing the spec's own example workflow:

    Add disconnect support to the AI seats.
    ChatGPT examines the requirements and proposes the behavior.
    Codex inspects the relevant local files and proposes a patch.
    The user approves it.
    The local Patch Worker applies the change.
    The local Test Worker runs the tests.
    One test fails and posts the exact error into the council chat.
    ChatGPT explains the likely problem.
    Codex proposes a smaller repair.
    The user approves it.
    The Patch Worker applies it, and the Test Worker confirms that all
    tests pass.

ChatGPT and Codex are MockSeat instances here (no API keys in this
environment -- see seats/ai_seat.py) but every local operation --
writing the file, running pytest, reporting the exact failure -- is
real, against a real temporary project directory.

Usage: python -m council_chamber.cli
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

from council_chamber.models import CouncilChat, Seat, SeatKind
from council_chamber.seats.ai_seat import MockSeat
from council_chamber.workers.patch_worker import PatchWorker
from council_chamber.workers.test_worker import TestWorker
from council_chamber.orchestrator import Council

STARTER_SEATS_PY = '''\
class AISeatRegistry:
    def __init__(self):
        self.seats = {}

    def add_seat(self, seat_id, name):
        self.seats[seat_id] = {"name": name, "connected": True}
'''

STARTER_TEST_PY = '''\
from seats import AISeatRegistry


def test_add_seat():
    registry = AISeatRegistry()
    registry.add_seat("s1", "Claude")
    assert registry.seats["s1"]["connected"] is True


def test_disconnect_seat():
    registry = AISeatRegistry()
    registry.add_seat("s1", "Claude")
    registry.disconnect_seat("s1")
    assert registry.seats["s1"]["connected"] is False
'''

# Codex's first attempt: a real, plausible bug -- forgets to actually flip
# the flag, so test_disconnect_seat fails for a real, printable reason.
BUGGY_PATCH_PY = '''\
class AISeatRegistry:
    def __init__(self):
        self.seats = {}

    def add_seat(self, seat_id, name):
        self.seats[seat_id] = {"name": name, "connected": True}

    def disconnect_seat(self, seat_id):
        pass
'''

FIXED_PATCH_PY = '''\
class AISeatRegistry:
    def __init__(self):
        self.seats = {}

    def add_seat(self, seat_id, name):
        self.seats[seat_id] = {"name": name, "connected": True}

    def disconnect_seat(self, seat_id):
        self.seats[seat_id]["connected"] = False
'''


def _print_message(chat: CouncilChat, m) -> None:
    who = "user" if m.sender_seat_id is None else chat.seats[m.sender_seat_id].name
    print(f"\n[{who}] {m.content}")


def run(project_dir: Path | None = None) -> bool:
    own_temp_dir = project_dir is None
    project_dir = project_dir or Path(tempfile.mkdtemp(prefix="council_chamber_demo_"))
    (project_dir / "seats.py").write_text(STARTER_SEATS_PY)
    (project_dir / "test_seats.py").write_text(STARTER_TEST_PY)

    chat = CouncilChat()
    council = Council(chat, PatchWorker(project_dir))
    test_worker = TestWorker(project_dir)

    chatgpt = MockSeat(
        Seat.create("ChatGPT", SeatKind.AI, model="gpt-5"),
        reply="Requirement: AISeatRegistry needs a disconnect_seat(seat_id) method that sets connected=False.",
    )
    codex = MockSeat(
        Seat.create("Codex", SeatKind.AI, model="gpt-5-codex"),
        reply="Patch proposed: add disconnect_seat to seats.py.",
    )
    council.register_ai_seat(chatgpt)
    council.register_ai_seat(codex)

    for m in council.ask([chatgpt.seat.seat_id], "Add disconnect support to the AI seats."):
        _print_message(chat, m)
    for m in council.ask([codex.seat.seat_id], "Inspect seats.py and propose a patch."):
        _print_message(chat, m)

    pending = council.propose_change(codex.seat.seat_id, "seats.py", BUGGY_PATCH_PY,
                                      description="add disconnect_seat")
    print(f"\n[diff for {pending.change.file_path}]\n{pending.diff}")

    print("\n[user] approved")
    council.approve_and_apply("seats.py")

    result = test_worker.run()
    _print_message(chat, chat.post(None, f"Test Worker: {result.summary}\n{result.stdout}"))

    if not result.passed:
        for m in council.ask([chatgpt.seat.seat_id], "Why did test_disconnect_seat fail?"):
            _print_message(chat, m)

        codex.reply = "Smaller repair: disconnect_seat wasn't setting connected=False. Fixing it."
        for m in council.ask([codex.seat.seat_id], "Propose a smaller repair."):
            _print_message(chat, m)

        pending = council.propose_change(codex.seat.seat_id, "seats.py", FIXED_PATCH_PY,
                                          description="actually set connected=False")
        print(f"\n[diff for {pending.change.file_path}]\n{pending.diff}")

        print("\n[user] approved")
        council.approve_and_apply("seats.py")

        result = test_worker.run()
        _print_message(chat, chat.post(None, f"Test Worker: {result.summary}\n{result.stdout}"))

    print(f"\n\nFinal result: {'ALL TESTS PASS' if result.passed else 'STILL FAILING'}")

    if own_temp_dir:
        shutil.rmtree(project_dir, ignore_errors=True)

    return result.passed


if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)
