"""First runnable vertical slice of the mounted Field/Void architecture.

Purpose:
- keep one instance small enough to inspect;
- let M4 route memory and build the shared active world;
- let Field ask about that world;
- let Void answer/check it;
- update memory/reference from the result;
- emit a receipt for every cycle.

This is an architecture probe, not a claim that these toy semantics are final.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List
import json


@dataclass
class MemoryItem:
    key: str
    value: str
    weight: float = 1.0


@dataclass
class ActiveWorld:
    cue: str
    reference: str
    recalled: List[MemoryItem] = field(default_factory=list)
    question: str = ""
    answer: str = ""
    status: str = "OPEN"


@dataclass
class CycleReceipt:
    cycle: int
    cue: str
    reference_before: str
    recalled_keys: List[str]
    field_question: str
    void_answer: str
    resolution: str
    reference_after: str
    world: Dict[str, Any]


class TinyMemory:
    def __init__(self) -> None:
        self.items: Dict[str, MemoryItem] = {
            "go": MemoryItem("go", "movement requested"),
            "stop": MemoryItem("stop", "inhibit movement"),
            "unknown": MemoryItem("unknown", "insufficient certainty"),
        }

    def recall(self, cue: str) -> List[MemoryItem]:
        text = cue.lower()
        hits = [item for key, item in self.items.items() if key in text]
        return hits

    def store(self, key: str, value: str) -> None:
        self.items[key] = MemoryItem(key, value)


class M4:
    """Memory router plus active-world constructor/maintainer."""

    def __init__(self, memory: TinyMemory) -> None:
        self.memory = memory

    def build_world(self, cue: str, reference: str) -> ActiveWorld:
        return ActiveWorld(
            cue=cue,
            reference=reference,
            recalled=self.memory.recall(cue),
        )

    def integrate_answer(self, world: ActiveWorld, answer: str, resolution: str) -> None:
        world.answer = answer
        world.status = resolution


class Field:
    """Inquiry/expansion side: asks what the active world implies."""

    def ask(self, world: ActiveWorld) -> str:
        memory_text = ", ".join(item.value for item in world.recalled) or "no matching memory"
        question = (
            f"Given cue={world.cue!r}, reference={world.reference!r}, "
            f"memory=[{memory_text}], what should change?"
        )
        world.question = question
        return question


class Void:
    """Answering/checking/compression side."""

    def answer(self, world: ActiveWorld) -> tuple[str, str]:
        text = world.cue.lower()
        if "stop" in text:
            return "DENY", "preserve reference and inhibit action"
        if "unknown" in text or not world.recalled:
            return "DEFER", "hold current reference pending more information"
        return "CONFIRM", "accept bounded change from current reference"


class MountedLoopDemo:
    def __init__(self) -> None:
        self.memory = TinyMemory()
        self.m4 = M4(self.memory)
        self.field = Field()
        self.void = Void()
        self.reference = "CENTER"
        self.cycle_count = 0

    def cycle(self, cue: str) -> CycleReceipt:
        self.cycle_count += 1
        before = self.reference

        world = self.m4.build_world(cue, before)
        question = self.field.ask(world)
        resolution, answer = self.void.answer(world)
        self.m4.integrate_answer(world, answer, resolution)

        if resolution == "CONFIRM":
            self.reference = f"CONFIRMED:{cue.strip().lower()}"
            self.memory.store(f"cycle-{self.cycle_count}", self.reference)
        elif resolution == "DENY":
            self.reference = before
        else:
            self.reference = before

        return CycleReceipt(
            cycle=self.cycle_count,
            cue=cue,
            reference_before=before,
            recalled_keys=[item.key for item in world.recalled],
            field_question=question,
            void_answer=answer,
            resolution=resolution,
            reference_after=self.reference,
            world=asdict(world),
        )


def main() -> None:
    loop = MountedLoopDemo()
    for cue in ("go forward", "unknown signal", "stop", "go again"):
        print(json.dumps(asdict(loop.cycle(cue)), indent=2))


if __name__ == "__main__":
    main()
