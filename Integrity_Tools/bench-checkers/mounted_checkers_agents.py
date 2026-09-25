"""Mounted checkers learners with a grayscale Micro receptor layer.

The agents receive only the grayscale framebuffer and direct consequences.
No symbolic board, legal-move list, piece identity, or checkers movement rule is
provided to the learners.

Current experimental stack:

    grayscale framebuffer
    -> Micro receptor-cell workers (local light transduction)
    -> M4 repeating loop / continuity and memory routing
    -> Field state machine proposes an action
    -> Void state machine checks remembered consequences
    -> attempted move
    -> world consequence
    -> memory update
    -> repeat

Micro is deliberately small and local: each receptor sees only a tiny patch of
light and emits an activation.  It does not know what a square or checker is.
The next scale can later be mounted between Micro and the Field/Void loop
without changing the environment contract.
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

# The receptor sheet is intentionally independent of the 8x8 game board.
# It is simply a regular sensory sheet laid over the incoming framebuffer.
MICRO_ROWS = 16
MICRO_COLS = 16


@dataclass(frozen=True)
class ReceptorSignal:
    """One Micro worker's local grayscale transduction."""

    index: int
    intensity: int
    activation: int
    delta: int


class GrayscaleReceptorCell:
    """Micro worker: local grayscale in -> compact nerve-like activation out."""

    def __init__(self, index: int) -> None:
        self.index = index
        self.previous_intensity: int | None = None

    def sense(self, intensity: int) -> ReceptorSignal:
        intensity = max(0, min(255, int(intensity)))
        # Five coarse response bands.  They are sensory response levels, not
        # semantic labels and carry no board/game meaning.
        activation = min(4, intensity // 52)
        delta = 0 if self.previous_intensity is None else intensity - self.previous_intensity
        self.previous_intensity = intensity
        return ReceptorSignal(self.index, intensity, activation, delta)


class MicroReceptorSheet:
    """A 2-D sheet of independent grayscale receptor-cell workers."""

    def __init__(self, rows: int = MICRO_ROWS, cols: int = MICRO_COLS) -> None:
        self.rows = rows
        self.cols = cols
        self.cells = [GrayscaleReceptorCell(i) for i in range(rows * cols)]

    @staticmethod
    def _patch_mean(
        grayscale: Sequence[int],
        width: int,
        height: int,
        r0: int,
        r1: int,
        c0: int,
        c1: int,
    ) -> int:
        total = 0
        count = 0
        for y in range(r0, max(r0 + 1, r1)):
            base = y * width
            for x in range(c0, max(c0 + 1, c1)):
                total += int(grayscale[base + x])
                count += 1
        return total // max(1, count)

    def receive(
        self, grayscale: Sequence[int], width: int, height: int
    ) -> Tuple[ReceptorSignal, ...]:
        if width <= 0 or height <= 0 or len(grayscale) < width * height:
            raise ValueError("invalid grayscale framebuffer")

        signals: List[ReceptorSignal] = []
        for rr in range(self.rows):
            y0 = rr * height // self.rows
            y1 = (rr + 1) * height // self.rows
            for cc in range(self.cols):
                x0 = cc * width // self.cols
                x1 = (cc + 1) * width // self.cols
                intensity = self._patch_mean(grayscale, width, height, y0, y1, x0, x1)
                cell = self.cells[rr * self.cols + cc]
                signals.append(cell.sense(intensity))
        return tuple(signals)


@dataclass
class Experience:
    attempts: int = 0
    accepted: int = 0
    rejected: int = 0
    terminal_losses: int = 0


@dataclass
class ActiveWorld:
    side: int
    micro_signals: Tuple[ReceptorSignal, ...]
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
    """Inquiry/expansion half. It knows no checkers legality rules."""

    def __init__(self, rng: random.Random, candidate_budget: int) -> None:
        self.rng = rng
        self.candidate_budget = candidate_budget
        self.state = FieldState.IDLE

    def generate(self, world: ActiveWorld) -> List[Move]:
        self.state = FieldState.EXPAND
        candidates: List[Move] = []
        for _ in range(self.candidate_budget):
            # Deliberately arbitrary source/destination coordinates.  Do not
            # smuggle diagonal/checkers movement geometry into the learner.
            sr = self.rng.randrange(BOARD)
            sc = self.rng.randrange(BOARD)
            dr = self.rng.randrange(BOARD)
            dc = self.rng.randrange(BOARD)
            candidates.append(Move((sr, sc), (dr, dc)))
        self.state = FieldState.PROPOSE
        self.state = FieldState.HANDOFF
        return candidates

    def reset_local(self) -> None:
        self.state = FieldState.IDLE


class VoidStateMachine:
    """Answer/check half using remembered consequences, never hidden rules."""

    def __init__(self, rng: random.Random, rejection_strength: int) -> None:
        self.rng = rng
        self.rejection_strength = rejection_strength
        self.state = VoidState.IDLE

    def choose(self, world: ActiveWorld, candidates: List[Move], recall) -> Move:
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

        self.state = VoidState.DEFER if best_pressure > 0 else VoidState.CONFIRM
        return self.rng.choice(finalists)

    def reset_local(self) -> None:
        self.state = VoidState.IDLE


class M4Loop:
    """Repeating continuity loop: active state plus consequence-memory routing."""

    def __init__(self) -> None:
        self.memory: Dict[Tuple[Tuple[int, ...], Move], Experience] = {}
        self.last_world: ActiveWorld | None = None
        self.last_move: Move | None = None
        self.cycles = 0

    def build_world(self, micro_signals: Tuple[ReceptorSignal, ...], side: int) -> ActiveWorld:
        self.cycles += 1
        # The memory signature is built only from Micro activations and local
        # change direction.  No symbolic board reconstruction occurs here.
        signature = tuple(
            (signal.activation * 3) + (1 if signal.delta > 0 else -1 if signal.delta < 0 else 0)
            for signal in micro_signals
        )
        world = ActiveWorld(side=side, micro_signals=micro_signals, signature=signature)
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
        self.micro = MicroReceptorSheet()
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
        micro_signals = self.micro.receive(grayscale, width, height)
        world = self.m4.build_world(micro_signals, side)
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
