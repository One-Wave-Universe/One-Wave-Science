#!/usr/bin/env python3
import argparse, ast, json, math, os, re, sqlite3, time
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
    """Persistent receipts + snapshot; receipts are sufficient for fallback rebuild."""
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
                pre_reference TEXT,
                post_reference TEXT,
                field_json TEXT NOT NULL,
                void_json TEXT NOT NULL,
                evidence_json TEXT,
                result TEXT NOT NULL,
                q REAL NOT NULL,
                salience REAL NOT NULL DEFAULT 0.5
            )
        """)
        cols = {r["name"] for r in self.conn.execute("PRAGMA table_info(receipts)")}
        for name, decl in (("pre_reference", "TEXT"), ("post_reference", "TEXT"), ("evidence_json", "TEXT")):
            if name not in cols:
                self.conn.execute(f"ALTER TABLE receipts ADD COLUMN {name} {decl}")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_receipts_cycle ON receipts(cycle)")
        self.conn.commit()

    def remember(self, *, state: BrainState, question: str, pre_reference: str,
                 post_reference: str, field: Dict[str, Any], void: Dict[str, Any],
                 evidence: Dict[str, Any], result: str, salience: float = 0.5):
        self.conn.execute(
            """INSERT INTO receipts
               (ts,cycle,question,reference,pre_reference,post_reference,field_json,void_json,evidence_json,result,q,salience)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
            (time.time(), state.cycle, question, pre_reference, pre_reference, post_reference,
             json.dumps(field, sort_keys=True), json.dumps(void, sort_keys=True),
             json.dumps(evidence, sort_keys=True), result, state.q, salience),
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
        newest_id = rows[0]["id"] if rows else 0
        for row in rows:
            pre = row["pre_reference"] or row["reference"] or ""
            post = row["post_reference"] or row["result"] or ""
            blob = f"{row['question']} {pre} {post} {row['result']}"
            tok = self._tokens(blob)
            overlap = len(qtok & tok) / max(1, len(qtok))
            recency = 1.0 / (1.0 + max(0, newest_id - row["id"]) / 20.0)
            score = 0.65 * overlap + 0.20 * recency + 0.15 * float(row["salience"])
            if overlap > 0:
                scored.append((score, row, pre, post))
        scored.sort(key=lambda x: x[0], reverse=True)
        out = []
        for score, row, pre, post in scored[:limit]:
            out.append({
                "score": round(score, 4), "cycle": row["cycle"], "question": row["question"],
                "pre_reference": pre, "post_reference": post, "result": row["result"], "q": row["q"]
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
        try:
            field = json.loads(row["field_json"])
        except Exception:
            field = {}
        try:
            void = json.loads(row["void_json"])
        except Exception:
            void = {}
        post = row["post_reference"] or row["result"] or row["reference"] or "GROUND / LOCAL REFERENCE"
        return BrainState(
            cycle=int(row["cycle"]), q=float(row["q"]), reference=post,
            last_choice=field.get("choice", "GROUND"), last_move=field.get("move", "HOLD"),
            last_void=void.get("response", "DEFER"), last_result=row["result"], lifecycle="IDLE"
        )

class DeterministicResolver:
    """No LLM: arithmetic, prior receipt recall, then local canonical text lookup."""
    STOP = {"what","when","where","which","who","why","how","are","was","were","the","and","for","with","about","does","did","this","that","from","into","your","you","our","can","tell","give","show","please"}
    NUMBERS = {
        "zero":"0","one":"1","two":"2","three":"3","four":"4","five":"5",
        "six":"6","seven":"7","eight":"8","nine":"9","ten":"10",
        "eleven":"11","twelve":"12","thirteen":"13","fourteen":"14","fifteen":"15",
        "sixteen":"16","seventeen":"17","eighteen":"18","nineteen":"19","twenty":"20",
    }
    CANON_FILES = [
        "AI_CANONICAL_START_HERE.md",
        "UPDATED_43_TWO_CHOICE_THREE_MOVE_SIX_ROUTE_LOGIC.md",
        "UPDATED_44_STATE_AXIS_AUTHORITY_AND_EVOLUTION_RULE.md",
        "Nodes/G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md",
        "Nodes/G-742_Nonverbal_Loop_Continuity_and_Language_Adapter.md",
        "Nodes/G-724_M4_Heterogeneous_Runtime_and_Dual_Six_Gate_Controller.md",
    ]

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def _safe_eval(self, expr: str) -> float:
        node = ast.parse(expr, mode="eval")
        def ev(n):
            if isinstance(n, ast.Expression): return ev(n.body)
            if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool): return n.value
            if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
                v = ev(n.operand); return v if isinstance(n.op, ast.UAdd) else -v
            if isinstance(n, ast.BinOp):
                a, b = ev(n.left), ev(n.right)
                if isinstance(n.op, ast.Add): return a + b
                if isinstance(n.op, ast.Sub): return a - b
                if isinstance(n.op, ast.Mult): return a * b
                if isinstance(n.op, ast.Div): return a / b
                if isinstance(n.op, ast.FloorDiv): return a // b
                if isinstance(n.op, ast.Mod): return a % b
                if isinstance(n.op, ast.Pow):
                    if abs(b) > 12: raise ValueError("exponent too large")
                    return a ** b
            raise ValueError("unsupported arithmetic")
        value = ev(node)
        if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
            raise ValueError("non-finite result")
        return float(value)

    def _math(self, question: str) -> Optional[Dict[str, Any]]:
        q = question.lower().strip()
        q = re.sub(r"\b(multiplied by|times)\b", " * ", q)
        q = re.sub(r"\b(divided by|over)\b", " / ", q)
        q = re.sub(r"\bplus\b", " + ", q)
        q = re.sub(r"\bminus\b", " - ", q)
        for word, digit in self.NUMBERS.items():
            q = re.sub(rf"\b{word}\b", digit, q)
        q = re.sub(r"\b(what is|calculate|compute|please|equals|equal to|answer|what)\b", " ", q)
        q = q.replace("?", " ").replace("=", " ")
        if re.search(r"[a-z]", q):
            return None
        expr = "".join(re.findall(r"[0-9\.\+\-\*/%() ]+", q)).strip()
        if not expr or not re.search(r"[+\-*/%]", expr):
            return None
        try:
            value = self._safe_eval(expr)
        except Exception:
            return None
        answer = str(int(value)) if value.is_integer() else (f"{value:.12g}")
        return {"status":"RESOLVED", "source":"arithmetic", "answer":answer,
                "confidence":1.0, "provenance":expr}

    def _memory(self, question: str, recalled: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        q = question.lower()
        cue = any(p in q for p in ("what did i say", "what did we say", "recall", "remember", "what about"))
        if not cue or not recalled:
            return None
        best = recalled[0]
        answer = f"Cycle {best['cycle']}: {best['question']}"
        return {"status":"RESOLVED", "source":"memory", "answer":answer,
                "confidence":min(1.0, 0.60 + float(best["score"])),
                "provenance":f"memory.sqlite3 cycle {best['cycle']}"}

    def _canon(self, question: str) -> Optional[Dict[str, Any]]:
        qtokens = {t for t in re.findall(r"[a-z0-9_]+", question.lower()) if len(t) > 2 and t not in self.STOP}
        if not qtokens:
            return None
        best = None
        for rel in self.CANON_FILES:
            path = self.repo_root / rel
            if not path.exists():
                continue
            try:
                text = path.read_text(errors="replace")
            except Exception:
                continue
            paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
            for idx, p in enumerate(paragraphs):
                ptok = set(re.findall(r"[a-z0-9_]+", p.lower()))
                overlap = len(qtokens & ptok)
                if overlap == 0:
                    continue
                coverage = overlap / len(qtokens)
                density = overlap / max(8, min(80, len(ptok)))
                score = 0.85 * coverage + 0.15 * density
                if best is None or score > best[0]:
                    best = (score, rel, idx, p, paragraphs[idx + 1] if idx + 1 < len(paragraphs) else "")
        if best is None or best[0] < 0.42:
            return None
        score, rel, idx, p, next_p = best
        if p.lstrip().startswith("#") and next_p:
            p = p + "\n" + next_p
        clean = re.sub(r"```(?:text)?", "", p).replace("```", "").strip()
        clean = re.sub(r"\s+", " ", clean)
        if len(clean) > 600:
            clean = clean[:597] + "..."
        return {"status":"RESOLVED", "source":"canon", "answer":clean,
                "confidence":round(min(0.95, 0.55 + 0.35 * score), 4),
                "provenance":f"{rel} paragraph {idx + 1}"}

    def resolve(self, question: str, recalled: List[Dict[str, Any]]) -> Dict[str, Any]:
        for fn in (lambda: self._math(question), lambda: self._memory(question, recalled), lambda: self._canon(question)):
            hit = fn()
            if hit:
                return hit
        return {"status":"UNKNOWN", "source":"none", "answer":"", "confidence":0.0,
                "provenance":"no deterministic resolver produced verified evidence"}

class FieldMachine:
    """Expressive side. Route is driven by resolver evidence, never by text hashing."""
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

    def step(self, question: str, state: BrainState, recalled: List[Dict[str, Any]], evidence: Dict[str, Any]) -> Dict[str, Any]:
        resolved = evidence.get("status") == "RESOLVED"
        strength = max(0.0, min(1.0, float(evidence.get("confidence", 0.0))))
        choice = "YES" if resolved else "NO"
        move = "UP" if resolved else "HOLD"
        m = 1.0 if resolved else 0.0
        b = 1.0 if resolved else -1.0
        phase_lock = 1.0 if resolved else 0.0
        if self.backend == "cuda":
            t = self.torch
            dev = t.device("cuda")
            q = t.tensor([state.q], dtype=t.float32, device=dev)
            nq = t.clamp(RETENTION*q + GAIN*b*m*strength*phase_lock, -Q_MAX, Q_MAX)
            q_next = float(nq.item())
        else:
            q_next = max(-Q_MAX, min(Q_MAX, RETENTION*state.q + GAIN*b*m*strength*phase_lock))
        return {
            "backend": self.backend,
            "polarity": "EXPRESS" if resolved else "HOLD",
            "choice": choice, "move": move, "drive": round(strength, 4),
            "phase_lock": phase_lock, "q_next": round(q_next, 6),
            "views_up": {"direction": move, "phase": "LOCKED" if resolved else "UNRESOLVED",
                         "strength": round(strength, 4), "reference": state.reference,
                         "evidence_source": evidence.get("source", "none")},
            "recalled_cycles": [r["cycle"] for r in recalled],
        }

class VoidMachine:
    """CPU oversight checks the deterministic evidence contract before commit."""
    def step(self, question: str, state: BrainState, field: Dict[str, Any], evidence: Dict[str, Any]) -> Dict[str, Any]:
        resolved = evidence.get("status") == "RESOLVED"
        answer = str(evidence.get("answer", "")).strip()
        provenance = str(evidence.get("provenance", "")).strip()
        confidence = float(evidence.get("confidence", 0.0))
        if not question.strip():
            decision, reason = "DENY", "empty question"
        elif not resolved:
            decision, reason = "DEFER", "no verified deterministic evidence"
        elif not answer or not provenance:
            decision, reason = "DENY", "resolved evidence missing answer or provenance"
        elif confidence < 0.50:
            decision, reason = "DEFER", "evidence below commit threshold"
        else:
            decision, reason = "CONFIRM", "evidence contract satisfied"
        return {
            "backend": "cpu", "response": decision,
            "oversight": "ALLOW" if decision == "CONFIRM" else ("HOLD" if decision == "DEFER" else "OVERRIDE"),
            "reason": reason, "action_down": "NONE" if decision != "DENY" else "OVERRIDE",
            "evidence_source": evidence.get("source", "none"),
        }

class M4Loop:
    def __init__(self, memory_root: Path, repo_root: Optional[Path] = None):
        self.memory = RecallRebuildMemory(memory_root)
        self.state = self.memory.rebuild()
        self.field = FieldMachine()
        self.void = VoidMachine()
        self.repo_root = repo_root or Path(__file__).resolve().parents[1]
        self.resolver = DeterministicResolver(self.repo_root)

    def cycle(self, question: str) -> Dict[str, Any]:
        s = self.state
        pre_reference = s.reference
        s.lifecycle = "PRIMED"
        recalled = self.memory.recall(question)
        evidence = self.resolver.resolve(question, recalled)
        s.lifecycle = "EXECUTING"
        field = self.field.step(question, s, recalled, evidence)
        s.lifecycle = "VECTORING"
        void = self.void.step(question, s, field, evidence)
        s.lifecycle = "RESOLVING"

        if void["response"] == "CONFIRM":
            s.q = float(field["q_next"])
            result = str(evidence["answer"])
            s.reference = result
        elif void["response"] == "DEFER":
            result = f"DEFER: {void['reason']}"
        else:
            result = f"DENY: {void['reason']}"

        s.cycle += 1
        s.last_choice = field["choice"]
        s.last_move = field["move"]
        s.last_void = void["response"]
        s.last_result = result
        s.lifecycle = "IDLE"
        post_reference = s.reference
        self.memory.remember(
            state=s, question=question, pre_reference=pre_reference, post_reference=post_reference,
            field=field, void=void, evidence=evidence, result=result,
            salience=min(1.0, 0.4 + abs(s.q)),
        )
        return {
            "cycle": s.cycle, "answer": result, "result": result,
            "state": asdict(s), "evidence": evidence, "field": field, "void": void,
            "recall": recalled,
            "recursion": ["BEGIN", "BUILD 1", "HOLD", "BUILD 2", "BREAK / RELEASE", "LOOP"],
        }

def main():
    ap = argparse.ArgumentParser(description="Algorythm-Zer0 deterministic Field/Void Jetson brain-loop prototype")
    ap.add_argument("question", nargs="*", help="one input/question")
    ap.add_argument("--memory", default=os.environ.get("ZER0_MEMORY", "./brain-memory"))
    ap.add_argument("--repl", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()
    loop = M4Loop(Path(args.memory))
    if args.status:
        print(json.dumps({"state": asdict(loop.state), "field_backend": loop.field.backend, "resolver": "deterministic"}, indent=2))
        return
    if args.repl or not args.question:
        print(f"Algorythm-Zer0 brain loop | Field={loop.field.backend} | Void=cpu | resolver=deterministic | memory={args.memory}")
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
