from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
import random

Move = Tuple[Tuple[int,int], Tuple[int,int], Optional[Tuple[int,int]]]

@dataclass
class Memory:
    recent_positions: List[str] = field(default_factory=list)
    move_scores: Dict[str, float] = field(default_factory=dict)
    subconscious_ticks: int = 0

    def remember_position(self, board):
        key = board_key(board)
        self.recent_positions.append(key)
        self.recent_positions = self.recent_positions[-64:]

    def score_move(self, move: Move) -> float:
        return self.move_scores.get(move_key(move), 0.0)

    def reinforce(self, move: Move, value: float):
        k = move_key(move)
        self.move_scores[k] = self.move_scores.get(k, 0.0) + value

def board_key(board):
    return "/".join("".join(row) for row in board)

def move_key(move):
    a,b,c = move
    return f"{a[0]},{a[1]}>{b[0]},{b[1]}:" + (f"{c[0]},{c[1]}" if c else "-")

def initial_board():
    b = [["." for _ in range(8)] for _ in range(8)]
    for r in range(3):
        for c in range(8):
            if (r+c) % 2 == 1: b[r][c] = "b"
    for r in range(5,8):
        for c in range(8):
            if (r+c) % 2 == 1: b[r][c] = "r"
    return b

def dirs(piece):
    if piece == "r": return [(-1,-1),(-1,1)]
    if piece == "b": return [(1,-1),(1,1)]
    return [(-1,-1),(-1,1),(1,-1),(1,1)]

def owner(piece):
    return piece.lower() if piece != "." else "."

def legal_moves(board, side):
    captures, moves = [], []
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if owner(p) != side: continue
            for dr,dc in dirs(p):
                r1,c1 = r+dr,c+dc
                r2,c2 = r+2*dr,c+2*dc
                if 0 <= r2 < 8 and 0 <= c2 < 8 and 0 <= r1 < 8 and 0 <= c1 < 8:
                    if board[r1][c1] != "." and owner(board[r1][c1]) != side and board[r2][c2] == ".":
                        captures.append(((r,c),(r2,c2),(r1,c1)))
                if 0 <= r1 < 8 and 0 <= c1 < 8 and board[r1][c1] == ".":
                    moves.append(((r,c),(r1,c1),None))
    return captures if captures else moves

def apply_move(board, move):
    b = [row[:] for row in board]
    (r,c),(r2,c2),cap = move
    p = b[r][c]
    b[r][c] = "."
    b[r2][c2] = p
    if cap: b[cap[0]][cap[1]] = "."
    if p == "r" and r2 == 0: b[r2][c2] = "R"
    if p == "b" and r2 == 7: b[r2][c2] = "B"
    return b

def material(board, side):
    vals = {"r":1,"R":2,"b":1,"B":2}
    mine = sum(vals.get(x,0) for row in board for x in row if owner(x)==side)
    other = sum(vals.get(x,0) for row in board for x in row if x!="." and owner(x)!=side)
    return mine-other

class TwoStateAgent:
    def __init__(self, name="Agent", variant="balanced", seed=1):
        self.name = name
        self.variant = variant
        self.rng = random.Random(seed)
        self.memory = Memory()
        self.last_move = None
        self.field_weight = 1.0
        self.void_weight = 1.0
        self.subconscious_rate = 3

    def subconscious_tick(self, board, side):
        self.memory.subconscious_ticks += 1
        self.memory.remember_position(board)
        for m in legal_moves(board, side):
            trial = apply_move(board, m)
            score = material(trial, side)
            if self.variant == "structure":
                score += 0.4 if m[2] else 0.0
                score += 0.08 * (3.5 - abs(m[1][1]-3.5))
            elif self.variant == "novelty":
                k = board_key(trial)
                score += 0.45 if k not in self.memory.recent_positions[:-1] else -0.2
                score += self.rng.uniform(-0.15,0.15)
            self.memory.reinforce(m, 0.02*score)

    def field(self, board, side):
        moves = legal_moves(board, side)
        if not moves: return None
        ranked = []
        for m in moves:
            trial = apply_move(board, m)
            immediate = material(trial, side)
            subconscious = self.memory.score_move(m)
            noise = self.rng.uniform(-0.05,0.05)
            ranked.append((self.field_weight*immediate + subconscious + noise, m))
        ranked.sort(key=lambda x:x[0], reverse=True)
        return ranked[0][1]

    def void(self, board, side, proposal):
        if proposal is None: return ("reject", None, -999)
        legal = legal_moves(board, side)
        if proposal not in legal: return ("reject", None, -999)
        trial = apply_move(board, proposal)
        own_after = material(trial, side)
        opp = "b" if side=="r" else "r"
        replies = legal_moves(trial, opp)
        worst = own_after
        for reply in replies:
            after_reply = apply_move(trial, reply)
            worst = min(worst, material(after_reply, side))
        threshold = -1.5 if self.variant == "structure" else -2.0
        if worst < threshold:
            alternatives = [m for m in legal if m != proposal]
            if alternatives:
                return ("hold", alternatives[0], worst)
        return ("accept", proposal, worst)

    def decide(self, board, side):
        for _ in range(self.subconscious_rate):
            self.subconscious_tick(board, side)
        proposal = self.field(board, side)
        result, move, score = self.void(board, side, proposal)
        if result == "hold" and move is not None:
            proposal = move
            result, move, score = self.void(board, side, proposal)
        self.last_move = move
        return result, move, score

    def learn(self, move, consequence):
        if move:
            self.memory.reinforce(move, consequence)

def play_game(agent_r, agent_b, max_turns=180):
    board = initial_board()
    side = "r"
    log = []
    for turn in range(max_turns):
        agent = agent_r if side=="r" else agent_b
        result, move, score = agent.decide(board, side)
        if move is None:
            winner = "b" if side=="r" else "r"
            return winner, board, log
        before = material(board, side)
        board = apply_move(board, move)
        after = material(board, side)
        agent.learn(move, (after-before)*0.15)
        log.append({"turn":turn+1,"side":side,"agent":agent.name,"state":result,"move":move_key(move),"score":score})
        side = "b" if side=="r" else "r"
    mr = material(board,"r")
    winner = "r" if mr > 0 else "b" if mr < 0 else "draw"
    return winner, board, log
