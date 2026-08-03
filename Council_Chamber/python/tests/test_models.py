import pytest

from council_chamber.models import (
    CouncilChat, Seat, SeatKind, SeatStatus, SeatNotFoundError, SeatAlreadyOpenError,
)


def test_open_seat_adds_to_open_seats():
    chat = CouncilChat()
    seat = Seat.create("Claude", SeatKind.AI, model="claude-sonnet-5")
    chat.open_seat(seat)
    assert seat in chat.open_seats()


def test_close_seat_removes_from_open_seats():
    chat = CouncilChat()
    seat = Seat.create("Codex", SeatKind.AI)
    chat.open_seat(seat)
    chat.close_seat(seat.seat_id)
    assert seat not in chat.open_seats()
    assert chat.seats[seat.seat_id].status == SeatStatus.CLOSED


def test_opening_same_seat_twice_raises():
    chat = CouncilChat()
    seat = Seat.create("ChatGPT", SeatKind.AI)
    chat.open_seat(seat)
    with pytest.raises(SeatAlreadyOpenError):
        chat.open_seat(seat)


def test_reopening_a_closed_seat_is_allowed():
    chat = CouncilChat()
    seat = Seat.create("ChatGPT", SeatKind.AI)
    chat.open_seat(seat)
    chat.close_seat(seat.seat_id)

    # a fresh Seat instance with the same id, not a mutated alias of the
    # one already stored in chat.seats -- this is what a real caller
    # reopening a seat would construct
    reopened = Seat(seat_id=seat.seat_id, name=seat.name, kind=seat.kind, status=SeatStatus.OPEN)
    chat.open_seat(reopened)  # must not raise
    assert reopened in chat.open_seats()


def test_closing_unknown_seat_raises():
    chat = CouncilChat()
    with pytest.raises(SeatNotFoundError):
        chat.close_seat("seat_doesnotexist")


def test_post_from_user_has_none_sender():
    chat = CouncilChat()
    message = chat.post(None, "Build the first Wave Mapper waveform display.")
    assert message.sender_seat_id is None
    assert message in chat.messages


def test_post_from_unknown_seat_raises():
    chat = CouncilChat()
    with pytest.raises(SeatNotFoundError):
        chat.post("seat_ghost", "hello")


def test_post_from_open_seat_succeeds():
    chat = CouncilChat()
    seat = Seat.create("Gemini", SeatKind.AI)
    chat.open_seat(seat)
    message = chat.post(seat.seat_id, "I'd approach it differently.")
    assert message.sender_seat_id == seat.seat_id


def test_default_visibility_is_everyone():
    chat = CouncilChat()
    a = Seat.create("Claude", SeatKind.AI)
    b = Seat.create("Codex", SeatKind.AI)
    chat.open_seat(a)
    chat.open_seat(b)
    chat.post(None, "public message")

    assert len(chat.messages_visible_to(a.seat_id)) == 1
    assert len(chat.messages_visible_to(b.seat_id)) == 1


def test_restricted_visibility_hides_from_other_seats():
    chat = CouncilChat()
    a = Seat.create("Claude", SeatKind.AI)
    b = Seat.create("Codex", SeatKind.AI)
    chat.open_seat(a)
    chat.open_seat(b)
    chat.post(None, "only for claude", visible_to=[a.seat_id])

    assert len(chat.messages_visible_to(a.seat_id)) == 1
    assert len(chat.messages_visible_to(b.seat_id)) == 0


def test_sender_always_sees_its_own_restricted_message():
    chat = CouncilChat()
    a = Seat.create("Claude", SeatKind.AI)
    b = Seat.create("Codex", SeatKind.AI)
    chat.open_seat(a)
    chat.open_seat(b)
    chat.post(a.seat_id, "just thinking out loud", visible_to=[])

    assert len(chat.messages_visible_to(a.seat_id)) == 1
    assert len(chat.messages_visible_to(b.seat_id)) == 0


def test_no_auto_response_posting_a_message_does_not_trigger_anything():
    # the whole point: CouncilChat.post is inert. No seat "responds" on
    # its own -- that requires an explicit, separate call (the
    # orchestrator, built on top of this model).
    chat = CouncilChat()
    seat = Seat.create("Claude", SeatKind.AI)
    chat.open_seat(seat)
    chat.post(None, "hello")
    assert len(chat.messages) == 1


def test_transcript_round_trips_message_content():
    chat = CouncilChat()
    chat.post(None, "hello council")
    transcript = chat.transcript()
    assert len(transcript) == 1
    assert transcript[0]["content"] == "hello council"


def test_chatgpt_and_codex_are_separate_seats_despite_shared_provider():
    chat = CouncilChat()
    chatgpt = Seat.create("ChatGPT", SeatKind.AI, model="gpt-5")
    codex = Seat.create("Codex", SeatKind.AI, model="gpt-5-codex")
    chat.open_seat(chatgpt)
    chat.open_seat(codex)
    assert chatgpt.seat_id != codex.seat_id

    codex_message = chat.post(codex.seat_id, "here's a patch proposal")
    assert codex_message.sender_seat_id == codex.seat_id
    assert codex_message.sender_seat_id != chatgpt.seat_id
