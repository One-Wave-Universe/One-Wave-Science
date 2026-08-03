"""Context curation: what subset of a seat's visible history actually
gets sent to it on each ask() call, instead of the full transcript every
time -- the spec's "an AI seat receives only the information relevant to
its current task... this saves tokens."

Kept intentionally simple and inspectable rather than spending an AI call
to summarize or rank messages -- that would contradict the spec's own
local-first principle that ordinary operations shouldn't cost a chatbot
response. Two honest levers instead: a recency window, and explicit
pinning of messages (e.g. a pinned requirement) that are always included
no matter how old they are.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from council_chamber.models import Message


@dataclass
class ContextPolicy:
    max_messages: int | None = None  # None = no recency cap, full history
    pinned_message_ids: set[str] = field(default_factory=set)

    def pin(self, message_id: str) -> None:
        self.pinned_message_ids.add(message_id)

    def unpin(self, message_id: str) -> None:
        self.pinned_message_ids.discard(message_id)

    def curate(self, messages: list[Message]) -> list[Message]:
        """Return messages in chronological order: pinned messages older
        than the recency window first, then the window itself."""
        if self.max_messages is None:
            return list(messages)

        recent = messages[-self.max_messages:] if self.max_messages > 0 else []
        recent_ids = {m.message_id for m in recent}
        pinned = [m for m in messages if m.message_id in self.pinned_message_ids and m.message_id not in recent_ids]
        return pinned + recent
