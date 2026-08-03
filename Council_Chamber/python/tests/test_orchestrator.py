import pytest

from council_chamber.models import CouncilChat, Seat, SeatKind
from council_chamber.seats.ai_seat import MockSeat
from council_chamber.workers.patch_worker import PatchWorker
from council_chamber.orchestrator import Council, SeatNotRegisteredError


@pytest.fixture
def sample_project(tmp_path):
    (tmp_path / "main.py").write_text("def add(a, b):\n    return a + b\n")
    return tmp_path


@pytest.fixture
def council(sample_project):
    chat = CouncilChat()
    return Council(chat, PatchWorker(sample_project))


def test_register_ai_seat_opens_it_in_chat(council):
    seat = Seat.create("Claude", SeatKind.AI)
    council.register_ai_seat(MockSeat(seat, reply="ready"))
    assert seat in council.chat.open_seats()


def test_ask_posts_user_message_and_labeled_replies(council):
    claude_seat = Seat.create("Claude", SeatKind.AI)
    codex_seat = Seat.create("Codex", SeatKind.AI)
    council.register_ai_seat(MockSeat(claude_seat, reply="I'd check the architecture first."))
    council.register_ai_seat(MockSeat(codex_seat, reply="Here's a patch proposal."))

    replies = council.ask([claude_seat.seat_id, codex_seat.seat_id], "Build the waveform display.")

    assert len(replies) == 2
    assert replies[0].sender_seat_id == claude_seat.seat_id
    assert replies[1].sender_seat_id == codex_seat.seat_id
    assert replies[0].content == "I'd check the architecture first."
    assert replies[1].content == "Here's a patch proposal."

    transcript = council.chat.transcript()
    assert transcript[0]["sender_seat_id"] is None  # the user's prompt
    assert transcript[0]["content"] == "Build the waveform display."


def test_ask_only_queries_named_seats(council):
    claude_seat = Seat.create("Claude", SeatKind.AI)
    gemini_seat = Seat.create("Gemini", SeatKind.AI)
    claude_mock = MockSeat(claude_seat, reply="claude speaking")
    gemini_mock = MockSeat(gemini_seat, reply="gemini speaking")
    council.register_ai_seat(claude_mock)
    council.register_ai_seat(gemini_mock)

    council.ask([claude_seat.seat_id], "only claude, please")

    assert len(claude_mock.received_contexts) == 1
    assert len(gemini_mock.received_contexts) == 0


def test_ask_with_unregistered_seat_raises(council):
    with pytest.raises(SeatNotRegisteredError):
        council.ask(["seat_ghost"], "hello?")


def test_seat_receives_prior_messages_as_context(council):
    claude_seat = Seat.create("Claude", SeatKind.AI)

    def echo_message_count(context):
        return f"I see {len(context)} messages so far"

    council.register_ai_seat(MockSeat(claude_seat, reply=echo_message_count))
    council.ask([claude_seat.seat_id], "first message")
    replies = council.ask([claude_seat.seat_id], "second message")

    # context includes: msg1 (user), msg2 (claude's first reply), msg3 (user, this prompt)
    assert replies[0].content == "I see 3 messages so far"


def test_propose_change_posts_diff_without_writing_file(council, sample_project):
    codex_seat = Seat.create("Codex", SeatKind.AI)
    council.register_ai_seat(MockSeat(codex_seat, reply="proposing"))

    pending = council.propose_change(
        codex_seat.seat_id, "main.py", "def add(a, b):\n    return a + b + 1\n",
        description="fix off-by-one",
    )

    assert "return a + b + 1" in pending.diff
    assert (sample_project / "main.py").read_text() == "def add(a, b):\n    return a + b\n"  # unchanged
    assert "main.py" in council.pending_changes


def test_approve_and_apply_writes_file_and_clears_pending(council, sample_project):
    codex_seat = Seat.create("Codex", SeatKind.AI)
    council.register_ai_seat(MockSeat(codex_seat, reply="proposing"))
    council.propose_change(codex_seat.seat_id, "main.py", "def add(a, b):\n    return a + b + 1\n")

    result = council.approve_and_apply("main.py")

    assert result.success is True
    assert (sample_project / "main.py").read_text() == "def add(a, b):\n    return a + b + 1\n"
    assert "main.py" not in council.pending_changes


def test_reject_does_not_write_file_and_clears_pending(council, sample_project):
    codex_seat = Seat.create("Codex", SeatKind.AI)
    council.register_ai_seat(MockSeat(codex_seat, reply="proposing"))
    council.propose_change(codex_seat.seat_id, "main.py", "def add(a, b):\n    return a + b + 1\n")

    council.reject("main.py", reason="not needed")

    assert (sample_project / "main.py").read_text() == "def add(a, b):\n    return a + b\n"
    assert "main.py" not in council.pending_changes


def test_approve_with_no_pending_change_fails_gracefully(council):
    result = council.approve_and_apply("does_not_exist.py")
    assert result.success is False


def test_chat_shows_labeled_approval_outcome(council, sample_project):
    codex_seat = Seat.create("Codex", SeatKind.AI)
    council.register_ai_seat(MockSeat(codex_seat, reply="proposing"))
    council.propose_change(codex_seat.seat_id, "main.py", "def add(a, b):\n    return a + b + 1\n")
    council.approve_and_apply("main.py")

    transcript = council.chat.transcript()
    assert any("[approved] main.py" in m["content"] for m in transcript)
