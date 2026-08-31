"""Two mounted checkers learners built as two state machines plus one M4 loop.

Both variants receive grayscale pixels only and learn from direct consequences.
They share the same architecture:

    M4 builds/maintains ActiveWorld and routes memory
    -> Field state machine generates possibilities
    -> M4 routes candidates
    -> Void state machine checks against remembered consequences
    -> action
    -> world consequence
    -> M4 updates memory

The experimental variable is Field/Void balance, not game knowledge.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Sequence, Tuple

try:
    from .checkers_contract import Move, WorldConsequence
except ImportError:
    from checkers_contract import Move, WorldConsequence

BOARD = 8
Coord = Tuple[int, int]


@dataclass
class Experience:
    attempts: int = 0
    accepted: int = 0
    rejected: int = 0
    terminal_losses: int = 0


@dataclass
class ActiveWorld:
    side: int
    cells: Tuple[int, ...]
    signature: Tuple[int, ...]


class FieldState(str, Enum):
    IDLE = "IDLE"
    EXPAND = "EXPAND"
    PROPOSE = "PROPOSE"
    HANDOFF = "HANDOFF"


class VoidState(str, Enum):
    IDLE = "IDLE"
    CHECK = "CHECK"
    CONFIRM = "CONFIRM"
    DEFER = "DEFER"
    DENY = "DENY"


class FieldStateMachine:
    """Inquiry/expansion machine. It knows no checkers legality rules."""

    def __init__(self, rng: random.Random, candidate_budget: int) -> None:
        self.rng = rng
        self.candidate_budget = candidate_budget
        self.state = FieldState.IDLE

    def generate(self, world: ActiveWorld) -> List[Move]:
        self.state = FieldState.EXPAND
        candidates: List[Move] = []
        for _ in range(self.candidate_budget):
            sr = self.rng.randrange(BOARD)
            sc = self.rng.randrange(BOARD)
            dr = sr + self.rng.choice((-2, -1, 1, 2))
            dc = sc + self.rng.choice((-2, -1, 1, 2))
            candidates.append(Move((sr, sc), (dr, dc)))
        self.state = FieldState.PROPOSE
        self.state = FieldState.HANDOFF
        return candidates

    def reset_local(self) -> None:
        self.state = FieldState.IDLE


class VoidStateMachine:
    """Answer/check machine using memory of consequences, not hidden rules."""

    def __init__(self, rng: random.Random, rejection_strength: int) -> None:
        self.rng = rng
        self.rejection_strength = rejection_strength
        self.state = VoidState.IDLE

    def choose(
        self,
        world: ActiveWorld,
        candidates: List[Move],
        recall,
    ) -> Move:
        self.state = VoidState.CHECK
        scored: List[Tuple[int, int, Move]] = []
        for move in candidates:
            exp: Experience = recall(world, move)
            rejection_pressure = (
                exp.rejected * self.rejection_strength
                + exp.terminal_losses * self.rejection_strength
            )
            continuity = exp.accepted
            scored.append((rejection_pressure, -continuity, move))

        best_pressure = min(item[0] for item in scored)
        survivors = [item for item in scored if item[0] == best_pressure]
        best_continuity = min(item[1] for item in survivors)
        finalists = [item[2] for item in survivors if item[1] == best_continuity]

        if best_pressure > 0:
            self.state = VoidState.DEFER
        else:
            self.state = VoidState.CONFIRM
        return self.rng.choice(finalists)

    def reset_local(self) -> None:
        self.state = VoidState.IDLE


class M4Loop:
    """The single loop: memory router plus active-world constructor/maintainer."""

    def __init__(self) -> None:
        self.memory: Dict[Tuple[Tuple[int, ...], Move], Experience] = {}
        self.last_world: ActiveWorld | None = None
        self.last_move: Move | None = None
        self.cycles = 0

    @staticmethod
    def _sample_cell(
        grayscale: Sequence[int], width: int, height: int, row: int, col: int
    ) -> int:
        cell_w = width // BOARD
        cell_h = height // BOARD
        x = min(width - 1, col * cell_w + cell_w // 2)
        y = min(height - 1, row * cell_h + cell_h // 2)
        return int(grayscale[y * width + x])

    def build_world(
        self, grayscale: Sequence[int], width: int, height: int, side: int
    ) -> ActiveWorld:
        self.cycles += 1
        cells = tuple(
            self._sample_cell(grayscale, width, height, r, c)
            for r in range(BOARD)
            for c in range(BOARD)
        )
        signature = tuple(v // 32 for v in cells)
        world = ActiveWorld(side=side, cells=cells, signature=signature)
        self.last_world = world
        return world

    def route_field_to_void(self, candidates: List[Move]) -> List[Move]:
        return candidates

    def recall(self, world: ActiveWorld, move: Move) -> Experience:
        return self.memory.get((world.signature, move), Experience())

    def remember(self, consequence: WorldConsequence) -> None:
        if self.last_world is None or self.last_move is None:
            return
        key = (self.last_world.signature, self.last_move)
        exp = self.memory.setdefault(key, Experience())
        exp.attempts += 1
        if consequence.accepted:
            exp.accepted += 1
        else:
            exp.rejected += 1
        if consequence.terminal and not consequence.accepted:
            exp.terminal_losses += 1


class MountedCheckersAgent:
    def __init__(
        self,
        name: str,
        *,
        seed: int,
        field_candidates: int,
        void_rejection_strength: int,
    ) -> None:
        self.name = name
        self.rng = random.Random(seed)
        self.m4 = M4Loop()
        self.field = FieldStateMachine(self.rng, field_candidates)
        self.void = VoidStateMachine(self.rng, void_rejection_strength)
        self.games_seen = 0

    def reset_episode(self, side: int) -> None:
        self.games_seen += 1
        self.m4.last_world = None
        self.m4.last_move = None
        self.field.reset_local()
        self.void.reset_local()

    def choose_move(
        self,
        grayscale: Sequence[int],
        width: int,
        height: int,
        side: int,
    ) -> Move:
        world = self.m4.build_world(grayscale, width, height, side)
        candidates = self.field.generate(world)
        routed = self.m4.route_field_to_void(candidates)
        move = self.void.choose(world, routed, self.m4.recall)
        self.m4.last_move = move
        return move

    def observe(self, consequence: WorldConsequence) -> None:
        self.m4.remember(consequence)
        self.field.reset_local()
        if consequence.accepted:
            self.void.state = VoidState.CONFIRM
        elif consequence.terminal:
            self.void.state = VoidState.DENY
        else:
            self.void.state = VoidState.DEFER


class FieldHeavyAgent(MountedCheckersAgent):
    def __init__(self, name: str = "FIELD-HEAVY", seed: int = 11) -> None:
        super().__init__(
            name,
            seed=seed,
            field_candidates=18,
            void_rejection_strength=1,
        )


class VoidHeavyAgent(MountedCheckersAgent):
    def __init__(self, name: str = "VOID-HEAVY", seed: int = 29) -> None:
        super().__init__(
            name,
            seed=seed,
            field_candidates=6,
            void_rejection_strength=4,
        )
