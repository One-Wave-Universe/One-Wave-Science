#!/usr/bin/env python3
"""OWATCH deterministic logic kernel v1.

This is NOT canon and does not write Nodes/.
It evaluates sentence-span relationships and emits only:
- DERIVED proposal edges
- HOLD
- UNRESOLVED

v1 supported source edge types:
- SUPPORTS
- CONTRADICTS

Every source edge must include:
reference, intention, consequence.
Missing any -> HOLD.

Route memory is observational input/output only. It is never authority.
Bad/HOLD paths are never strengthened by this kernel.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import argparse
import json
from pathlib import Path
from typing import Any, Iterable

SOURCE_TYPES = {"SUPPORTS", "CONTRADICTS"}
DERIVED = "DERIVED"
HOLD = "HOLD"
UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    kind: str
    reference: str
    intention: str
    consequence: str
    derived: bool = False
    parents: tuple[str, ...] = ()

    def key(self) -> str:
        return f"{self.kind}:{self.source}->{self.target}"

    def complete(self) -> bool:
        return all(
            isinstance(v, str) and v.strip()
            for v in (self.source, self.target, self.reference, self.intention, self.consequence)
        )


@dataclass
class Receipt:
    correct_derivations: int = 0
    wrong_derivations: int = 0
    holds: int = 0
    unresolved: int = 0
    hysteresis_boost_on_bad_path: int = 0
    decayed_bad_paths: int = 0
    terminated_loops: int = 0

    def json(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Decision:
    status: str
    reason: str
    proposal: Edge | None = None
    bad_path_keys: tuple[str, ...] = ()

    def json(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "reason": self.reason,
            "proposal": asdict(self.proposal) if self.proposal else None,
            "bad_path_keys": list(self.bad_path_keys),
        }


class RouteMemory:
    """Minimal hysteresis receipt state for the kernel harness.

    The kernel never boosts on HOLD/wrong paths.
    Success boost is explicit and separate from inference correctness.
    """

    def __init__(self, scores: dict[str, float] | None = None) -> None:
        self.scores = dict(scores or {})
        self.boost_on_bad_path = 0

    def score(self, key: str) -> float:
        return float(self.scores.get(key, 0.0))

    def success(self, key: str, amount: float = 0.20) -> None:
        self.scores[key] = min(1.0, self.score(key) + amount)

    def decay_bad(self, key: str, amount: float = 0.25) -> None:
        self.scores[key] = max(-1.0, self.score(key) - amount)

    def hold(self, key: str, amount: float = 0.12) -> None:
        self.scores[key] = max(-1.0, self.score(key) - amount)

    def bad_boost(self, key: str, amount: float = 0.20) -> None:
        # This exists only so the harness can prove the forbidden action
        # remains unused.
        self.boost_on_bad_path += 1
        self.scores[key] = min(1.0, self.score(key) + amount)


def edge_from_dict(raw: dict[str, Any]) -> Edge:
    kind = str(raw.get("kind", "")).upper().strip()
    if kind not in SOURCE_TYPES and not bool(raw.get("derived", False)):
        raise ValueError(f"unsupported source edge kind: {kind}")
    parents = raw.get("parents", ())
    if not isinstance(parents, (list, tuple)):
        parents = ()
    return Edge(
        source=str(raw.get("source", "")).strip(),
        target=str(raw.get("target", "")).strip(),
        kind=kind,
        reference=str(raw.get("reference", "")).strip(),
        intention=str(raw.get("intention", "")).strip(),
        consequence=str(raw.get("consequence", "")).strip(),
        derived=bool(raw.get("derived", False)),
        parents=tuple(str(x) for x in parents),
    )


def missing_metadata(edges: Iterable[Edge]) -> list[str]:
    missing: list[str] = []
    for edge in edges:
        for name, value in (
            ("reference", edge.reference),
            ("intention", edge.intention),
            ("consequence", edge.consequence),
        ):
            if not value.strip():
                missing.append(f"{edge.key()} missing {name}")
    return missing


def contradiction_cycle(edges: Iterable[Edge]) -> tuple[bool, tuple[str, ...]]:
    """Detect v1 contradiction self-loop or 2-node cycle.

    Spec text says A⇔B⇔A; v1 intentionally keeps this bounded to self/2-cycle.
    """
    contradictions = [e for e in edges if e.kind == "CONTRADICTS"]
    by_pair = {(e.source, e.target): e for e in contradictions}

    for e in contradictions:
        if e.source == e.target:
            return True, (e.key(),)

    for e in contradictions:
        rev = by_pair.get((e.target, e.source))
        if rev is not None:
            return True, tuple(sorted({e.key(), rev.key()}))

    return False, ()


def derive_pair(a: Edge, b: Edge) -> Decision:
    """Apply exactly one deterministic v1 rule to an ordered pair."""
    # Rule 1:
    # SUPPORTS(A,B) + SUPPORTS(B,C) -> derived SUPPORTS(A,C)
    if a.kind == "SUPPORTS" and b.kind == "SUPPORTS" and a.target == b.source:
        proposal = Edge(
            source=a.source,
            target=b.target,
            kind="SUPPORTS",
            reference=f"derived:{a.reference}|{b.reference}",
            intention="deterministic SUPPORTS transitivity proposal",
            consequence="propose derived SUPPORTS edge only; do not write Nodes/",
            derived=True,
            parents=(a.key(), b.key()),
        )
        return Decision(DERIVED, "SUPPORTS transitivity", proposal)

    # Rule 2:
    # CONTRADICTS(A,B) + SUPPORTS(C,A) -> derived CONTRADICTS(C,B)
    if a.kind == "CONTRADICTS" and b.kind == "SUPPORTS" and b.target == a.source:
        proposal = Edge(
            source=b.source,
            target=a.target,
            kind="CONTRADICTS",
            reference=f"derived:{a.reference}|{b.reference}",
            intention="deterministic CONTRADICTS propagation proposal",
            consequence="propose derived CONTRADICTS edge only; do not write Nodes/",
            derived=True,
            parents=(a.key(), b.key()),
        )
        return Decision(DERIVED, "CONTRADICTS propagation", proposal)

    if b.kind == "CONTRADICTS" and a.kind == "SUPPORTS" and a.target == b.source:
        proposal = Edge(
            source=a.source,
            target=b.target,
            kind="CONTRADICTS",
            reference=f"derived:{a.reference}|{b.reference}",
            intention="deterministic CONTRADICTS propagation proposal",
            consequence="propose derived CONTRADICTS edge only; do not write Nodes/",
            derived=True,
            parents=(a.key(), b.key()),
        )
        return Decision(DERIVED, "CONTRADICTS propagation", proposal)

    return Decision(UNRESOLVED, "no v1 deterministic rule applies")


def evaluate(edges: list[Edge]) -> Decision:
    """Return one bounded v1 decision.

    Order of operations is authority first:
    1. metadata completeness
    2. direct contradiction loop termination
    3. deterministic derivation
    4. unresolved
    """
    missing = missing_metadata(edges)
    if missing:
        return Decision(HOLD, "; ".join(missing), bad_path_keys=tuple(e.key() for e in edges))

    cycle, keys = contradiction_cycle(edges)
    if cycle:
        return Decision(
            HOLD,
            "circular CONTRADICTS route without third referee; terminate",
            bad_path_keys=keys,
        )

    proposals: list[Edge] = []
    reasons: list[str] = []
    for i, left in enumerate(edges):
        for j, right in enumerate(edges):
            if i == j:
                continue
            decision = derive_pair(left, right)
            if decision.status == DERIVED and decision.proposal is not None:
                if decision.proposal.key() not in {p.key() for p in proposals}:
                    proposals.append(decision.proposal)
                    reasons.append(decision.reason)

    # Rule 4:
    # two derived CONTRADICTS that close a loop -> HOLD, no strengthen.
    derived_contra = [p for p in proposals if p.kind == "CONTRADICTS"]
    pairs = {(p.source, p.target): p for p in derived_contra}
    for p in derived_contra:
        rev = pairs.get((p.target, p.source))
        if rev is not None:
            bad = tuple(sorted({*p.parents, *rev.parents, p.key(), rev.key()}))
            return Decision(
                HOLD,
                "derived CONTRADICTS loop would close; terminate without route boost",
                bad_path_keys=bad,
            )

    if not proposals:
        return Decision(UNRESOLVED, "no v1 deterministic rule applies")

    # v1 emits only one proposal per evaluation so result ordering is stable.
    proposals.sort(key=lambda e: e.key())
    return Decision(DERIVED, reasons[0], proposals[0])


def apply_memory(decision: Decision, memory: RouteMemory, receipt: Receipt) -> None:
    """Memory policy frozen by LOGIC_KERNEL.md.

    HOLD/wrong path => decay.
    HOLD => zero boost.
    UNRESOLVED => no boost, no penalty.
    DERIVED => no automatic boost here; higher-authority validation must decide
               whether the route was actually correct/useful.
    """
    if decision.status == HOLD:
        receipt.holds += 1
        if decision.bad_path_keys:
            for key in decision.bad_path_keys:
                before = memory.score(key)
                memory.hold(key)
                if memory.score(key) < before:
                    receipt.decayed_bad_paths += 1
        receipt.hysteresis_boost_on_bad_path = memory.boost_on_bad_path
    elif decision.status == UNRESOLVED:
        receipt.unresolved += 1


def validate_proposal(decision: Decision, expected: dict[str, Any] | None, receipt: Receipt,
                      memory: RouteMemory) -> bool:
    if decision.status != DERIVED or decision.proposal is None:
        return False

    if expected is None:
        return False

    ok = all(
        str(getattr(decision.proposal, key)) == str(value)
        for key, value in expected.items()
        if key in {"source", "target", "kind"}
    )
    if ok:
        receipt.correct_derivations += 1
        # Positive memory is allowed only after external/higher-authority validation.
        for parent in decision.proposal.parents:
            memory.success(parent)
    else:
        receipt.wrong_derivations += 1
        for parent in decision.proposal.parents:
            memory.decay_bad(parent)
            receipt.decayed_bad_paths += 1

    receipt.hysteresis_boost_on_bad_path = memory.boost_on_bad_path
    return ok


def run_case(case: dict[str, Any], memory: RouteMemory, receipt: Receipt) -> dict[str, Any]:
    edges = [edge_from_dict(e) for e in case.get("edges", [])]
    decision = evaluate(edges)
    apply_memory(decision, memory, receipt)

    expected_status = str(case.get("expect_status", "")).upper()
    status_ok = not expected_status or decision.status == expected_status

    expected_proposal = case.get("expect_proposal")
    derivation_ok = True
    if decision.status == DERIVED:
        derivation_ok = validate_proposal(
            decision,
            expected_proposal if isinstance(expected_proposal, dict) else None,
            receipt,
            memory,
        )
    elif expected_proposal is not None:
        derivation_ok = False

    if decision.status == HOLD and "terminate" in decision.reason.lower():
        receipt.terminated_loops += 1

    return {
        "name": case.get("name", "unnamed"),
        "decision": decision.json(),
        "status_ok": status_ok,
        "derivation_ok": derivation_ok,
    }


def run_corpus(corpus: dict[str, Any]) -> dict[str, Any]:
    memory = RouteMemory(corpus.get("initial_route_memory", {}))
    receipt = Receipt()
    results = [run_case(case, memory, receipt) for case in corpus.get("cases", [])]

    checks = {
        "all_statuses_match": all(r["status_ok"] for r in results),
        "all_expected_derivations_match": all(r["derivation_ok"] for r in results),
        "hysteresis_boost_on_bad_path_is_zero": receipt.hysteresis_boost_on_bad_path == 0,
        "wrong_derivations_is_zero": receipt.wrong_derivations == 0,
        "at_least_one_hold": receipt.holds > 0,
        "at_least_one_terminated_loop": receipt.terminated_loops > 0,
    }

    # Poison check is explicit: unrelated path score must remain unchanged.
    poison_key = str(corpus.get("poison_probe_key", "")).strip()
    poison_before = None
    poison_after = None
    poison_clean = True
    if poison_key:
        poison_before = float(corpus.get("initial_route_memory", {}).get(poison_key, 0.0))
        poison_after = memory.score(poison_key)
        poison_clean = poison_after == poison_before
    checks["unrelated_route_not_poisoned"] = poison_clean

    passed = all(checks.values())

    return {
        "schema": "owatch-logic-kernel-receipt-v1",
        "passed": passed,
        "checks": checks,
        "receipt": receipt.json(),
        "route_memory_after": memory.scores,
        "poison_probe": {
            "key": poison_key,
            "before": poison_before,
            "after": poison_after,
        },
        "results": results,
        "authority": {
            "route_memory_is_authority": False,
            "derived_is_canon": False,
            "nodes_written": False,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("corpus", type=Path)
    ap.add_argument("--receipt", type=Path)
    args = ap.parse_args()

    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    result = run_corpus(corpus)

    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(raw, encoding="utf-8")
    print(raw, end="")
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
