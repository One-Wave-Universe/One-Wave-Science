"""Persistent hear -> associate -> optionally respond loop for the Android brain."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import subprocess
from typing import Callable

from One_Wave_Bench.brain.cli import _cycle_receipt
from One_Wave_Bench.brain.command_memory import VerbalCommand
from One_Wave_Bench.brain.receipt_store import ReceiptStore


VOICE_PROGRAMS = ("espeak-ng", "espeak", "spd-say")


class SystemSpeaker:
    """Use an installed local voice; never send speech to a cloud service."""

    def __init__(self, *, enabled: bool = True):
        self.program = next((p for p in VOICE_PROGRAMS if shutil.which(p)), None)
        self.enabled = enabled

    @property
    def available(self) -> bool:
        return self.program is not None

    def say(self, text: str) -> None:
        print(f"Brain: {text}")
        if not self.enabled or self.program is None:
            return
        args = [self.program, text]
        if self.program == "spd-say":
            args = [self.program, "--wait", text]
        subprocess.run(args, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class ExperienceJournal:
    """Append observations without promoting every observation to knowledge."""

    def __init__(self, path: Path, *, association_threshold: int = 2):
        self.path = path
        self.association_threshold = association_threshold
        self.counts: Counter[tuple[str, VerbalCommand]] = Counter()
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                record = json.loads(line)
                if "followed_by" in record:
                    self.counts[(record["cue"], VerbalCommand(record["followed_by"]))] += 1

    def hear(self, cue: str) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"kind": "heard", "cue": cue}) + "\n")

    def observe(self, cue: str, followed_by: VerbalCommand) -> int:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"kind": "association", "cue": cue, "followed_by": followed_by.value}) + "\n")
        key = (cue, followed_by)
        self.counts[key] += 1
        return self.counts[key]


@dataclass(slots=True)
class LoopState:
    unresolved_cue: str | None = None
    last_command: VerbalCommand | None = None
    cycles: int = 0
    teachings: int = 0
    silent_cycles: int = 0


class ConversationLoop:
    """Hear continuously; learn repeated temporal relations; speech is optional."""

    def __init__(self, store: ReceiptStore, speaker: SystemSpeaker, *, responses: str = "changes", association_threshold: int = 2):
        if responses not in {"always", "changes", "never"}:
            raise ValueError("responses must be always, changes, or never")
        self.store = store
        self.speaker = speaker
        self.responses = responses
        self.journal = ExperienceJournal(store.path.with_name("experience.jsonl"), association_threshold=association_threshold)
        self.state = LoopState()

    def _learn_temporal_relation(self, command: VerbalCommand) -> None:
        phrase = self.state.unresolved_cue
        self.state.unresolved_cue = None
        if phrase is None:
            return
        count = self.journal.observe(phrase, command)
        if count < self.journal.association_threshold:
            return
        try:
            self.store.teach(phrase, command)
        except ValueError:
            return
        self.state.teachings += 1

    def _respond(self, command: VerbalCommand) -> None:
        previous = self.state.last_command
        should_speak = self.responses == "always"
        should_speak |= self.responses == "changes" and command is not previous
        should_speak |= self.responses != "never" and command is VerbalCommand.STOP
        self.state.last_command = command
        if should_speak:
            self.speaker.say(command.value.replace("_", " "))
        else:
            self.state.silent_cycles += 1

    def process(self, cue: str) -> bool:
        cue = cue.strip()
        if not cue:
            self.state.silent_cycles += 1
            return True
        if cue.lower() in {"quit", "exit", "goodbye"}:
            if self.responses != "never":
                self.speaker.say("Loop held. Memory saved.")
            return False
        self.journal.hear(cue)
        _, receipt = _cycle_receipt(self.store, cue)
        self.state.cycles += 1
        recall = receipt.recall
        if not recall.executable:
            self.state.unresolved_cue = cue
            self.state.silent_cycles += 1
            return True
        command = receipt.compressive_after.committed_command
        self._learn_temporal_relation(command)
        self._respond(command)
        return True

    def run(self, input_fn: Callable[[str], str] = input) -> LoopState:
        while True:
            try:
                cue = input_fn("")
            except (EOFError, KeyboardInterrupt):
                if self.responses != "never":
                    self.speaker.say("Loop held. Memory saved.")
                break
            if not self.process(cue):
                break
        return self.state
