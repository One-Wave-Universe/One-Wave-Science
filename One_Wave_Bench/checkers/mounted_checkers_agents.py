"""Two mounted checkers learners: Field-heavy and Void-heavy.

Both agents:
- receive grayscale pixels only;
- reconstruct a coarse active world from those pixels;
- generate candidate moves internally;
- remember attempted moves and their observed consequences;
- use the same M4 memory/active-world loop;
- receive no legal-move list and no strategy reward.

The experimental variable is only Field/Void balance.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
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


class M4Loop:
    """Memory router and active-world constructor shared by both variants."""

    def __init__(self) -> None:
        self.memory: Dict[Tuple[Tuple[int, ...], Move], Experience] = {}
        self.last_world: ActiveWorld | None = None
        self.last_move: Move | None = None

    @staticmethod
    def _sample_cell(
        grayscale: Sequence[int], width: int, height: int, row: int, col: int
    ) -> int:
        cell_w = width // BOARD
        cell_h = height // BOARD
        # Sample the center of each square. The checkers renderer puts the piece
        # body through this region, so this remains perception from pixels rather
        # than access to the symbolic board.
        x = min(width - 1, col * cell_w + cell_w // 2)
        y = min(height - 1, row * cell_h + cell_h // 2)
        return int(grayscale[y * width + x])

    def build_world(
        self, grayscale: Sequence[int], width: int, height: int, side: int
    ) -> ActiveWorld:
        cells = tuple(
            self._sample_cell(grayscale, width, height, r, c)
            for r in range(BOARD)
            for c in range(BOARD)
        )
        # Coarse signature keeps learned consequences tied to visually similar
        # states without handing the agent symbolic piece labels.
        signature = tuple(v // 32 for v in cells)
        world = ActiveWorld(side=side, cells=cells, signature=signature)
        self.last_world = world
        return world

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
        self.field_candidates = field_candidates
        self.void_rejection_strength = void_rejection_strength
        self.games_seen = 0

    def reset_episode(self, side: int) -> None:
        self.games_seen += 1
        # Long-term consequence memory deliberately survives episode boundaries.
        self.m4.last_world = None
        self.m4.last_move = None

    @staticmethod
    def _candidate() -> Move:
        raise RuntimeError("instance method required")

    def _field_generate(self) -> List[Move]:
        """Field generates possibilities without being told checkers legality."""
        candidates: List[Move] = []
        for _ in range(self.field_candidates):
            sr = self.rng.randrange(BOARD)
            sc = self.rng.randrange(BOARD)
            # Candidate motion is intentionally broad enough to make mistakes.
            dr = sr + self.rng.choice((-2, -1, 1, 2))
            dc = sc + self.rng.choice((-2, -1, 1, 2))
            candidates.append(Move((sr, sc), (dr, dc)))
        return candidates

    def _void_choose(self, world: ActiveWorld, candidates: List[Move]) -> Move:
        """Void checks only remembered consequences, not hidden game rules."""
        scored: List[Tuple[int, int, Move]] = []
        for move in candidates:
            exp = self.m4.recall(world, move)
            # No externally supplied reward. This is memory of direct world
            # consequences: rejected attempts count as reasons to distrust a move.
            rejection_pressure = (
                exp.rejected * self.void_rejection_strength
                + exp.terminal_losses * self.void_rejection_strength
            )
            continuity = exp.accepted
            scored.append((rejection_pressure, -continuity, move))

        best_pressure = min(item[0] for item in scored)
        survivors = [item for item in scored if item[0] == best_pressure]
        best_continuity = min(item[1] for item in survivors)
        finalists = [item[2] for item in survivors if item[1] == best_continuity]
        return self.rng.choice(finalists)

    def choose_move(
        self,
        grayscale: Sequence[int],
        width: int,
        height: int,
        side: int,
    ) -> Move:
        world = self.m4.build_world(grayscale, width, height, side)
        candidates = self._field_generate()
        move = self._void_choose(world, candidates)
        self.m4.last_move = move
        return move

    def observe(self, consequence: WorldConsequence) -> None:
        self.m4.remember(consequence)


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
