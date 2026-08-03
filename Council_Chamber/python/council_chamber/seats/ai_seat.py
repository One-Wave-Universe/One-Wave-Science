"""AI seat interface: one method, respond(context) -> str.

The orchestrator decides what subset of the council log a seat receives
(the spec's "only the information relevant to its current task") --
AISeat implementations just answer with whatever context they're handed.

MockSeat is a real, working implementation used for testing the rest of
the system without any network access. RemoteAPISeat is the honest
placeholder for a real ChatGPT/Codex/Gemini/etc. connection: it takes an
injected `client` callable that would perform the actual API call, and
raises a clear error if none is supplied, rather than silently
fabricating a response. No client is wired to a real provider here --
this container has no API keys for OpenAI, Google, or any provider other
than the Anthropic session it's already running in.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

from council_chamber.models import Message, Seat


class AISeat(ABC):
    def __init__(self, seat: Seat):
        self.seat = seat

    @abstractmethod
    def respond(self, context: list[Message]) -> str:
        """Given a curated list of Messages, return this seat's reply text."""
        raise NotImplementedError


class MockSeat(AISeat):
    """A working, deterministic seat for tests and offline demos. Either a
    fixed reply string or a callable(context) -> str."""

    def __init__(self, seat: Seat, reply: str | Callable[[list[Message]], str] = "(mock reply)"):
        super().__init__(seat)
        self.reply = reply
        self.received_contexts: list[list[Message]] = []

    def respond(self, context: list[Message]) -> str:
        self.received_contexts.append(context)
        if callable(self.reply):
            return self.reply(context)
        return self.reply


class SeatNotConfiguredError(RuntimeError):
    pass


class RemoteAPISeat(AISeat):
    """Placeholder for a real provider connection (ChatGPT, Codex, Gemini,
    DeepSeek, ...). Supply `client`, a callable(context) -> str that
    performs the actual API call, to make this seat real; without one,
    respond() raises rather than fabricating output."""

    def __init__(self, seat: Seat, client: Callable[[list[Message]], str] | None = None):
        super().__init__(seat)
        self.client = client

    def respond(self, context: list[Message]) -> str:
        if self.client is None:
            raise SeatNotConfiguredError(
                f"seat {self.seat.name!r} ({self.seat.seat_id}) has no API client configured -- "
                "supply one via RemoteAPISeat(seat, client=...) to connect it to a real provider"
            )
        return self.client(context)
