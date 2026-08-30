"""Visible two-agent checkers world with pluggable controllers.

The environment does not reinforce, score, or teach strategy.
It only enforces checkers rules and exposes consequences.

Each plugin receives a grayscale raster of the visible board and the actions the
world currently accepts. After the move, it receives the new grayscale raster,
whether the action was accepted, whose turn follows, and whether the episode
ended. No reward values or strategic hints are supplied.

Learning belongs entirely inside the plugins.
"""

from __future__ import annotations

import random
import tkinter as tk
from dataclasses import dataclass
from typing import List, Optional, Protocol, Sequence, Tuple

BOARD = 8
CELL = 72
PAD = 16
STATUS_H = 112
DELAY_MS = 350
MAX_PLIES = 300

EMPTY = 0
BLACK = 1
BLACK_KING = 2
WHITE = -1
WHITE_KING = -2

Coord = Tuple[int, int]


@dataclass(frozen=True)
class Move:
    src: Coord
    dst: Coord
    captured: Optional[Coord] = None


@dataclass(frozen=True)
class WorldConsequence:
    accepted: bool
    before_pixels: Tuple[int, ...]
    after_pixels: Tuple[int, ...]
    actor_side: int
    next_side: int
    terminal: bool
    terminal_fact: str  # CONTINUE / BLACK_WIN / WHITE_WIN / DRAW / REJECTED
    move: Move


class AgentPlugin(Protocol):
    name: str

    def choose_move(
        self,
        grayscale: Sequence[int],
        width: int,
        height: int,
        side: int,
        legal_moves: Sequence[Move],
    ) -> Move:
        ...

    def observe(self, consequence: WorldConsequence) -> None:
        ...

    def reset_episode(self, side: int) -> None:
        ...


class RandomObserver:
    """Runnable placeholder plugin.

    It deliberately does not learn. Replace it with a mounted Field/Void/M4
    plugin that owns its own memory, prediction, error detection, and adaptation.
    """

    def __init__(self, name: str, seed: int) -> None:
        self.name = name
        self.rng = random.Random(seed)
        self.last_consequence: Optional[WorldConsequence] = None

    def reset_episode(self, side: int) -> None:
        self.last_consequence = None

    def choose_move(
        self,
        grayscale: Sequence[int],
        width: int,
        height: int,
        side: int,
        legal_moves: Sequence[Move],
    ) -> Move:
        if not legal_moves:
            raise RuntimeError("No legal moves")
        return self.rng.choice(list(legal_moves))

    def observe(self, consequence: WorldConsequence) -> None:
        self.last_consequence = consequence


class CheckersWorld:
    def __init__(self) -> None:
        self.board = [[EMPTY for _ in range(BOARD)] for _ in range(BOARD)]
        self.turn = BLACK
        self.ply = 0
        self.reset()

    def reset(self) -> None:
        self.board = [[EMPTY for _ in range(BOARD)] for _ in range(BOARD)]
        for r in range(3):
            for c in range(BOARD):
                if (r + c) % 2 == 1:
                    self.board[r][c] = WHITE
        for r in range(5, 8):
            for c in range(BOARD):
                if (r + c) % 2 == 1:
                    self.board[r][c] = BLACK
        self.turn = BLACK
        self.ply = 0

    @staticmethod
    def _inside(r: int, c: int) -> bool:
        return 0 <= r < BOARD and 0 <= c < BOARD

    @staticmethod
    def _belongs(piece: int, side: int) -> bool:
        return piece != EMPTY and (piece > 0) == (side > 0)

    @staticmethod
    def _enemy(piece: int, side: int) -> bool:
        return piece != EMPTY and (piece > 0) != (side > 0)

    @staticmethod
    def _dirs(piece: int) -> Sequence[Tuple[int, int]]:
        if abs(piece) == 2:
            return ((1, -1), (1, 1), (-1, -1), (-1, 1))
        return ((-1, -1), (-1, 1)) if piece > 0 else ((1, -1), (1, 1))

    def legal_moves(self, side: int) -> List[Move]:
        captures: List[Move] = []
        quiet: List[Move] = []
        for r in range(BOARD):
            for c in range(BOARD):
                piece = self.board[r][c]
                if not self._belongs(piece, side):
                    continue
                for dr, dc in self._dirs(piece):
                    r1, c1 = r + dr, c + dc
                    if self._inside(r1, c1) and self.board[r1][c1] == EMPTY:
                        quiet.append(Move((r, c), (r1, c1)))
                    r2, c2 = r + 2 * dr, c + 2 * dc
                    if (
                        self._inside(r2, c2)
                        and self._inside(r1, c1)
                        and self._enemy(self.board[r1][c1], side)
                        and self.board[r2][c2] == EMPTY
                    ):
                        captures.append(Move((r, c), (r2, c2), (r1, c1)))
        return captures if captures else quiet

    def apply(self, move: Move) -> Tuple[bool, str]:
        legal = self.legal_moves(self.turn)
        if move not in legal:
            return False, "REJECTED"

        sr, sc = move.src
        dr, dc = move.dst
        piece = self.board[sr][sc]
        self.board[sr][sc] = EMPTY

        if move.captured is not None:
            cr, cc = move.captured
            self.board[cr][cc] = EMPTY

        if piece == BLACK and dr == 0:
            piece = BLACK_KING
        elif piece == WHITE and dr == BOARD - 1:
            piece = WHITE_KING

        self.board[dr][dc] = piece
        self.ply += 1
        actor = self.turn
        self.turn = -self.turn

        if not self.legal_moves(self.turn):
            return True, "BLACK_WIN" if actor == BLACK else "WHITE_WIN"
        if self.ply >= MAX_PLIES:
            return True, "DRAW"
        return True, "CONTINUE"


class CheckersApp:
    def __init__(self, black_agent: AgentPlugin, white_agent: AgentPlugin) -> None:
        self.world = CheckersWorld()
        self.agents = {BLACK: black_agent, WHITE: white_agent}
        self.running = False
        self.game_number = 1

        self.root = tk.Tk()
        self.root.title("One-Wave Two-State Checkers Lab")
        width = BOARD * CELL + 2 * PAD
        height = BOARD * CELL + 2 * PAD + STATUS_H
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="#202020")
        self.canvas.pack()

        controls = tk.Frame(self.root)
        controls.pack(fill="x")
        tk.Button(controls, text="Start", command=self.start).pack(side="left")
        tk.Button(controls, text="Pause", command=self.pause).pack(side="left")
        tk.Button(controls, text="Reset", command=self.reset).pack(side="left")

        for side, agent in self.agents.items():
            agent.reset_episode(side)
        self.draw()

    def grayscale_pixels(self) -> Tuple[int, ...]:
        values: List[int] = []
        for r in range(BOARD):
            for py in range(CELL):
                for c in range(BOARD):
                    square = 74 if (r + c) % 2 else 190
                    piece = self.world.board[r][c]
                    for px in range(CELL):
                        cx = px - CELL / 2
                        cy = py - CELL / 2
                        if piece != EMPTY and cx * cx + cy * cy < (CELL * 0.31) ** 2:
                            values.append(35 if piece > 0 else 225)
                        elif abs(piece) == 2 and cx * cx + cy * cy < (CELL * 0.13) ** 2:
                            values.append(130)
                        else:
                            values.append(square)
        return tuple(values)

    def draw(self) -> None:
        self.canvas.delete("all")
        for r in range(BOARD):
            for c in range(BOARD):
                x0 = PAD + c * CELL
                y0 = PAD + r * CELL
                x1 = x0 + CELL
                y1 = y0 + CELL
                shade = "#bdbdbd" if (r + c) % 2 == 0 else "#4a4a4a"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=shade, outline=shade)
                piece = self.world.board[r][c]
                if piece:
                    fill = "#202020" if piece > 0 else "#eeeeee"
                    outline = "#d0d0d0" if piece > 0 else "#303030"
                    inset = 13
                    self.canvas.create_oval(x0 + inset, y0 + inset, x1 - inset, y1 - inset,
                                            fill=fill, outline=outline, width=3)
                    if abs(piece) == 2:
                        self.canvas.create_oval(x0 + 27, y0 + 27, x1 - 27, y1 - 27,
                                                fill="#808080", outline="#808080")

        black = self.agents[BLACK].name
        white = self.agents[WHITE].name
        turn_name = black if self.world.turn == BLACK else white
        status_y = PAD + BOARD * CELL + 22
        self.canvas.create_text(PAD, status_y, anchor="w", fill="white",
                                text=f"Game {self.game_number}   Ply {self.world.ply}   Turn: {turn_name}")
        self.canvas.create_text(PAD, status_y + 28, anchor="w", fill="#cfcfcf",
                                text=f"BLACK: {black}     WHITE: {white}")
        self.canvas.create_text(PAD, status_y + 56, anchor="w", fill="#a9a9a9",
                                text="World supplies consequences only. Learning lives inside each plugin.")

    def start(self) -> None:
        if not self.running:
            self.running = True
            self.root.after(50, self.step)

    def pause(self) -> None:
        self.running = False

    def reset(self) -> None:
        self.running = False
        self.world.reset()
        self.game_number += 1
        for side, agent in self.agents.items():
            agent.reset_episode(side)
        self.draw()

    def step(self) -> None:
        if not self.running:
            return

        side = self.world.turn
        agent = self.agents[side]
        legal = self.world.legal_moves(side)
        if not legal:
            self.reset()
            return

        before = self.grayscale_pixels()
        move = agent.choose_move(before, BOARD * CELL, BOARD * CELL, side, legal)
        accepted, fact = self.world.apply(move)
        after = self.grayscale_pixels()
        terminal = fact != "CONTINUE"

        consequence = WorldConsequence(
            accepted=accepted,
            before_pixels=before,
            after_pixels=after,
            actor_side=side,
            next_side=self.world.turn,
            terminal=terminal,
            terminal_fact=fact,
            move=move,
        )
        agent.observe(consequence)
        self.draw()

        if terminal:
            self.running = False
            self.canvas.create_text(
                PAD + BOARD * CELL / 2,
                PAD + BOARD * CELL / 2,
                text=fact.replace("_", " "),
                fill="white",
                font=("TkDefaultFont", 28, "bold"),
            )
            return

        self.root.after(DELAY_MS, self.step)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = CheckersApp(
        black_agent=RandomObserver("BLACK PLUGIN", seed=1),
        white_agent=RandomObserver("WHITE PLUGIN", seed=2),
    )
    app.run()


if __name__ == "__main__":
    main()
