"""Core data model: seats, messages, and the shared council log.

The chat is deliberately inert by default -- posting a message never
triggers another seat to respond on its own. The user (or the
orchestrator acting on the user's explicit instruction) decides which
seats receive each message and when the next round happens, per the
spec's "the system must not allow the AIs to generate an uncontrolled
endless conversation."
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum


class SeatKind(Enum):
    AI = "ai"
    LOCAL_WORKER = "local_worker"


class SeatStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    DISCONNECTED = "disconnected"


@dataclass
class Seat:
    seat_id: str
    name: str
    kind: SeatKind
    status: SeatStatus = SeatStatus.OPEN
    model: str | None = None
    description: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["kind"] = self.kind.value
        d["status"] = self.status.value
        return d

    @classmethod
    def create(cls, name: str, kind: SeatKind, model: str | None = None, description: str = "") -> "Seat":
        return cls(seat_id=f"seat_{uuid.uuid4().hex[:8]}", name=name, kind=kind, model=model,
                    description=description)


@dataclass
class Message:
    message_id: str
    sender_seat_id: str | None  # None = the user
    content: str
    created_at: str
    in_response_to: str | None = None
    visible_to: list | None = None  # None = visible to everyone; else list of seat_ids

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def create(cls, sender_seat_id: str | None, content: str, in_response_to: str | None = None,
               visible_to: list | None = None) -> "Message":
        return cls(
            message_id=f"msg_{uuid.uuid4().hex[:8]}",
            sender_seat_id=sender_seat_id,
            content=content,
            created_at=datetime.now(timezone.utc).isoformat(),
            in_response_to=in_response_to,
            visible_to=visible_to,
        )


class SeatNotFoundError(KeyError):
    pass


class SeatAlreadyOpenError(ValueError):
    pass


@dataclass
class CouncilChat:
    seats: dict = field(default_factory=dict)  # seat_id -> Seat
    messages: list = field(default_factory=list)  # ordered list[Message]

    def open_seat(self, seat: Seat) -> None:
        if seat.seat_id in self.seats and self.seats[seat.seat_id].status == SeatStatus.OPEN:
            raise SeatAlreadyOpenError(f"seat {seat.seat_id} is already open")
        self.seats[seat.seat_id] = seat

    def close_seat(self, seat_id: str) -> None:
        seat = self._require_seat(seat_id)
        seat.status = SeatStatus.CLOSED

    def mark_disconnected(self, seat_id: str) -> None:
        seat = self._require_seat(seat_id)
        seat.status = SeatStatus.DISCONNECTED

    def open_seats(self) -> list:
        return [s for s in self.seats.values() if s.status == SeatStatus.OPEN]

    def _require_seat(self, seat_id: str) -> Seat:
        if seat_id not in self.seats:
            raise SeatNotFoundError(seat_id)
        return self.seats[seat_id]

    def post(self, sender_seat_id: str | None, content: str, in_response_to: str | None = None,
              visible_to: list | None = None) -> Message:
        if sender_seat_id is not None:
            self._require_seat(sender_seat_id)
        message = Message.create(sender_seat_id, content, in_response_to, visible_to)
        self.messages.append(message)
        return message

    def messages_visible_to(self, seat_id: str) -> list:
        """User messages and messages with no visibility restriction are
        visible to every seat; a restricted message only to the seats
        named in its visible_to list (plus its own sender)."""
        visible = []
        for m in self.messages:
            if m.visible_to is None or seat_id in m.visible_to or m.sender_seat_id == seat_id:
                visible.append(m)
        return visible

    def transcript(self) -> list:
        return [m.to_dict() for m in self.messages]
