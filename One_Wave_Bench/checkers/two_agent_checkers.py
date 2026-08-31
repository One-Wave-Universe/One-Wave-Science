"""Visible two-agent checkers world with pluggable controllers.

The environment is deliberately dumb reality:
- it renders a grayscale board;
- each plugin sees pixels, not a symbolic board or legal-move list;
- each plugin attempts any source/destination move it chooses;
- legal moves change the world;
- an illegal move is an immediate loss;
- games restart automatically while running;
- the world supplies no strategy reward, hints, or correction.

This makes stale attention costly without hard-coding an "attention penalty".
If a plugin keeps acting from an old internal world, it can repeat the same bad
assumption across games and trap itself in a consequence loop until its own
memory/ActiveWorld changes.

Learning belongs entirely inside the plugins. reset_episode() marks an episode
boundary; it must not be treated as an instruction to erase learned memory.
"""

from __future__ import annotations

import random
import tkinter as tk
from dataclasses import dataclass
from typing import List, Optional, Protocol, Sequence, Tuple

BOARD = 8
CELL = 72
PAD = 16
STATUS_H = 132
DELAY_MS = 350
TERMINAL_PAUSE_MS = 1000
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


@dataclass(frozen=True)
class WorldConsequence:
    accepted: bool
    before_pixels: Tuple[int, ...]
    after_pixels: Tuple[int, ...]
    actor_side: int
    next_side: int
    terminal: bool
    terminal_fact: str  # CONTINUE / BLACK_WIN / WHITE_WIN / DRAW
    move: Move


class AgentPlugin(Protocol):
    name: str

    def choose_move(
        self,
        grayscale: Sequence[int],
        width: int,
        height: int,
        side: int,
    ) -> Move:
        """Choose from pixels only. No symbolic board or legal-move list."""
        ...

    def observe(self, consequence: WorldConsequence) -> None:
        """Observe what actually happened. The plugin decides what it means."""
        ...

    def reset_episode(self, side: int) -> None:
        """Episode boundary only; learned memory may persist."""
        ...


class RandomPixelActor:
    """Non-learning smoke-test plugin.

    It proves the environment really permits mistakes: it guesses a source and
    diagonal destination without access to the board model or legal moves.
    Replace this with a mounted Field/Void/M4 learner.
    """

    def __init__(self, name: str, seed: int) -> None:
        self.name = name
        self.rng = random.Random(seed)
        self.games_seen = 0
        self.last_consequence: Optional[WorldConsequence] = None

    def reset_episode(self, side: int) -> None:
        self.games_seen += 1
        # Deliberately preserve learned/long-term state across games.
        self.last_consequence = None

    def choose_move(
        self,
        grayscale: Sequence[int],
        width: int,
        height: int,
        side: int,
    ) -> Move:
        sr = self.rng.randrange(BOARD)
        sc = self.rng.randrange(BOARD)
        dr = sr + self.rng.choice((-1, 1, -2, 2))
        dc = sc + self.rng.choice((-1, 1, -2, 2))
        return Move((sr, sc), (dr, dc))

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

    def legal_moves(self, side: int) -> List[Tuple[Move, Optional[Coord]]]:
        captures: List[Tuple[Move, Optional[Coord]]] = []
        quiet: List[Tuple[Move, Optional[Coord]]] = []
        for r in range(BOARD):
            for c in range(BOARD):
                piece = self.board[r][c]
                if not self._belongs(piece, side):
                    continue
                for dr, dc in self._dirs(piece):
                    r1, c1 = r + dr, c + dc
                    if self._inside(r1, c1) and self.board[r1][c1] == EMPTY:
                        quiet.append((Move((r, c), (r1, c1)), None))
                    r2, c2 = r + 2 * dr, c + 2 * dc
                    if (
                        self._inside(r2, c2)
                        and self._inside(r1, c1)
                        and self._enemy(self.board[r1][c1], side)
                        and self.board[r2][c2] == EMPTY
                    ):
                        captures.append((Move((r, c), (r2, c2)), (r1, c1)))
        return captures if captures else quiet

    def apply(self, move: Move) -> Tuple[bool, str]:
        actor = self.turn
        legal = self.legal_moves(actor)
        match = next(((m, captured) for m, captured in legal if m == move), None)
        if match is None:
            winner = WHITE if actor == BLACK else BLACK
            return False, "BLACK_WIN" if winner == BLACK else "WHITE_WIN"

        _, captured = match
        sr, sc = move.src
        dr, dc = move.dst
        piece = self.board[sr][sc]
        self.board[sr][sc] = EMPTY

        if captured is not None:
            cr, cc = captured
            self.board[cr][cc] = EMPTY

        if piece == BLACK and dr == 0:
            piece = BLACK_KING
        elif piece == WHITE and dr == BOARD - 1:
            piece = WHITE_KING

        self.board[dr][dc] = piece
        self.ply += 1
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
        self.last_terminal = ""
        self.loss_streak = {BLACK: 0, WHITE: 0}

        self.root = tk.Tk()
        self.root.title("One-Wave Vision Checkers Lab")
        width = BOARD * CELL + 2 * PAD
        height = BOARD * CELL + 2 * PAD + STATUS_H
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="#202020")
        self.canvas.pack()

        controls = tk.Frame(self.root)
        controls.pack(fill="x")
        tk.Button(controls, text="Start", command=self.start).pack(side="left")
        tk.Button(controls, text="Pause", command=self.pause).pack(side="left")
        tk.Button(controls, text="New Game", command=self.manual_new_game).pack(side="left")

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
                        radius2 = cx * cx + cy * cy
                        if abs(piece) == 2 and radius2 < (CELL * 0.13) ** 2:
                            values.append(130)
                        elif piece != EMPTY and radius2 < (CELL * 0.31) ** 2:
                            values.append(35 if piece > 0 else 225)
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
                    self.canvas.create_oval(
                        x0 + inset, y0 + inset, x1 - inset, y1 - inset,
                        fill=fill, outline=outline, width=3,
                    )
                    if abs(piece) == 2:
                        self.canvas.create_oval(
                            x0 + 27, y0 + 27, x1 - 27, y1 - 27,
                            fill="#808080", outline="#808080",
                        )

        black = self.agents[BLACK].name
        white = self.agents[WHITE].name
        turn_name = black if self.world.turn == BLACK else white
        status_y = PAD + BOARD * CELL + 20
        self.canvas.create_text(
            PAD, status_y, anchor="w", fill="white",
            text=f"Game {self.game_number}   Ply {self.world.ply}   Turn: {turn_name}",
        )
        self.canvas.create_text(
            PAD, status_y + 26, anchor="w", fill="#cfcfcf",
            text=f"BLACK: {black}     WHITE: {white}",
        )
        self.canvas.create_text(
            PAD, status_y + 52, anchor="w", fill="#a9a9a9",
            text="Pixels in. Any move out. Illegal move = immediate loss. No legal-move hints.",
        )
        self.canvas.create_text(
            PAD, status_y + 78, anchor="w", fill="#8f8f8f",
            text=(f"Loss streaks — black {self.loss_streak[BLACK]} / white {self.loss_streak[WHITE]}"
                  + (f"   Last: {self.last_terminal}" if self.last_terminal else "")),
        )

    def start(self) -> None:
        if not self.running:
            self.running = True
            self.root.after(50, self.step)

    def pause(self) -> None:
        self.running = False

    def _begin_next_game(self) -> None:
        self.world.reset()
        self.game_number += 1
        for side, agent in self.agents.items():
            agent.reset_episode(side)
        self.draw()
        if self.running:
            self.root.after(DELAY_MS, self.step)

    def manual_new_game(self) -> None:
        self._begin_next_game()

    def step(self) -> None:
        if not self.running:
            return

        side = self.world.turn
        agent = self.agents[side]
        before = self.grayscale_pixels()
        move = agent.choose_move(before, BOARD * CELL, BOARD * CELL, side)
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

        if terminal:
            winner = BLACK if fact == "BLACK_WIN" else WHITE if fact == "WHITE_WIN" else 0
            if winner:
                loser = -winner
                self.loss_streak[loser] += 1
                self.loss_streak[winner] = 0
            self.last_terminal = ("WRONG MOVE — " if not accepted else "") + fact.replace("_", " ")

        self.draw()

        if terminal:
            self.canvas.create_text(
                PAD + BOARD * CELL / 2,
                PAD + BOARD * CELL / 2,
                text=self.last_terminal,
                fill="white",
                font=("TkDefaultFont", 28, "bold"),
            )
            if self.running:
                self.root.after(TERMINAL_PAUSE_MS, self._begin_next_game)
            return

        self.root.after(DELAY_MS, self.step)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = CheckersApp(
        black_agent=RandomPixelActor("BLACK PLUGIN", seed=1),
        white_agent=RandomPixelActor("WHITE PLUGIN", seed=2),
    )
    app.run()


if __name__ == "__main__":
    main()
