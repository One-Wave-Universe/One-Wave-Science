#!/usr/bin/env python3
"""OWATCH deterministic logic kernel v1.1.

Scope:
- sentence/span-level SUPPORTS and CONTRADICTS only
- deterministic derived proposals
- HOLD / UNRESOLVED
- runtime-only derived ledger with recursive stale-child prune
- route memory is navigation hysteresis, never authority
- no writes to Nodes/

Authority:
- canon/source edges carry source_class="canon" and derived=False
- only a non-derived canon CONTRADICTS edge may referee a derived SUPPORTS edge
- lineage/prune uses stable edge IDs, never semantic tuple keys
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

SOURCE_TYPES = {"SUPPORTS", "CONTRADICTS"}
DERIVED = "DERIVED"
HOLD = "HOLD"
UNRESOLVED = "UNRESOLVED"

REPO_NODE_CHAIN = (
    "GENERAL_REFERENCE_RULES.md",
    "AI_CANONICAL_START_HERE.md",
    "Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md",
    "One_Wave_Bench/hive-pipe/LOGIC_KERNEL.md",
    "One_Wave_Bench/hive-pipe/OWATCH_FULL_VISION.md",
)


def stable_hash(*parts: str, prefix: str = "edge") -> str:
    raw = "\x1f".join(parts).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(raw).hexdigest()[:20]}"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    kind: str
    reference: str
    intention: str
    consequence: str
    edge_id: str
    source_class: str = "canon"
    derived: bool = False
    parent_ids: tuple[str, ...] = ()
    rule_id: str = ""

    def key(self) -> str:
        return f"{self.kind}:{self.source}->{self.target}"

    def complete(self) -> bool:
        return all(
            isinstance(v, str) and v.strip()
            for v in (
                self.source,
                self.target,
                self.reference,
                self.intention,
                self.consequence,
                self.edge_id,
            )
        )

    def is_canon_referee(self) -> bool:
        return (
            self.kind == "CONTRADICTS"
            and self.source_class == "canon"
            and not self.derived
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
    pruned_derived: int = 0
    stale_children_pruned: int = 0
    referee_invalidations: int = 0

    def json(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Decision:
    status: str
    reason: str
    proposal: Edge | None = None
    bad_path_ids: tuple[str, ...] = ()

    def json(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "reason": self.reason,
            "proposal": asdict(self.proposal) if self.proposal else None,
            "bad_path_ids": list(self.bad_path_ids),
        }


@dataclass
class DerivedRecord:
    edge: Edge
    status: str = "ACTIVE"
    reason: str = ""

    def json(self) -> dict[str, Any]:
        return {
            "edge": asdict(self.edge),
            "status": self.status,
            "reason": self.reason,
        }


class DerivedLedger:
    """Disposable runtime ledger for derived edges only."""

    def __init__(self) -> None:
        self.records: dict[str, DerivedRecord] = {}

    def add(self, edge: Edge) -> None:
        if not edge.derived:
            raise ValueError("DerivedLedger accepts derived edges only")
        self.records.setdefault(edge.edge_id, DerivedRecord(edge=edge))

    def get(self, edge_id: str) -> DerivedRecord | None:
        return self.records.get(edge_id)

    def active(self, edge_id: str) -> bool:
        rec = self.records.get(edge_id)
        return bool(rec and rec.status == "ACTIVE")

    def active_children(self, parent_id: str) -> list[str]:
        return sorted(
            edge_id
            for edge_id, rec in self.records.items()
            if rec.status == "ACTIVE" and parent_id in rec.edge.parent_ids
        )

    def prune(self, edge_id: str, reason: str) -> tuple[list[str], list[str]]:
        """Idempotent cycle-safe prune.

        Returns (all_pruned_ids, descendant_ids).
        Mark-before-recurse prevents re-entrant double counts.
        """
        root = self.records.get(edge_id)
        if root is None or root.status != "ACTIVE":
            return [], []

        pruned: list[str] = []
        descendants: list[str] = []
        queue: list[tuple[str, bool]] = [(edge_id, False)]
        seen: set[str] = set()

        while queue:
            current, is_child = queue.pop(0)
            if current in seen:
                continue
            seen.add(current)

            rec = self.records.get(current)
            if rec is None or rec.status != "ACTIVE":
                continue

            # mark first; then traverse children
            rec.status = "PRUNED"
            rec.reason = reason if not is_child else f"stale parent pruned: {edge_id}"
            pruned.append(current)
            if is_child:
                descendants.append(current)

            for child_id in self.active_children(current):
                if child_id not in seen:
                    queue.append((child_id, True))

        return pruned, descendants

    def json(self) -> dict[str, Any]:
        return {
            edge_id: rec.json()
            for edge_id, rec in sorted(self.records.items())
        }


class RouteMemory:
    """Navigation hysteresis only.

    HOLD/wrong/pruned paths can decay.
    Positive boost is allowed only after explicit validation.
    """

    def __init__(self, scores: dict[str, float] | None = None) -> None:
        self.scores = dict(scores or {})
        self.boost_on_bad_path = 0

    def score(self, edge_id: str) -> float:
        return float(self.scores.get(edge_id, 0.0))

    def success(self, edge_id: str, amount: float = 0.20) -> None:
        self.scores[edge_id] = min(1.0, self.score(edge_id) + amount)

    def decay_bad(self, edge_id: str, amount: float = 0.25) -> None:
        self.scores[edge_id] = max(-1.0, self.score(edge_id) - amount)

    def hold(self, edge_id: str, amount: float = 0.12) -> None:
        self.scores[edge_id] = max(-1.0, self.score(edge_id) - amount)

    def bad_boost(self, edge_id: str, amount: float = 0.20) -> None:
        # Forbidden path. Exists only so the harness can prove it is never called.
        self.boost_on_bad_path += 1
        self.scores[edge_id] = min(1.0, self.score(edge_id) + amount)


def source_edge_id(raw: dict[str, Any]) -> str:
    explicit = str(raw.get("edge_id", "")).strip()
    if explicit:
        return explicit
    return stable_hash(
        str(raw.get("source", "")).strip(),
        str(raw.get("target", "")).strip(),
        str(raw.get("kind", "")).upper().strip(),
        str(raw.get("reference", "")).strip(),
        str(raw.get("intention", "")).strip(),
        str(raw.get("consequence", "")).strip(),
        str(raw.get("source_class", "canon")).strip(),
        prefix="src",
    )


def derived_edge_id(rule_id: str, parent_ids: Iterable[str], source: str,
                    target: str, kind: str) -> str:
    parents = tuple(sorted(str(x) for x in parent_ids))
    return stable_hash(
        rule_id,
        *parents,
        source,
        target,
        kind,
        prefix="drv",
    )


def edge_from_dict(raw: dict[str, Any]) -> Edge:
    kind = str(raw.get("kind", "")).upper().strip()
    derived = bool(raw.get("derived", False))
    if kind not in SOURCE_TYPES:
        raise ValueError(f"unsupported edge kind: {kind}")

    parent_ids = raw.get("parent_ids", ())
    if not isinstance(parent_ids, (list, tuple)):
        parent_ids = ()

    source_class = str(raw.get("source_class", "canon")).strip().lower() or "canon"
    if derived:
        source_class = "derived"

    return Edge(
        source=str(raw.get("source", "")).strip(),
        target=str(raw.get("target", "")).strip(),
        kind=kind,
        reference=str(raw.get("reference", "")).strip(),
        intention=str(raw.get("intention", "")).strip(),
        consequence=str(raw.get("consequence", "")).strip(),
        edge_id=source_edge_id(raw),
        source_class=source_class,
        derived=derived,
        parent_ids=tuple(str(x) for x in parent_ids),
        rule_id=str(raw.get("rule_id", "")).strip(),
    )


def make_derived(rule_id: str, parents: tuple[Edge, ...], source: str,
                 target: str, kind: str, intention: str) -> Edge:
    parent_ids = tuple(p.edge_id for p in parents)
    return Edge(
        source=source,
        target=target,
        kind=kind,
        reference="derived:" + "|".join(p.reference for p in parents),
        intention=intention,
        consequence="propose derived edge only; do not write Nodes/",
        edge_id=derived_edge_id(rule_id, parent_ids, source, target, kind),
        source_class="derived",
        derived=True,
        parent_ids=parent_ids,
        rule_id=rule_id,
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
                missing.append(f"{edge.edge_id} missing {name}")
    return missing


def contradiction_cycle(edges: Iterable[Edge]) -> tuple[bool, tuple[str, ...]]:
    contradictions = [e for e in edges if e.kind == "CONTRADICTS"]
    by_pair = {(e.source, e.target): e for e in contradictions}

    for edge in contradictions:
        if edge.source == edge.target:
            return True, (edge.edge_id,)

    for edge in contradictions:
        reverse = by_pair.get((edge.target, edge.source))
        if reverse is not None:
            return True, tuple(sorted({edge.edge_id, reverse.edge_id}))

    return False, ()


def derive_pair(a: Edge, b: Edge) -> Decision:
    # SUPPORTS(A,B) + SUPPORTS(B,C) -> derived SUPPORTS(A,C)
    if a.kind == "SUPPORTS" and b.kind == "SUPPORTS" and a.target == b.source:
        proposal = make_derived(
            "supports_transitivity_v1",
            (a, b),
            a.source,
            b.target,
            "SUPPORTS",
            "deterministic SUPPORTS transitivity proposal",
        )
        return Decision(DERIVED, "SUPPORTS transitivity", proposal)

    # CONTRADICTS(A,B) + SUPPORTS(C,A) -> derived CONTRADICTS(C,B)
    if a.kind == "CONTRADICTS" and b.kind == "SUPPORTS" and b.target == a.source:
        proposal = make_derived(
            "contradicts_propagation_v1",
            (a, b),
            b.source,
            a.target,
            "CONTRADICTS",
            "deterministic CONTRADICTS propagation proposal",
        )
        return Decision(DERIVED, "CONTRADICTS propagation", proposal)

    if b.kind == "CONTRADICTS" and a.kind == "SUPPORTS" and a.target == b.source:
        proposal = make_derived(
            "contradicts_propagation_v1",
            (a, b),
            a.source,
            b.target,
            "CONTRADICTS",
            "deterministic CONTRADICTS propagation proposal",
        )
        return Decision(DERIVED, "CONTRADICTS propagation", proposal)

    return Decision(UNRESOLVED, "no v1 deterministic rule applies")


def evaluate(edges: list[Edge]) -> Decision:
    missing = missing_metadata(edges)
    if missing:
        return Decision(
            HOLD,
            "; ".join(missing),
            bad_path_ids=tuple(e.edge_id for e in edges),
        )

    cycle, ids = contradiction_cycle(edges)
    if cycle:
        return Decision(
            HOLD,
            "circular CONTRADICTS route without canon referee; terminate",
            bad_path_ids=ids,
        )

    proposals: dict[str, Edge] = {}
    reasons: dict[str, str] = {}
    for i, left in enumerate(edges):
        for j, right in enumerate(edges):
            if i == j:
                continue
            decision = derive_pair(left, right)
            if decision.status == DERIVED and decision.proposal is not None:
                proposals.setdefault(decision.proposal.edge_id, decision.proposal)
                reasons.setdefault(decision.proposal.edge_id, decision.reason)

    derived_contra = [p for p in proposals.values() if p.kind == "CONTRADICTS"]
    by_pair = {(p.source, p.target): p for p in derived_contra}
    for proposal in derived_contra:
        reverse = by_pair.get((proposal.target, proposal.source))
        if reverse is not None:
            bad = tuple(sorted({
                *proposal.parent_ids,
                *reverse.parent_ids,
                proposal.edge_id,
                reverse.edge_id,
            }))
            return Decision(
                HOLD,
                "derived CONTRADICTS loop would close; terminate without route boost",
                bad_path_ids=bad,
            )

    if not proposals:
        return Decision(UNRESOLVED, "no v1 deterministic rule applies")

    selected_id = sorted(proposals)[0]
    return Decision(DERIVED, reasons[selected_id], proposals[selected_id])


def apply_memory(decision: Decision, memory: RouteMemory, receipt: Receipt) -> None:
    if decision.status == HOLD:
        receipt.holds += 1
        for edge_id in decision.bad_path_ids:
            before = memory.score(edge_id)
            memory.hold(edge_id)
            if memory.score(edge_id) < before:
                receipt.decayed_bad_paths += 1
        receipt.hysteresis_boost_on_bad_path = memory.boost_on_bad_path
    elif decision.status == UNRESOLVED:
        receipt.unresolved += 1


def validate_proposal(decision: Decision, expected: dict[str, Any] | None,
                      receipt: Receipt, memory: RouteMemory) -> bool:
    if decision.status != DERIVED or decision.proposal is None or expected is None:
        return False

    ok = all(
        str(getattr(decision.proposal, key)) == str(value)
        for key, value in expected.items()
        if key in {"source", "target", "kind"}
    )

    if ok:
        receipt.correct_derivations += 1
        for parent_id in decision.proposal.parent_ids:
            memory.success(parent_id)
    else:
        receipt.wrong_derivations += 1
        for parent_id in decision.proposal.parent_ids:
            memory.decay_bad(parent_id)
            receipt.decayed_bad_paths += 1

    receipt.hysteresis_boost_on_bad_path = memory.boost_on_bad_path
    return ok


def referee_matches(referee: Edge, derived: Edge) -> bool:
    return (
        referee.is_canon_referee()
        and derived.derived
        and derived.kind == "SUPPORTS"
        and referee.source == derived.source
        and referee.target == derived.target
    )


def invalidate_with_referee(referee: Edge, derived_edge_id_value: str,
                            ledger: DerivedLedger, memory: RouteMemory,
                            receipt: Receipt) -> dict[str, Any]:
    record = ledger.get(derived_edge_id_value)
    if record is None:
        return {
            "status": UNRESOLVED,
            "reason": "derived edge not found in runtime ledger",
            "pruned": [],
        }
    if record.status != "ACTIVE":
        return {
            "status": UNRESOLVED,
            "reason": "derived edge already inactive; invalidation is idempotent",
            "pruned": [],
        }
    if not referee_matches(referee, record.edge):
        return {
            "status": HOLD,
            "reason": "referee lacks canon/non-derived authority or pair does not match",
            "pruned": [],
        }

    receipt.referee_invalidations += 1
    receipt.wrong_derivations += 1

    # Decay the exact source routes that generated the wrong derivation.
    for parent_id in record.edge.parent_ids:
        before = memory.score(parent_id)
        memory.decay_bad(parent_id)
        if memory.score(parent_id) < before:
            receipt.decayed_bad_paths += 1

    pruned, descendants = ledger.prune(
        derived_edge_id_value,
        f"canon referee {referee.edge_id} contradicts derived SUPPORTS",
    )
    receipt.pruned_derived += len(pruned)
    receipt.stale_children_pruned += len(descendants)
    receipt.holds += 1
    receipt.hysteresis_boost_on_bad_path = memory.boost_on_bad_path

    return {
        "status": HOLD,
        "reason": "canon referee invalidated derived SUPPORTS; descendants pruned",
        "referee_edge_id": referee.edge_id,
        "invalidated_edge_id": derived_edge_id_value,
        "pruned": pruned,
        "stale_children": descendants,
    }


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

    require_wrong_zero = bool(corpus.get("require_wrong_derivations_zero", True))
    checks = {
        "all_statuses_match": all(r["status_ok"] for r in results),
        "all_expected_derivations_match": all(r["derivation_ok"] for r in results),
        "hysteresis_boost_on_bad_path_is_zero": receipt.hysteresis_boost_on_bad_path == 0,
        "wrong_derivations_policy": (
            receipt.wrong_derivations == 0
            if require_wrong_zero
            else receipt.wrong_derivations > 0
        ),
    }

    if corpus.get("require_hold", True):
        checks["at_least_one_hold"] = receipt.holds > 0
    if corpus.get("require_terminated_loop", True):
        checks["at_least_one_terminated_loop"] = receipt.terminated_loops > 0

    poison_edge_id = str(corpus.get("poison_probe_edge_id", "")).strip()
    poison_before = None
    poison_after = None
    poison_clean = True
    if poison_edge_id:
        poison_before = float(corpus.get("initial_route_memory", {}).get(poison_edge_id, 0.0))
        poison_after = memory.score(poison_edge_id)
        poison_clean = poison_after == poison_before
    checks["unrelated_route_not_poisoned"] = poison_clean

    passed = all(checks.values())

    return {
        "schema": "owatch-logic-kernel-receipt-v1.1",
        "passed": passed,
        "checks": checks,
        "receipt": receipt.json(),
        "route_memory_after": memory.scores,
        "poison_probe": {
            "edge_id": poison_edge_id,
            "before": poison_before,
            "after": poison_after,
        },
        "results": results,
        "repo_node_chain": list(REPO_NODE_CHAIN),
        "authority": {
            "route_memory_is_authority": False,
            "derived_is_canon": False,
            "canon_referee_required": True,
            "nodes_written": False,
        },
    }


def run_lifecycle_corpus(corpus: dict[str, Any]) -> dict[str, Any]:
    """Second independent corpus: derive -> referee -> retract -> prune descendants."""
    memory = RouteMemory(corpus.get("initial_route_memory", {}))
    receipt = Receipt()
    ledger = DerivedLedger()

    seed_edges = {
        str(name): edge_from_dict(raw)
        for name, raw in corpus.get("seed_edges", {}).items()
    }

    steps: list[dict[str, Any]] = []
    derived_names: dict[str, str] = {}

    for step in corpus.get("steps", []):
        action = str(step.get("action", "")).strip()

        if action == "derive":
            left_name = str(step["left"])
            right_name = str(step["right"])

            def resolve(name: str) -> Edge:
                if name in seed_edges:
                    return seed_edges[name]
                edge_id = derived_names.get(name)
                if edge_id:
                    rec = ledger.get(edge_id)
                    if rec is None:
                        raise RuntimeError(f"derived alias missing from ledger: {name}")
                    return rec.edge
                raise RuntimeError(f"unknown edge alias: {name}")

            left = resolve(left_name)
            right = resolve(right_name)
            decision = derive_pair(left, right)
            if decision.status != DERIVED or decision.proposal is None:
                steps.append({
                    "action": action,
                    "name": step.get("name"),
                    "status": decision.status,
                    "reason": decision.reason,
                })
                continue

            ledger.add(decision.proposal)
            alias = str(step.get("save_as", decision.proposal.edge_id))
            derived_names[alias] = decision.proposal.edge_id
            steps.append({
                "action": action,
                "name": step.get("name"),
                "status": DERIVED,
                "saved_as": alias,
                "edge_id": decision.proposal.edge_id,
                "edge": asdict(decision.proposal),
            })

        elif action == "referee":
            referee = seed_edges[str(step["referee"])]
            target_alias = str(step["target"])
            target_id = derived_names.get(target_alias, target_alias)
            outcome = invalidate_with_referee(
                referee,
                target_id,
                ledger,
                memory,
                receipt,
            )
            steps.append({
                "action": action,
                "name": step.get("name"),
                **outcome,
            })

        else:
            steps.append({
                "action": action,
                "name": step.get("name"),
                "status": HOLD,
                "reason": f"unknown lifecycle action: {action}",
            })
            receipt.holds += 1

    expected = corpus.get("expect", {})
    required_pruned_aliases = [
        str(x) for x in expected.get("pruned_aliases", [])
    ]
    required_pruned_ids = [
        derived_names.get(alias, alias)
        for alias in required_pruned_aliases
    ]

    poison_edge_id = str(corpus.get("poison_probe_edge_id", "")).strip()
    poison_before = (
        float(corpus.get("initial_route_memory", {}).get(poison_edge_id, 0.0))
        if poison_edge_id else None
    )
    poison_after = memory.score(poison_edge_id) if poison_edge_id else None

    checks = {
        "wrong_derivations_gt_zero": receipt.wrong_derivations > 0,
        "pruned_derived_gt_zero": receipt.pruned_derived > 0,
        "stale_children_pruned_gt_zero": receipt.stale_children_pruned > 0,
        "hysteresis_boost_on_bad_path_is_zero": receipt.hysteresis_boost_on_bad_path == 0,
        "unrelated_route_not_poisoned": poison_before == poison_after,
        "required_derived_edges_pruned": all(
            (ledger.get(edge_id) is not None and ledger.get(edge_id).status == "PRUNED")
            for edge_id in required_pruned_ids
        ),
        "canon_referee_used": receipt.referee_invalidations > 0,
    }

    return {
        "schema": "owatch-logic-kernel-lifecycle-receipt-v1",
        "passed": all(checks.values()),
        "checks": checks,
        "receipt": receipt.json(),
        "steps": steps,
        "ledger": ledger.json(),
        "route_memory_after": memory.scores,
        "poison_probe": {
            "edge_id": poison_edge_id,
            "before": poison_before,
            "after": poison_after,
        },
        "repo_node_chain": list(REPO_NODE_CHAIN),
        "authority": {
            "route_memory_is_authority": False,
            "derived_is_canon": False,
            "canon_referee_required": True,
            "nodes_written": False,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("corpus", type=Path)
    ap.add_argument("--receipt", type=Path)
    args = ap.parse_args()

    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    if str(corpus.get("mode", "")).lower() == "lifecycle":
        result = run_lifecycle_corpus(corpus)
    else:
        result = run_corpus(corpus)

    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(raw, encoding="utf-8")
    print(raw, end="")
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
