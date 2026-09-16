#!/usr/bin/env python3
import argparse, json, math, os, re, sqlite3, time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

RETENTION = 0.92
GAIN = 0.24
Q_MAX = 1.0

@dataclass
class BrainState:
    cycle: int = 0
    q: float = 0.0
    reference: str = "GROUND / LOCAL REFERENCE"
    last_choice: str = "GROUND"
    last_move: str = "HOLD"
    last_void: str = "DEFER"
    last_result: str = ""
    lifecycle: str = "IDLE"

class RecallRebuildMemory:
    """Persistent memory for the Field/Void loop.

    HOLD: current BrainState in RAM.
    RECALL: retrieve relevant prior cycle receipts from SQLite.
    REBUILD: reconstruct state from latest snapshot + append-only receipts.
    """
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.db_path = root / "memory.sqlite3"
        self.snapshot_path = root / "state.json"
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts REAL NOT NULL,
                cycle INTEGER NOT NULL,
                question TEXT NOT NULL,
                reference TEXT NOT NULL,
                field_json TEXT NOT NULL,
                void_json TEXT NOT NULL,
                result TEXT NOT NULL,
                q REAL NOT NULL,
                salience REAL NOT NULL DEFAULT 0.5
            )
        """)
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_receipts_cycle ON receipts(cycle)")
        self.conn.commit()

    def remember(self, *, state: BrainState, question: str, field: Dict[str, Any], void: Dict[str, Any], result: str, salience: float = 0.5):
        self.conn.execute(
            "INSERT INTO receipts(ts,cycle,question,reference,field_json,void_json,result,q,salience) VALUES(?,?,?,?,?,?,?,?,?)",
            (time.time(), state.cycle, question, state.reference, json.dumps(field, sort_keys=True), json.dumps(void, sort_keys=True), result, state.q, salience),
        )
        self.conn.commit()
        self.snapshot(state)

    def snapshot(self, state: BrainState):
        tmp = self.snapshot_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(asdict(state), indent=2, sort_keys=True) + "\n")
        os.replace(tmp, self.snapshot_path)

    def _tokens(self, text: str):
        return {w for w in re.findall(r"[a-z0-9_]+", text.lower()) if len(w) > 2}

    def recall(self, query: str, limit: int = 6) -> List[Dict[str, Any]]:
        qtok = self._tokens(query)
        rows = self.conn.execute("SELECT * FROM receipts ORDER BY id DESC LIMIT 250").fetchall()
        scored = []
        for row in rows:
            blob = f"{row['question']} {row['reference']} {row['result']}"
            tok = self._tokens(blob)
            overlap = len(qtok & tok) / max(1, len(qtok))
            recency = 1.0 / (1.0 + max(0, rows[0]['id'] - row['id']) / 20.0) if rows else 0.0
            score = 0.65 * overlap + 0.20 * recency + 0.15 * float(row['salience'])
            if overlap > 0 or len(scored) < limit:
                scored.append((score, row))
        scored.sort(key=lambda x: x[0], reverse=True)
        out = []
        for score, row in scored[:limit]:
            out.append({
                "score": round(score, 4), "cycle": row["cycle"], "question": row["question"],
                "reference": row["reference"], "result": row["result"], "q": row["q"]
            })
        return out

    def rebuild(self) -> BrainState:
        if self.snapshot_path.exists():
            try:
                return BrainState(**json.loads(self.snapshot_path.read_text()))
            except Exception:
                pass
        row = self.conn.execute("SELECT * FROM receipts ORDER BY id DESC LIMIT 1").fetchone()
        if not row:
            return BrainState()
        return BrainState(
            cycle=int(row["cycle"]), q=float(row["q"]), reference=row["result"] or row["reference"],
            last_result=row["result"], lifecycle="IDLE"
        )

class FieldMachine:
    """Expressive side. Uses CUDA for numerical state update when torch+CUDA exist."""
    def __init__(self):
        self.backend = "cpu-python"
        self.torch = None
        try:
            import torch
            self.torch = torch
            if torch.cuda.is_available():
                self.backend = "cuda"
        except Exception:
            pass

    def _drive(self, text: str) -> float:
        h = sum((i + 1) * ord(c) for i, c in enumerate(text[:2048]))
        return ((h % 2001) - 1000) / 1000.0

    def step(self, question: str, state: BrainState, recalled: List[Dict[str, Any]]) -> Dict[str, Any]:
        drive = self._drive(question)
        choice = "YES" if drive >= 0 else "NO"
        b = 1.0 if choice == "YES" else -1.0
        magnitude = min(1.0, abs(drive))
        if magnitude < 0.12:
            move, m = "HOLD", 0.0
        elif drive > 0:
            move, m = "UP", 1.0
        else:
            move, m = "DOWN", -1.0
        phase_lock = 1.0
        if self.backend == "cuda":
            t = self.torch
            dev = t.device("cuda")
            q = t.tensor([state.q], dtype=t.float32, device=dev)
            nq = t.clamp(RETENTION*q + GAIN*b*m*magnitude*phase_lock, -Q_MAX, Q_MAX)
            q_next = float(nq.item())
        else:
            q_next = max(-Q_MAX, min(Q_MAX, RETENTION*state.q + GAIN*b*m*magnitude*phase_lock))
        return {
            "backend": self.backend,
            "polarity": "EXPRESS" if drive >= 0 else "COMPRESS",
            "choice": choice,
            "move": move,
            "drive": round(drive, 4),
            "phase_lock": phase_lock,
            "q_next": round(q_next, 6),
            "views_up": {
                "direction": move,
                "phase": "LOCKED",
                "strength": round(magnitude, 4),
                "reference": state.reference,
            },
            "recalled_cycles": [r["cycle"] for r in recalled],
        }

class VoidMachine:
    """Independent CPU oversight side."""
    def step(self, question: str, state: BrainState, field: Dict[str, Any], recalled: List[Dict[str, Any]]) -> Dict[str, Any]:
        strength = float(field["views_up"]["strength"])
        if not question.strip():
            decision = "DENY"
        elif strength < 0.12:
            decision = "DEFER"
        else:
            decision = "CONFIRM"
        if abs(float(field["q_next"])) > Q_MAX:
            decision = "DENY"
        return {
            "backend": "cpu",
            "response": decision,
            "oversight": "ALLOW" if decision == "CONFIRM" else ("HOLD" if decision == "DEFER" else "OVERRIDE"),
            "actions_down": ["INWARD", "OUTWARD", "ACROSS", "OVER"],
            "memory_hits": len(recalled),
        }

class M4Loop:
    def __init__(self, memory_root: Path):
        self.memory = RecallRebuildMemory(memory_root)
        self.state = self.memory.rebuild()
        self.field = FieldMachine()
        self.void = VoidMachine()

    def cycle(self, question: str) -> Dict[str, Any]:
        s = self.state
        s.lifecycle = "PRIMED"
        recalled = self.memory.recall(question)
        s.lifecycle = "EXECUTING"
        field = self.field.step(question, s, recalled)
        s.lifecycle = "VECTORING"
        void = self.void.step(question, s, field, recalled)
        s.lifecycle = "RESOLVING"

        if void["response"] == "CONFIRM":
            s.q = float(field["q_next"])
            result = f"{field['polarity']} / {field['choice']} / {field['move']} / q={s.q:.4f}"
            s.reference = result
        elif void["response"] == "DEFER":
            result = f"HOLD against reference: {s.reference}"
        else:
            result = f"RESET/HOLD against reference: {s.reference}"

        s.cycle += 1
        s.last_choice = field["choice"]
        s.last_move = field["move"]
        s.last_void = void["response"]
        s.last_result = result
        s.lifecycle = "IDLE"
        self.memory.remember(state=s, question=question, field=field, void=void, result=result, salience=min(1.0, 0.4 + abs(s.q)))
        return {
            "cycle": s.cycle,
            "result": result,
            "state": asdict(s),
            "field": field,
            "void": void,
            "recall": recalled,
            "recursion": ["BEGIN", "BUILD 1", "HOLD", "BUILD 2", "BREAK / RELEASE", "LOOP"],
        }

def main():
    ap = argparse.ArgumentParser(description="Algorythm-Zer0 Field/Void Jetson brain-loop prototype")
    ap.add_argument("question", nargs="*", help="one input/question")
    ap.add_argument("--memory", default=os.environ.get("ZER0_MEMORY", "./brain-memory"))
    ap.add_argument("--repl", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()
    loop = M4Loop(Path(args.memory))
    if args.status:
        print(json.dumps({"state": asdict(loop.state), "field_backend": loop.field.backend}, indent=2))
        return
    if args.repl or not args.question:
        print(f"Algorythm-Zer0 brain loop | Field={loop.field.backend} | Void=cpu | memory={args.memory}")
        while True:
            try: q = input("zer0> ").strip()
            except (EOFError, KeyboardInterrupt): break
            if not q: continue
            if q in {"/quit", "/exit"}: break
            if q == "/status":
                print(json.dumps(asdict(loop.state), indent=2)); continue
            if q.startswith("/recall "):
                print(json.dumps(loop.memory.recall(q[8:]), indent=2)); continue
            print(json.dumps(loop.cycle(q), indent=2))
    else:
        print(json.dumps(loop.cycle(" ".join(args.question)), indent=2))

if __name__ == "__main__":
    main()
