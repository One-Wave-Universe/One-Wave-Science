from council_chamber.context import ContextPolicy
from council_chamber.models import CouncilChat, Seat, SeatKind
from council_chamber.seats.ai_seat import MockSeat
from council_chamber.workers.patch_worker import PatchWorker
from council_chamber.orchestrator import Council


def _chat_with_messages(n):
    chat = CouncilChat()
    for i in range(n):
        chat.post(None, f"message {i}")
    return chat


def test_default_policy_returns_full_history_unchanged():
    chat = _chat_with_messages(5)
    policy = ContextPolicy()

    curated = policy.curate(chat.messages)

    assert [m.content for m in curated] == [f"message {i}" for i in range(5)]


def test_max_messages_caps_to_most_recent():
    chat = _chat_with_messages(5)
    policy = ContextPolicy(max_messages=2)

    curated = policy.curate(chat.messages)

    assert [m.content for m in curated] == ["message 3", "message 4"]


def test_max_messages_zero_returns_only_pinned():
    chat = _chat_with_messages(3)
    policy = ContextPolicy(max_messages=0)
    policy.pin(chat.messages[0].message_id)

    curated = policy.curate(chat.messages)

    assert [m.content for m in curated] == ["message 0"]


def test_pinned_message_survives_outside_recency_window():
    chat = _chat_with_messages(5)
    policy = ContextPolicy(max_messages=2)
    policy.pin(chat.messages[0].message_id)  # "message 0" -- otherwise dropped

    curated = policy.curate(chat.messages)

    assert [m.content for m in curated] == ["message 0", "message 3", "message 4"]


def test_pinned_message_inside_window_is_not_duplicated():
    chat = _chat_with_messages(5)
    policy = ContextPolicy(max_messages=2)
    policy.pin(chat.messages[4].message_id)  # already inside the window

    curated = policy.curate(chat.messages)

    assert [m.content for m in curated] == ["message 3", "message 4"]


def test_unpin_removes_a_pinned_message():
    chat = _chat_with_messages(5)
    policy = ContextPolicy(max_messages=1)
    policy.pin(chat.messages[0].message_id)
    policy.unpin(chat.messages[0].message_id)

    curated = policy.curate(chat.messages)

    assert [m.content for m in curated] == ["message 4"]


def test_council_ask_sends_curated_context_to_seat(tmp_path):
    chat = CouncilChat()
    council = Council(chat, PatchWorker(tmp_path), context_policy=ContextPolicy(max_messages=1))

    seen_context_lengths = []

    def record_length(context):
        seen_context_lengths.append(len(context))
        return "ok"

    claude_seat = Seat.create("Claude", SeatKind.AI)
    council.register_ai_seat(MockSeat(claude_seat, reply=record_length))

    council.ask([claude_seat.seat_id], "first")
    council.ask([claude_seat.seat_id], "second")

    # Full history would be [1, 3] (user msg, then user+reply+user); with
    # max_messages=1 curation the seat only ever sees the latest message.
    assert seen_context_lengths == [1, 1]


def test_council_ask_respects_pinned_message_with_curated_policy(tmp_path):
    chat = CouncilChat()
    council = Council(chat, PatchWorker(tmp_path), context_policy=ContextPolicy(max_messages=1))

    seen_contents = []

    def record_contents(context):
        seen_contents.append([m.content for m in context])
        return "ok"

    claude_seat = Seat.create("Claude", SeatKind.AI)
    council.register_ai_seat(MockSeat(claude_seat, reply=record_contents))

    council.ask([claude_seat.seat_id], "pin me: use snake_case for all new code")
    pinned_id = chat.messages[0].message_id
    council.context_policy.pin(pinned_id)

    council.ask([claude_seat.seat_id], "second unrelated prompt")

    assert seen_contents[1][0] == "pin me: use snake_case for all new code"
