"""Field/Void claim-database builder.

Two machine states only: FIELD and VOID. The six steps run *inside* each
state; they are progress within a pass, not additional machine states.

    step 1  reference     read the claim version, sources, incoming receipt
    step 2  choice        select one move (constructive / uncertainty)
    step 3  move          derive, test, counterderive, countertest
    step 4  views_up      findings returned to the parent question
    step 5  actions_down  bounded work sent into child questions
    step 6  state_scale   what the result supports, and at what scope
    reentry               handoff() -> the other state

Field builds the candidate state. Void tests and rebuilds it. Either side may
propose, challenge, act, and correct.

The SQLite database is the shared retained reference. Neither side starts
from an empty conversation: each pass reads the exact claim version,
reference version, repository commit, evidence, and open contradictions.

Handoff conditions (initial implementation):

    FIELD -> VOID   candidate, scope, supporting evidence and a complete
                    six-step receipt are saved.
    VOID  -> FIELD  review (six steps), counterproposal or correction,
                    evidence, and the next bounded question are saved.
    HOLD            any unmet condition, an explicit hold, or a changed shared
                    reference. The loop keeps its state and records the
                    blocker. Nothing switches merely because time passed.

A correction creates a new claim version. Earlier versions and receipts are
never rewritten. Claim status ("supported", "unresolved", ...) describes a
claim version and is separate from the machine's FIELD/VOID state.

Nested operation: a loop may open child loops. A child keeps its own claim,
reference, and receipts; return_upward() attaches the child's latest receipt
to the parent's current pass as evidence.

Deterministic. No model calls. Content for each step is supplied by the
caller (a human, a worker, or a later Field/Void provider).
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


FIELD = "FIELD"
VOID = "VOID"
STATES = (FIELD, VOID)

STEPS = ("reference", "choice", "move", "views_up", "actions_down", "state_scale")

CLAIM_STATUSES = ("proposed", "supported", "unresolved", "refuted")


class ClaimLoopError(Exception):
    """Raised for calls that violate the machine's rules (not for holds)."""


@dataclass
class MachineRecord:
    active_state: str
    claim_id: str
    claim_version: int
    reference_version: int
    parent_loop_id: Optional[str]
    current_step: int
    candidate: str
    evidence_ids: List[str]
    contradiction_ids: List[str]
    receipt_id: Optional[str]

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HandoffResult:
    switched: bool
    from_state: str
    to_state: str
    receipt_id: Optional[str]
    blockers: List[str]


_SCHEMA = """
CREATE TABLE meta (key TEXT PRIMARY KEY, value INTEGER NOT NULL);
CREATE TABLE claims (
    claim_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    parent_version INTEGER,
    parent_claim_id TEXT,
    text TEXT NOT NULL,
    scope TEXT NOT NULL,
    status TEXT NOT NULL,
    created_by TEXT NOT NULL,
    created_loop_id TEXT,
    created_seq INTEGER NOT NULL,
    PRIMARY KEY (claim_id, version)
);
CREATE TABLE loops (
    loop_id TEXT PRIMARY KEY,
    parent_loop_id TEXT,
    claim_id TEXT NOT NULL,
    claim_version INTEGER NOT NULL,
    reference_version INTEGER NOT NULL,
    repo_commit TEXT,
    question TEXT NOT NULL,
    active_state TEXT NOT NULL,
    pass_number INTEGER NOT NULL,
    current_step INTEGER NOT NULL,
    incoming_receipt_id TEXT,
    last_receipt_id TEXT,
    pass_json TEXT NOT NULL
);
CREATE TABLE evidence (
    evidence_id TEXT PRIMARY KEY,
    loop_id TEXT,
    pass_number INTEGER,
    claim_id TEXT NOT NULL,
    claim_version INTEGER NOT NULL,
    kind TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT NOT NULL
);
CREATE TABLE contradictions (
    contradiction_id TEXT PRIMARY KEY,
    loop_id TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    claim_version INTEGER NOT NULL,
    description TEXT NOT NULL,
    resolved INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE receipts (
    receipt_id TEXT PRIMARY KEY,
    loop_id TEXT NOT NULL,
    pass_number INTEGER NOT NULL,
    state TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    claim_version INTEGER NOT NULL,
    reference_version INTEGER NOT NULL,
    repo_commit TEXT,
    incoming_receipt_id TEXT,
    body_json TEXT NOT NULL
);
CREATE TABLE events (
    seq INTEGER PRIMARY KEY,
    loop_id TEXT,
    kind TEXT NOT NULL,
    detail TEXT NOT NULL
);
"""


def _empty_pass() -> Dict[str, Any]:
    return {
        "steps": {},
        "evidence_ids": [],
        "contradiction_ids": [],
        "correction_version": None,
        "counterproposal": None,
        "next_question": None,
        "holds": [],
    }


class ClaimDatabase:
    """Shared retained reference plus the Field/Void loop machine."""

    def __init__(self, path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        exists = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='meta'"
        ).fetchone()
        if not exists:
            self.conn.executescript(_SCHEMA)
            self.conn.executemany(
                "INSERT INTO meta (key, value) VALUES (?, 0)",
                [("seq",), ("claim",), ("loop",), ("evidence",),
                 ("contradiction",), ("receipt",)],
            )
            self.conn.commit()

    # ------------------------------------------------------------------ ids

    def _next(self, key: str) -> int:
        self.conn.execute("UPDATE meta SET value = value + 1 WHERE key = ?", (key,))
        return self.conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()[0]

    def _new_id(self, key: str, prefix: str) -> str:
        return f"{prefix}{self._next(key):04d}"

    @property
    def reference_version(self) -> int:
        """Ledger sequence: increases on every committed write."""
        return self.conn.execute("SELECT value FROM meta WHERE key = 'seq'").fetchone()[0]

    def _log(self, loop_id: Optional[str], kind: str, detail: Any) -> int:
        seq = self._next("seq")
        self.conn.execute(
            "INSERT INTO events (seq, loop_id, kind, detail) VALUES (?, ?, ?, ?)",
            (seq, loop_id, kind, json.dumps(detail, sort_keys=True)),
        )
        return seq

    # --------------------------------------------------------------- claims

    def create_claim(
        self, text: str, scope: str, *, parent_claim_id: Optional[str] = None,
        status: str = "unresolved",
    ) -> str:
        self._check_status(status)
        claim_id = self._new_id("claim", "C")
        seq = self._log(None, "claim_created", {"claim_id": claim_id, "version": 1})
        self.conn.execute(
            "INSERT INTO claims VALUES (?, 1, NULL, ?, ?, ?, ?, 'EXTERNAL', NULL, ?)",
            (claim_id, parent_claim_id, text, scope, status, seq),
        )
        self.conn.commit()
        return claim_id

    def claim(self, claim_id: str, version: Optional[int] = None) -> Dict[str, Any]:
        if version is None:
            version = self.latest_version(claim_id)
        row = self.conn.execute(
            "SELECT * FROM claims WHERE claim_id = ? AND version = ?", (claim_id, version)
        ).fetchone()
        if row is None:
            raise ClaimLoopError(f"unknown claim {claim_id} v{version}")
        return dict(row)

    def claim_versions(self, claim_id: str) -> List[Dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT * FROM claims WHERE claim_id = ? ORDER BY version", (claim_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    def latest_version(self, claim_id: str) -> int:
        row = self.conn.execute(
            "SELECT MAX(version) FROM claims WHERE claim_id = ?", (claim_id,)
        ).fetchone()
        if row[0] is None:
            raise ClaimLoopError(f"unknown claim {claim_id}")
        return row[0]

    @staticmethod
    def _check_status(status: str) -> None:
        if status not in CLAIM_STATUSES:
            raise ClaimLoopError(f"unknown claim status {status!r}")

    def add_source(self, claim_id: str, content: str, source: str) -> str:
        """Attach external source material to the latest claim version."""
        evidence_id = self._new_id("evidence", "E")
        self.conn.execute(
            "INSERT INTO evidence VALUES (?, NULL, NULL, ?, ?, 'source', ?, ?)",
            (evidence_id, claim_id, self.latest_version(claim_id), content, source),
        )
        self._log(None, "source_added", {"evidence_id": evidence_id, "claim_id": claim_id})
        self.conn.commit()
        return evidence_id

    # ---------------------------------------------------------------- loops

    def open_loop(
        self, claim_id: str, question: str, *, parent_loop_id: Optional[str] = None,
        repo_commit: Optional[str] = None,
    ) -> str:
        if parent_loop_id is not None:
            self._loop(parent_loop_id)
        version = self.latest_version(claim_id)
        loop_id = self._new_id("loop", "L")
        seq = self._log(loop_id, "loop_opened", {
            "claim_id": claim_id, "claim_version": version, "parent_loop_id": parent_loop_id,
        })
        self.conn.execute(
            "INSERT INTO loops VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 1, NULL, NULL, ?)",
            (loop_id, parent_loop_id, claim_id, version, seq, repo_commit, question,
             FIELD, json.dumps(_empty_pass())),
        )
        self.conn.commit()
        return loop_id

    def open_child(
        self, parent_loop_id: str, question: str, claim_text: str, scope: str,
        *, repo_commit: Optional[str] = None,
    ) -> str:
        """Open a child loop on its own child claim (calculation, measurement)."""
        parent = self._loop(parent_loop_id)
        child_claim = self.create_claim(claim_text, scope, parent_claim_id=parent["claim_id"])
        return self.open_loop(
            child_claim, question, parent_loop_id=parent_loop_id,
            repo_commit=repo_commit if repo_commit is not None else parent["repo_commit"],
        )

    def _loop(self, loop_id: str) -> Dict[str, Any]:
        row = self.conn.execute("SELECT * FROM loops WHERE loop_id = ?", (loop_id,)).fetchone()
        if row is None:
            raise ClaimLoopError(f"unknown loop {loop_id}")
        loop = dict(row)
        loop["pass"] = json.loads(loop.pop("pass_json"))
        return loop

    def _save_pass(self, loop_id: str, pass_state: Dict[str, Any]) -> None:
        self.conn.execute(
            "UPDATE loops SET pass_json = ? WHERE loop_id = ?",
            (json.dumps(pass_state), loop_id),
        )

    def machine_record(self, loop_id: str) -> MachineRecord:
        loop = self._loop(loop_id)
        claim = self.claim(loop["claim_id"], loop["claim_version"])
        return MachineRecord(
            active_state=loop["active_state"],
            claim_id=loop["claim_id"],
            claim_version=loop["claim_version"],
            reference_version=loop["reference_version"],
            parent_loop_id=loop["parent_loop_id"],
            current_step=loop["current_step"],
            candidate=claim["text"],
            evidence_ids=list(loop["pass"]["evidence_ids"]),
            contradiction_ids=list(loop["pass"]["contradiction_ids"]),
            receipt_id=loop["last_receipt_id"],
        )

    # ---------------------------------------------------------------- steps

    def record_step(self, loop_id: str, step: str, content: str) -> int:
        """Record one of the six steps, strictly in order. Returns next step."""
        if step not in STEPS:
            raise ClaimLoopError(f"unknown step {step!r}")
        loop = self._loop(loop_id)
        index = STEPS.index(step) + 1
        if index != loop["current_step"] or step in loop["pass"]["steps"]:
            raise ClaimLoopError(
                f"{loop['active_state']} is at step {loop['current_step']} "
                f"({STEPS[loop['current_step'] - 1]}); cannot record {step!r}"
            )
        if not content.strip():
            raise ClaimLoopError(f"step {step!r} needs content")
        pass_state = loop["pass"]
        pass_state["steps"][step] = content
        next_step = min(index + 1, len(STEPS))
        self._save_pass(loop_id, pass_state)
        self.conn.execute(
            "UPDATE loops SET current_step = ? WHERE loop_id = ?", (next_step, loop_id)
        )
        self._log(loop_id, "step", {"state": loop["active_state"], "step": step})
        self.conn.commit()
        return next_step

    def add_evidence(self, loop_id: str, content: str, source: str, kind: str = "result") -> str:
        loop = self._loop(loop_id)
        evidence_id = self._new_id("evidence", "E")
        self.conn.execute(
            "INSERT INTO evidence VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (evidence_id, loop_id, loop["pass_number"], loop["claim_id"],
             loop["claim_version"], kind, content, source),
        )
        pass_state = loop["pass"]
        pass_state["evidence_ids"].append(evidence_id)
        self._save_pass(loop_id, pass_state)
        self._log(loop_id, "evidence", {"evidence_id": evidence_id, "kind": kind})
        self.conn.commit()
        return evidence_id

    def evidence(self, evidence_id: str) -> Dict[str, Any]:
        row = self.conn.execute(
            "SELECT * FROM evidence WHERE evidence_id = ?", (evidence_id,)
        ).fetchone()
        if row is None:
            raise ClaimLoopError(f"unknown evidence {evidence_id}")
        return dict(row)

    def add_contradiction(self, loop_id: str, description: str) -> str:
        loop = self._loop(loop_id)
        contradiction_id = self._new_id("contradiction", "X")
        self.conn.execute(
            "INSERT INTO contradictions VALUES (?, ?, ?, ?, ?, 0)",
            (contradiction_id, loop_id, loop["claim_id"], loop["claim_version"], description),
        )
        pass_state = loop["pass"]
        pass_state["contradiction_ids"].append(contradiction_id)
        self._save_pass(loop_id, pass_state)
        self._log(loop_id, "contradiction", {"contradiction_id": contradiction_id})
        self.conn.commit()
        return contradiction_id

    def open_contradictions(self, claim_id: str) -> List[Dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT * FROM contradictions WHERE claim_id = ? AND resolved = 0 "
            "ORDER BY contradiction_id", (claim_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    def resolve_contradiction(self, loop_id: str, contradiction_id: str) -> None:
        self._loop(loop_id)
        self.conn.execute(
            "UPDATE contradictions SET resolved = 1 WHERE contradiction_id = ?",
            (contradiction_id,),
        )
        self._log(loop_id, "contradiction_resolved", {"contradiction_id": contradiction_id})
        self.conn.commit()

    def set_status(self, loop_id: str, status: str) -> None:
        """Set claim status on the loop's current claim version."""
        self._check_status(status)
        loop = self._loop(loop_id)
        self.conn.execute(
            "UPDATE claims SET status = ? WHERE claim_id = ? AND version = ?",
            (status, loop["claim_id"], loop["claim_version"]),
        )
        self._log(loop_id, "status", {
            "claim_id": loop["claim_id"], "version": loop["claim_version"], "status": status,
        })
        self.conn.commit()

    def set_next_question(self, loop_id: str, question: str) -> None:
        loop = self._loop(loop_id)
        pass_state = loop["pass"]
        pass_state["next_question"] = question
        self._save_pass(loop_id, pass_state)
        self.conn.commit()

    def propose_counter(self, loop_id: str, counterproposal: str) -> None:
        """Void alternative that does not (yet) change the claim text."""
        loop = self._loop(loop_id)
        if loop["active_state"] != VOID:
            raise ClaimLoopError("counterproposals are recorded by VOID")
        pass_state = loop["pass"]
        pass_state["counterproposal"] = counterproposal
        self._save_pass(loop_id, pass_state)
        self._log(loop_id, "counterproposal", {"text": counterproposal})
        self.conn.commit()

    def submit_correction(self, loop_id: str, text: str, scope: str) -> int:
        """Create a new claim version from the active state. Old versions stay."""
        loop = self._loop(loop_id)
        if self.latest_version(loop["claim_id"]) != loop["claim_version"]:
            raise ClaimLoopError("loop reference is stale; resync before correcting")
        version = loop["claim_version"] + 1
        seq = self._log(loop_id, "correction", {
            "claim_id": loop["claim_id"], "from": loop["claim_version"], "to": version,
        })
        parent = self.claim(loop["claim_id"], loop["claim_version"])
        self.conn.execute(
            "INSERT INTO claims VALUES (?, ?, ?, ?, ?, ?, 'proposed', ?, ?, ?)",
            (loop["claim_id"], version, loop["claim_version"], parent["parent_claim_id"],
             text, scope, loop["active_state"], loop_id, seq),
        )
        pass_state = loop["pass"]
        pass_state["correction_version"] = version
        self._save_pass(loop_id, pass_state)
        self.conn.execute(
            "UPDATE loops SET claim_version = ?, reference_version = ? WHERE loop_id = ?",
            (version, seq, loop_id),
        )
        self.conn.commit()
        return version

    # ---------------------------------------------------------------- holds

    def hold(self, loop_id: str, reason: str) -> None:
        loop = self._loop(loop_id)
        pass_state = loop["pass"]
        pass_state["holds"].append(reason)
        self._save_pass(loop_id, pass_state)
        self._log(loop_id, "hold", {"state": loop["active_state"], "reason": reason})
        self.conn.commit()

    def release(self, loop_id: str, reason: str) -> None:
        loop = self._loop(loop_id)
        pass_state = loop["pass"]
        if reason not in pass_state["holds"]:
            raise ClaimLoopError(f"no hold {reason!r} on {loop_id}")
        pass_state["holds"].remove(reason)
        self._save_pass(loop_id, pass_state)
        self._log(loop_id, "release", {"reason": reason})
        self.conn.commit()

    def blockers(self, loop_id: str) -> List[str]:
        return list(self._loop(loop_id)["pass"]["holds"])

    def resync(self, loop_id: str, repo_commit: Optional[str] = None) -> None:
        """Re-read the shared reference. The pass restarts at step 1."""
        loop = self._loop(loop_id)
        version = self.latest_version(loop["claim_id"])
        seq = self._log(loop_id, "resync", {
            "from_version": loop["claim_version"], "to_version": version,
            "repo_commit": repo_commit,
        })
        pass_state = loop["pass"]
        pass_state["steps"] = {}
        pass_state["holds"] = [h for h in pass_state["holds"] if not h.startswith("reference:")]
        self._save_pass(loop_id, pass_state)
        self.conn.execute(
            "UPDATE loops SET claim_version = ?, reference_version = ?, current_step = 1, "
            "repo_commit = COALESCE(?, repo_commit) WHERE loop_id = ?",
            (version, seq, repo_commit, loop_id),
        )
        self.conn.commit()

    # -------------------------------------------------------------- handoff

    def _handoff_blockers(self, loop: Dict[str, Any], repo_commit: Optional[str]) -> List[str]:
        blockers: List[str] = []
        pass_state = loop["pass"]
        state = loop["active_state"]

        if self.latest_version(loop["claim_id"]) != loop["claim_version"]:
            blockers.append("reference: claim has a newer version; resync required")
        if repo_commit is not None and loop["repo_commit"] not in (None, repo_commit):
            blockers.append("reference: repository commit changed; resync required")

        missing = [s for s in STEPS if s not in pass_state["steps"]]
        if missing:
            blockers.append(f"receipt incomplete: missing {', '.join(missing)}")
        if not pass_state["evidence_ids"]:
            blockers.append("no evidence recorded in this pass")

        claim = self.claim(loop["claim_id"], loop["claim_version"])
        if state == FIELD:
            if not claim["text"].strip():
                blockers.append("no candidate saved")
            if not claim["scope"].strip():
                blockers.append("no scope saved")
        else:
            if pass_state["correction_version"] is None and not pass_state["counterproposal"]:
                blockers.append("no counterproposal or correction saved")
            if not pass_state["next_question"]:
                blockers.append("no next bounded question saved")
        return blockers

    def handoff(self, loop_id: str, *, repo_commit: Optional[str] = None) -> HandoffResult:
        """Reentry: switch FIELD<->VOID only when the handoff conditions hold.

        Otherwise the loop keeps its state and the blockers are recorded.
        """
        loop = self._loop(loop_id)
        state = loop["active_state"]
        other = VOID if state == FIELD else FIELD
        pass_state = loop["pass"]

        blockers = list(pass_state["holds"]) + self._handoff_blockers(loop, repo_commit)
        if blockers:
            self._log(loop_id, "handoff_held", {"state": state, "blockers": blockers})
            self.conn.commit()
            return HandoffResult(False, state, state, None, blockers)

        receipt_id = self._new_id("receipt", "R")
        body = {
            "question": loop["question"],
            "steps": pass_state["steps"],
            "candidate": self.claim(loop["claim_id"], loop["claim_version"])["text"],
            "evidence_ids": pass_state["evidence_ids"],
            "contradiction_ids": pass_state["contradiction_ids"],
            "correction_version": pass_state["correction_version"],
            "counterproposal": pass_state["counterproposal"],
            "next_question": pass_state["next_question"],
        }
        self.conn.execute(
            "INSERT INTO receipts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (receipt_id, loop_id, loop["pass_number"], state, loop["claim_id"],
             loop["claim_version"], loop["reference_version"], loop["repo_commit"],
             loop["incoming_receipt_id"], json.dumps(body, sort_keys=True)),
        )
        seq = self._log(loop_id, "handoff", {"from": state, "to": other, "receipt_id": receipt_id})
        self.conn.execute(
            "UPDATE loops SET active_state = ?, pass_number = pass_number + 1, current_step = 1, "
            "incoming_receipt_id = ?, last_receipt_id = ?, reference_version = ?, "
            "pass_json = ? WHERE loop_id = ?",
            (other, receipt_id, receipt_id, seq, json.dumps(_empty_pass()), loop_id),
        )
        self.conn.commit()
        return HandoffResult(True, state, other, receipt_id, [])

    def receipt(self, receipt_id: str) -> Dict[str, Any]:
        row = self.conn.execute(
            "SELECT * FROM receipts WHERE receipt_id = ?", (receipt_id,)
        ).fetchone()
        if row is None:
            raise ClaimLoopError(f"unknown receipt {receipt_id}")
        receipt = dict(row)
        receipt["body"] = json.loads(receipt.pop("body_json"))
        return receipt

    def receipts(self, loop_id: str) -> List[Dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT receipt_id FROM receipts WHERE loop_id = ? ORDER BY pass_number", (loop_id,)
        ).fetchall()
        return [self.receipt(r[0]) for r in rows]

    def reference_packet(self, loop_id: str) -> Dict[str, Any]:
        """Everything a pass reads at step 1: never an empty conversation."""
        loop = self._loop(loop_id)
        claim_id = loop["claim_id"]
        sources = self.conn.execute(
            "SELECT * FROM evidence WHERE claim_id = ? ORDER BY evidence_id", (claim_id,)
        ).fetchall()
        return {
            "machine": self.machine_record(loop_id).as_dict(),
            "question": loop["question"],
            "repo_commit": loop["repo_commit"],
            "claim": self.claim(claim_id, loop["claim_version"]),
            "claim_history": self.claim_versions(claim_id),
            "evidence": [dict(r) for r in sources],
            "open_contradictions": self.open_contradictions(claim_id),
            "incoming_receipt": (
                self.receipt(loop["incoming_receipt_id"]) if loop["incoming_receipt_id"] else None
            ),
            "children": self.children(loop_id),
        }

    # --------------------------------------------------------------- nesting

    def children(self, loop_id: str) -> List[str]:
        rows = self.conn.execute(
            "SELECT loop_id FROM loops WHERE parent_loop_id = ? ORDER BY loop_id", (loop_id,)
        ).fetchall()
        return [r[0] for r in rows]

    def return_upward(self, child_loop_id: str) -> str:
        """Attach the child's latest receipt to the parent's current pass."""
        child = self._loop(child_loop_id)
        if child["parent_loop_id"] is None:
            raise ClaimLoopError(f"{child_loop_id} has no parent loop")
        if child["last_receipt_id"] is None:
            raise ClaimLoopError(f"{child_loop_id} has no receipt to return")
        receipt = self.receipt(child["last_receipt_id"])
        child_claim = self.claim(receipt["claim_id"], receipt["claim_version"])
        content = json.dumps({
            "child_loop_id": child_loop_id,
            "receipt_id": receipt["receipt_id"],
            "state": receipt["state"],
            "claim": child_claim["text"],
            "scope": child_claim["scope"],
            "status": child_claim["status"],
        }, sort_keys=True)
        return self.add_evidence(
            child["parent_loop_id"], content, source=receipt["receipt_id"], kind="child_receipt",
        )
