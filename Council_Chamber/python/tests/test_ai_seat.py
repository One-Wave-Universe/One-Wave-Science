import pytest

from council_chamber.models import Seat, SeatKind
from council_chamber.seats.ai_seat import MockSeat, RemoteAPISeat, SeatNotConfiguredError


def test_mock_seat_returns_fixed_reply():
    seat = Seat.create("Claude", SeatKind.AI)
    mock = MockSeat(seat, reply="looks good to me")
    assert mock.respond([]) == "looks good to me"


def test_mock_seat_records_received_context():
    seat = Seat.create("Codex", SeatKind.AI)
    mock = MockSeat(seat, reply="ok")
    context = ["fake-context-item"]
    mock.respond(context)
    assert mock.received_contexts == [context]


def test_mock_seat_supports_callable_reply():
    seat = Seat.create("Gemini", SeatKind.AI)
    mock = MockSeat(seat, reply=lambda ctx: f"I see {len(ctx)} messages")
    assert mock.respond([1, 2, 3]) == "I see 3 messages"


def test_remote_seat_without_client_raises_clear_error():
    seat = Seat.create("ChatGPT", SeatKind.AI, model="gpt-5")
    remote = RemoteAPISeat(seat)
    with pytest.raises(SeatNotConfiguredError, match="ChatGPT"):
        remote.respond([])


def test_remote_seat_with_injected_client_works():
    seat = Seat.create("ChatGPT", SeatKind.AI, model="gpt-5")
    remote = RemoteAPISeat(seat, client=lambda ctx: "hello from the real API")
    assert remote.respond([]) == "hello from the real API"


def test_chatgpt_and_codex_seats_are_independent_instances():
    chatgpt_seat = Seat.create("ChatGPT", SeatKind.AI, model="gpt-5")
    codex_seat = Seat.create("Codex", SeatKind.AI, model="gpt-5-codex")

    chatgpt = MockSeat(chatgpt_seat, reply="chatgpt says hi")
    codex = MockSeat(codex_seat, reply="codex says hi")

    assert chatgpt.respond([]) != codex.respond([])
    assert chatgpt.seat.seat_id != codex.seat.seat_id
