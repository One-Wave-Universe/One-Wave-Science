import json

from council_chamber.models import CouncilChat, Seat, SeatKind, SeatStatus
from council_chamber.seats.ai_seat import MockSeat
from council_chamber.workers.patch_worker import PatchWorker
from council_chamber.orchestrator import Council
from council_chamber.storage import (
    chat_to_dict, chat_from_dict, save_chat, load_chat,
    session_to_dict, save_session, load_session,
)


def test_chat_round_trips_seats_and_messages(tmp_path):
    chat = CouncilChat()
    claude_seat = Seat.create("Claude", SeatKind.AI, model="claude-5")
    chat.open_seat(claude_seat)
    chat.post(None, "hello everyone")
    chat.post(claude_seat.seat_id, "hi there", visible_to=[claude_seat.seat_id])
    chat.close_seat(claude_seat.seat_id)

    path = tmp_path / "chat.json"
    save_chat(chat, path)
    restored = load_chat(path)

    assert restored.seats[claude_seat.seat_id].name == "Claude"
    assert restored.seats[claude_seat.seat_id].model == "claude-5"
    assert restored.seats[claude_seat.seat_id].status == SeatStatus.CLOSED
    assert [m.content for m in restored.messages] == ["hello everyone", "hi there"]
    assert restored.messages[1].visible_to == [claude_seat.seat_id]
    assert restored.messages[1].sender_seat_id == claude_seat.seat_id


def test_chat_to_dict_from_dict_round_trip_is_lossless():
    chat = CouncilChat()
    seat = Seat.create("Codex", SeatKind.AI)
    chat.open_seat(seat)
    chat.post(None, "prompt")

    restored = chat_from_dict(chat_to_dict(chat))

    assert restored.seats.keys() == chat.seats.keys()
    assert [m.content for m in restored.messages] == [m.content for m in chat.messages]


def test_load_chat_with_no_seats_or_messages_gives_empty_chat(tmp_path):
    path = tmp_path / "empty.json"
    save_chat(CouncilChat(), path)

    restored = load_chat(path)

    assert restored.seats == {}
    assert restored.messages == []


def test_session_round_trip_restores_pending_changes(tmp_path):
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / "main.py").write_text("def add(a, b):\n    return a + b\n")

    chat = CouncilChat()
    council = Council(chat, PatchWorker(project_dir))
    codex_seat = Seat.create("Codex", SeatKind.AI)
    council.register_ai_seat(MockSeat(codex_seat, reply="proposing"))
    council.propose_change(
        codex_seat.seat_id, "main.py", "def add(a, b):\n    return a + b + 1\n",
        description="fix off-by-one",
    )

    session_path = tmp_path / "session.json"
    save_session(council, session_path)
    restored = load_session(session_path, PatchWorker(project_dir))

    assert "main.py" in restored.pending_changes
    pending = restored.pending_changes["main.py"]
    assert pending.change.new_content == "def add(a, b):\n    return a + b + 1\n"
    assert pending.change.description == "fix off-by-one"
    assert pending.proposed_by_seat_id == codex_seat.seat_id
    assert pending.diff == council.pending_changes["main.py"].diff
    assert codex_seat.seat_id in restored.chat.seats
    # no AISeat objects are reconstructed -- the caller re-registers them
    assert restored.ai_seats == {}


def test_load_session_with_no_pending_changes_key_gives_empty_pending(tmp_path):
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    chat = CouncilChat()
    council = Council(chat, PatchWorker(project_dir))

    session_path = tmp_path / "session.json"
    session_path.write_text(json.dumps({"chat": chat_to_dict(chat)}))

    restored = load_session(session_path, PatchWorker(project_dir))

    assert restored.pending_changes == {}


def test_session_to_dict_pending_changes_are_json_serializable(tmp_path):
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / "main.py").write_text("x = 1\n")

    chat = CouncilChat()
    council = Council(chat, PatchWorker(project_dir))
    codex_seat = Seat.create("Codex", SeatKind.AI)
    council.register_ai_seat(MockSeat(codex_seat, reply="proposing"))
    council.propose_change(codex_seat.seat_id, "main.py", "x = 2\n")

    data = session_to_dict(council)

    assert "main.py" in data["pending_changes"]
    assert data["pending_changes"]["main.py"]["change"]["new_content"] == "x = 2\n"
