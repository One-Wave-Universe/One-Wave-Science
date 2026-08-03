"""Council orchestrator: routes a message to explicitly-selected seats,
collects labeled responses into the shared log, and gates code changes
behind an explicit preview/approve/reject step.

Nothing here auto-continues a conversation -- ask() runs exactly one
round against exactly the seats named in the call. A proposed change is
never written to disk until approve_and_apply() is called, separately
and explicitly, on that specific ProposedChange.
"""

from __future__ import annotations

from dataclasses import dataclass

from council_chamber.models import CouncilChat, Message, Seat
from council_chamber.seats.ai_seat import AISeat
from council_chamber.workers.patch_worker import PatchWorker, ProposedChange, PatchResult


class SeatNotRegisteredError(KeyError):
    pass


@dataclass
class PendingChange:
    change: ProposedChange
    proposed_by_seat_id: str
    diff: str
    message_id: str


class Council:
    def __init__(self, chat: CouncilChat, patch_worker: PatchWorker):
        self.chat = chat
        self.patch_worker = patch_worker
        self.ai_seats: dict[str, AISeat] = {}
        self.pending_changes: dict[str, PendingChange] = {}  # keyed by change file_path

    def register_ai_seat(self, ai_seat: AISeat) -> None:
        seat = ai_seat.seat
        if seat.seat_id not in self.chat.seats:
            self.chat.open_seat(seat)
        self.ai_seats[seat.seat_id] = ai_seat

    def ask(self, seat_ids: list[str], prompt: str) -> list[Message]:
        """Post `prompt` as the user, then ask exactly these seats -- one
        round, no follow-up, no seat sees this call unless it's named."""
        for seat_id in seat_ids:
            if seat_id not in self.ai_seats:
                raise SeatNotRegisteredError(seat_id)

        user_message = self.chat.post(None, prompt)
        responses = []
        for seat_id in seat_ids:
            ai_seat = self.ai_seats[seat_id]
            context = self.chat.messages_visible_to(seat_id)
            reply_text = ai_seat.respond(context)
            reply_message = self.chat.post(seat_id, reply_text, in_response_to=user_message.message_id)
            responses.append(reply_message)
        return responses

    def propose_change(self, seat_id: str, file_path: str, new_content: str, description: str = "") -> PendingChange:
        if seat_id not in self.ai_seats:
            raise SeatNotRegisteredError(seat_id)

        change = ProposedChange(file_path=file_path, new_content=new_content, description=description)
        diff = self.patch_worker.preview_diff(change)
        summary = f"Proposed change to {file_path}: {description}\n\n{diff}"
        message = self.chat.post(seat_id, summary)

        pending = PendingChange(change=change, proposed_by_seat_id=seat_id, diff=diff, message_id=message.message_id)
        self.pending_changes[file_path] = pending
        return pending

    def approve_and_apply(self, file_path: str) -> PatchResult:
        pending = self.pending_changes.pop(file_path, None)
        if pending is None:
            return PatchResult(success=False, message=f"no pending change for {file_path}")

        result = self.patch_worker.apply(pending.change)
        status = "applied" if result.success else f"failed: {result.message}"
        self.chat.post(None, f"[approved] {file_path} -- {status}")
        return result

    def reject(self, file_path: str, reason: str = "") -> None:
        pending = self.pending_changes.pop(file_path, None)
        note = f"[rejected] {file_path}"
        if reason:
            note += f" -- {reason}"
        self.chat.post(None, note)
        if pending is None:
            raise KeyError(f"no pending change for {file_path}")
