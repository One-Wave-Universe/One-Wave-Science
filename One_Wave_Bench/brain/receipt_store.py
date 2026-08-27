"""Persistent append-only command teaching receipts."""

from __future__ import annotations

import fcntl
import os
from pathlib import Path

from One_Wave_Bench.brain.command_memory import CommandMemory, DEFAULT_PHRASES


class ReceiptStore:
    def __init__(self, path: Path):
        self.path = Path(path)

    def initialize(self) -> CommandMemory:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists() and self.path.stat().st_size:
            return self.load()
        memory = CommandMemory.defaults()
        self.path.touch(mode=0o600, exist_ok=True)
        os.chmod(self.path, 0o600)
        with self.path.open("a", encoding="utf-8") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            for receipt in memory.receipts:
                stream.write(receipt.to_json() + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        return memory

    def load(self) -> CommandMemory:
        if not self.path.exists():
            raise FileNotFoundError(self.path)
        with self.path.open("r", encoding="utf-8") as stream:
            fcntl.flock(stream, fcntl.LOCK_SH)
            lines = [line.rstrip("\n") for line in stream if line.strip()]
        return CommandMemory.rebuild(lines)

    def teach(self, phrase: str, command) -> CommandMemory:
        self.initialize()
        with self.path.open("r+", encoding="utf-8") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            lines = [line.rstrip("\n") for line in stream if line.strip()]
            memory = CommandMemory.rebuild(lines)
            receipt = memory.teach(phrase, command)
            stream.seek(0, os.SEEK_END)
            stream.write(receipt.to_json() + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        return memory


def default_phrase_count() -> int:
    return sum(len(phrases) for phrases in DEFAULT_PHRASES.values())
