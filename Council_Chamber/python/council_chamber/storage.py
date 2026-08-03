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


def session_to_dict(council: Council) -> dict:
    pending = {
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
        for file_path, pc in council.pending_changes.items()
    }
    return {"chat": chat_to_dict(council.chat), "pending_changes": pending}


def save_session(council: Council, path: str | Path) -> None:
    Path(path).write_text(json.dumps(session_to_dict(council), indent=2))


def load_session(path: str | Path, patch_worker: PatchWorker) -> Council:
    data = json.loads(Path(path).read_text())
    chat = chat_from_dict(data["chat"])
    council = Council(chat, patch_worker)

    for file_path, pc_dict in data.get("pending_changes", {}).items():
        change = ProposedChange(**pc_dict["change"])
        council.pending_changes[file_path] = PendingChange(
            change=change,
            proposed_by_seat_id=pc_dict["proposed_by_seat_id"],
            diff=pc_dict["diff"],
            message_id=pc_dict["message_id"],
        )
    return council
