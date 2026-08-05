"""Local session persistence (JSON) -- "the authoritative project memory
belongs to the local computer, not to any individual chatbot" (spec).

Saves/restores the chat log, seat identities, and any pending (proposed
but not yet approved) changes, so a session survives a process restart.
Live AI seat connections (API clients, etc.) are not serializable and are
not saved -- after loading, the caller re-registers whatever AISeat
implementations it wants against the restored seat identities.
"""

from __future__ import annotations

import json
from pathlib import Path

from council_chamber.models import CouncilChat, Message, Seat, SeatKind, SeatStatus
from council_chamber.orchestrator import Council, PendingChange
from council_chamber.rooms import Room, World
from council_chamber.workers.patch_worker import PatchWorker, ProposedChange


def _seat_from_dict(d: dict) -> Seat:
    return Seat(
        seat_id=d["seat_id"], name=d["name"], kind=SeatKind(d["kind"]),
        status=SeatStatus(d["status"]), model=d.get("model"), description=d.get("description", ""),
    )


def _message_from_dict(d: dict) -> Message:
    return Message(
        message_id=d["message_id"], sender_seat_id=d["sender_seat_id"], content=d["content"],
        created_at=d["created_at"], in_response_to=d.get("in_response_to"), visible_to=d.get("visible_to"),
    )


def chat_to_dict(chat: CouncilChat) -> dict:
    return {
        "seats": [s.to_dict() for s in chat.seats.values()],
        "messages": [m.to_dict() for m in chat.messages],
    }


def chat_from_dict(data: dict) -> CouncilChat:
    chat = CouncilChat()
    for seat_dict in data.get("seats", []):
        seat = _seat_from_dict(seat_dict)
        chat.seats[seat.seat_id] = seat
    for message_dict in data.get("messages", []):
        chat.messages.append(_message_from_dict(message_dict))
    return chat


def save_chat(chat: CouncilChat, path: str | Path) -> None:
    Path(path).write_text(json.dumps(chat_to_dict(chat), indent=2))


def load_chat(path: str | Path) -> CouncilChat:
    return chat_from_dict(json.loads(Path(path).read_text()))


def _pending_changes_to_dict(pending_changes: dict[str, PendingChange]) -> dict:
    return {
        file_path: {
            "change": {
                "file_path": pc.change.file_path,
                "new_content": pc.change.new_content,
                "description": pc.change.description,
            },
            "proposed_by_seat_id": pc.proposed_by_seat_id,
            "diff": pc.diff,
            "message_id": pc.message_id,
        }
        for file_path, pc in pending_changes.items()
    }


def _pending_changes_from_dict(data: dict) -> dict[str, PendingChange]:
    pending_changes = {}
    for file_path, pc_dict in data.items():
        change = ProposedChange(**pc_dict["change"])
        pending_changes[file_path] = PendingChange(
            change=change,
            proposed_by_seat_id=pc_dict["proposed_by_seat_id"],
            diff=pc_dict["diff"],
            message_id=pc_dict["message_id"],
        )
    return pending_changes


def session_to_dict(council: Council) -> dict:
    return {
        "chat": chat_to_dict(council.chat),
        "pending_changes": _pending_changes_to_dict(council.pending_changes),
    }


def save_session(council: Council, path: str | Path) -> None:
    Path(path).write_text(json.dumps(session_to_dict(council), indent=2))


def load_session(path: str | Path, patch_worker: PatchWorker) -> Council:
    data = json.loads(Path(path).read_text())
    chat = chat_from_dict(data["chat"])
    council = Council(chat, patch_worker)
    council.pending_changes.update(_pending_changes_from_dict(data.get("pending_changes", {})))
    return council


def world_to_dict(world: World) -> dict:
    """A World is every room's name, its real project directory (the
    files themselves are already persisted on disk -- this only needs
    the path), and that room's session (chat + pending changes)."""
    return {
        "rooms": {
            name: {"project_dir": str(room.project_dir), "session": session_to_dict(room.council)}
            for name, room in world.rooms.items()
        }
    }


def save_world(world: World, path: str | Path) -> None:
    Path(path).write_text(json.dumps(world_to_dict(world), indent=2))


def world_from_dict(data: dict) -> World:
    world = World()
    for name, room_data in data.get("rooms", {}).items():
        project_dir = room_data["project_dir"]
        session = room_data["session"]
        chat = chat_from_dict(session["chat"])
        council = Council(chat, PatchWorker(project_dir))
        council.pending_changes.update(_pending_changes_from_dict(session.get("pending_changes", {})))
        world.rooms[name] = Room(name, project_dir, council=council)
    return world


def load_world(path: str | Path) -> World:
    return world_from_dict(json.loads(Path(path).read_text()))
