"""Minimal terminal UI over Council -- the spec's "shared coding
workspace" (file tree / diff viewer / approve-reject controls) as a real
command interpreter, not a mockup.

CouncilTUI.execute(line) parses and runs exactly one command and returns
the text that would be printed, so the whole interface is unit-testable
without a real terminal or any AI provider. repl(council) wraps it in an
actual input()/print() loop for interactive use.
"""

from __future__ import annotations

import shlex
import sys
from pathlib import Path

from council_chamber.models import CouncilChat, Seat, SeatKind
from council_chamber.orchestrator import Council
from council_chamber.seats.ai_seat import MockSeat
from council_chamber.storage import save_session, load_session
from council_chamber.usage import summarize
from council_chamber.workers.patch_worker import PatchWorker

# Every seat kind the spec names as a possible council-table seat. Any of
# these can be opened on demand with `open <key>` -- there is nothing
# ChatGPT- or Codex-specific in propose_change/approve_and_apply/ask;
# whichever seat is registered can supply code the same way. All of them
# are MockSeat placeholders until a real client is wired into a
# RemoteAPISeat for that seat, since this environment has no provider
# API keys.
SEAT_CATALOG: dict[str, str] = {
    "chatgpt": "ChatGPT",
    "codex": "Codex",
    "claude": "Claude",
    "gemini": "Gemini",
    "deepseek": "DeepSeek",
    "grok": "Grok",
    "local": "Local Model",
}

_PLACEHOLDER_REPLY = "(demo seat -- no real provider connected; see RemoteAPISeat in seats/ai_seat.py)"

HELP_TEXT = """\
Commands:
  seats                                  list open seats
  open <{catalog}>
                                          open a new seat from the catalog
  ask <seat[,seat...]> <prompt...>       ask one or more seats (by name or seat_id)
  propose <seat> <file> <content> [--desc "..."]
                                          propose a change (use \\n for newlines in content)
  pending                                 list files with an unapproved proposed change
  diff <file>                            show the diff for a pending change
  approve <file>                         apply a pending change
  reject <file> [reason...]              discard a pending change
  usage <seat>                           show raw usage reports for a seat
  usage-summary <seat>                   show totals (None where nothing was reported)
  transcript                             print the full chat log
  save <path>                            save the chat + pending changes to disk
  load <path>                            load a saved session (re-attaches AI seats as placeholders)
  help                                   show this text
  quit / exit                            leave the council chamber
""".format(catalog="|".join(SEAT_CATALOG))


def open_catalog_seat(council: Council, key: str) -> Seat:
    """Open a new seat of the given catalog kind as a MockSeat placeholder
    and register it with `council`. Any seat opened this way can ask/be
    asked and propose_change exactly like every other -- there is no
    special-cased "only Codex can write code" path."""
    key = key.lower()
    if key not in SEAT_CATALOG:
        raise ValueError(f"unknown seat {key!r} -- catalog: {', '.join(SEAT_CATALOG)}")
    seat = Seat.create(SEAT_CATALOG[key], SeatKind.AI)
    council.register_ai_seat(MockSeat(seat, reply=_PLACEHOLDER_REPLY))
    return seat


class UnknownCommandError(ValueError):
    pass


class SeatNotFoundError(ValueError):
    pass


class CouncilTUI:
    def __init__(self, council: Council):
        self.council = council

    def _resolve_seat_id(self, token: str) -> str:
        if token in self.council.chat.seats:
            return token
        for seat in self.council.chat.seats.values():
            if seat.name.lower() == token.lower():
                return seat.seat_id
        raise SeatNotFoundError(f"no seat named or id'd {token!r}")

    def execute(self, line: str) -> str:
        line = line.strip()
        if not line:
            return ""
        parts = shlex.split(line)
        command, args = parts[0], parts[1:]

        handlers = {
            "help": lambda: HELP_TEXT,
            "seats": self._cmd_seats,
            "open": lambda: self._cmd_open(args),
            "ask": lambda: self._cmd_ask(args),
            "propose": lambda: self._cmd_propose(args),
            "pending": self._cmd_pending,
            "diff": lambda: self._cmd_diff(args),
            "approve": lambda: self._cmd_approve(args),
            "reject": lambda: self._cmd_reject(args),
            "usage": lambda: self._cmd_usage(args),
            "usage-summary": lambda: self._cmd_usage_summary(args),
            "transcript": self._cmd_transcript,
            "save": lambda: self._cmd_save(args),
            "load": lambda: self._cmd_load(args),
            "quit": lambda: "goodbye",
            "exit": lambda: "goodbye",
        }
        if command not in handlers:
            raise UnknownCommandError(f"unknown command {command!r} -- type 'help' for a list")
        return handlers[command]()

    def _cmd_seats(self) -> str:
        seats = list(self.council.chat.seats.values())
        if not seats:
            return "(no seats open)"
        return "\n".join(f"{s.name} ({s.seat_id}) [{s.status.value}]" for s in seats)

    def _cmd_open(self, args: list[str]) -> str:
        if not args:
            raise ValueError(f"usage: open <{'|'.join(SEAT_CATALOG)}>")
        seat = open_catalog_seat(self.council, args[0])
        return f"opened {seat.name} ({seat.seat_id})"

    def _cmd_ask(self, args: list[str]) -> str:
        if len(args) < 2:
            raise ValueError("usage: ask <seat[,seat...]> <prompt...>")
        seat_ids = [self._resolve_seat_id(tok) for tok in args[0].split(",")]
        prompt = " ".join(args[1:])
        replies = self.council.ask(seat_ids, prompt)
        lines = [f"[{self.council.chat.seats[r.sender_seat_id].name}] {r.content}" for r in replies]
        return "\n".join(lines)

    def _cmd_propose(self, args: list[str]) -> str:
        desc = ""
        if "--desc" in args:
            idx = args.index("--desc")
            desc = args[idx + 1]
            args = args[:idx] + args[idx + 2:]
        if len(args) < 3:
            raise ValueError('usage: propose <seat> <file> <content> [--desc "..."]')
        seat_id = self._resolve_seat_id(args[0])
        file_path = args[1]
        content = args[2].replace("\\n", "\n")
        pending = self.council.propose_change(seat_id, file_path, content, description=desc)
        return f"proposed change to {file_path}\n{pending.diff}"

    def _cmd_pending(self) -> str:
        if not self.council.pending_changes:
            return "(no pending changes)"
        return "\n".join(self.council.pending_changes.keys())

    def _cmd_diff(self, args: list[str]) -> str:
        if not args:
            raise ValueError("usage: diff <file>")
        pending = self.council.pending_changes.get(args[0])
        if pending is None:
            return f"no pending change for {args[0]}"
        return pending.diff

    def _cmd_approve(self, args: list[str]) -> str:
        if not args:
            raise ValueError("usage: approve <file>")
        result = self.council.approve_and_apply(args[0])
        return result.message

    def _cmd_reject(self, args: list[str]) -> str:
        if not args:
            raise ValueError("usage: reject <file> [reason...]")
        reason = " ".join(args[1:])
        self.council.reject(args[0], reason=reason)
        return f"rejected {args[0]}"

    def _cmd_usage(self, args: list[str]) -> str:
        if not args:
            raise ValueError("usage: usage <seat>")
        seat_id = self._resolve_seat_id(args[0])
        reports = self.council.usage_for(seat_id)
        if not reports:
            return "(no usage recorded)"
        return "\n".join(str(r.to_dict()) for r in reports)

    def _cmd_usage_summary(self, args: list[str]) -> str:
        if not args:
            raise ValueError("usage: usage-summary <seat>")
        seat_id = self._resolve_seat_id(args[0])
        return str(summarize(self.council.usage_for(seat_id)))

    def _cmd_transcript(self) -> str:
        transcript = self.council.chat.transcript()
        if not transcript:
            return "(empty)"
        lines = []
        for m in transcript:
            who = "user" if m["sender_seat_id"] is None else self.council.chat.seats[m["sender_seat_id"]].name
            lines.append(f"[{who}] {m['content']}")
        return "\n".join(lines)

    def _cmd_save(self, args: list[str]) -> str:
        if not args:
            raise ValueError("usage: save <path>")
        save_session(self.council, args[0])
        return f"saved session to {args[0]}"

    def _cmd_load(self, args: list[str]) -> str:
        """Restore a saved session's seats and transcript. Live AI
        connections are never persisted (see storage.py), so every AI-kind
        seat that comes back is re-attached as a MockSeat placeholder here
        -- presence and conversation survive the restart; a real provider
        connection still has to be wired in again via RemoteAPISeat."""
        if not args:
            raise ValueError("usage: load <path>")
        self.council = load_session(args[0], self.council.patch_worker)
        reattached = 0
        for seat in self.council.chat.seats.values():
            if seat.kind == SeatKind.AI:
                self.council.register_ai_seat(MockSeat(seat, reply=_PLACEHOLDER_REPLY))
                reattached += 1
        return (
            f"loaded session from {args[0]} -- {len(self.council.chat.seats)} seat(s), "
            f"{len(self.council.chat.messages)} message(s), {reattached} AI seat(s) reattached "
            "as placeholders (swap in a real RemoteAPISeat client to reconnect for real)"
        )


def repl(council: Council) -> None:
    tui = CouncilTUI(council)
    print("One-Wave Council Chamber -- type 'help' for commands, 'quit' to leave.")
    while True:
        try:
            line = input("council> ")
        except EOFError:
            break
        try:
            output = tui.execute(line)
        except (UnknownCommandError, SeatNotFoundError, ValueError) as exc:
            print(f"error: {exc}")
            continue
        if output:
            print(output)
        if line.strip() in ("quit", "exit"):
            break


def demo_council(project_dir: Path) -> Council:
    """A Council with two MockSeat placeholders (ChatGPT, Codex) already
    open, against a real project directory -- the same honest setup as
    cli.py's scripted demo, but left for the person at the terminal to
    drive interactively instead of following a fixed script. Use `open
    <key>` at the prompt to add any other seat from SEAT_CATALOG (Claude,
    Gemini, DeepSeek, Grok, a local model) -- "the user opens only the
    seats needed for the current job." Real provider responses require
    registering a RemoteAPISeat with a real client instead; there are no
    provider API keys in this environment to wire up automatically."""
    project_dir.mkdir(parents=True, exist_ok=True)
    council = Council(CouncilChat(), PatchWorker(project_dir))
    open_catalog_seat(council, "chatgpt")
    open_catalog_seat(council, "codex")
    return council


def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    project_dir = Path(argv[0]) if argv else Path.cwd()
    repl(demo_council(project_dir))


if __name__ == "__main__":
    main()
