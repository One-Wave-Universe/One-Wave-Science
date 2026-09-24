#!/usr/bin/env python3
"""Automated reference and quality gate for Composite Agent Lab.

Quality is evidence-backed and rubric-driven. "A+" is a configured acceptance
band, never a self-awarded claim. Failed dimensions generate targeted repair
tasks and re-enter the loop.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any

@dataclass
class Criterion:
    name: str
    weight: float
    score: float = 0.0
    evidence: list[str] = field(default_factory=list)
    required: bool = True
    note: str = ""

@dataclass
class QualityReport:
    criteria: list[Criterion]
    total: float
    accepted: bool
    band: str
    repair_tasks: list[dict[str,Any]]
    missing_references: list[str]

DEFAULT_RUBRIC = [
    ("reference_coverage", 0.22),
    ("factual_support", 0.18),
    ("requirement_match", 0.18),
    ("test_or_validation", 0.18),
    ("void_review", 0.12),
    ("clarity_and_usability", 0.07),
    ("drift_control", 0.05),
]

def _band(score: float) -> str:
    if score >= 0.95: return "A+"
    if score >= 0.90: return "A"
    if score >= 0.85: return "B+"
    if score >= 0.80: return "B"
    return "REPAIR"

def evaluate(payload: dict[str,Any], threshold: float = 0.95) -> QualityReport:
    refs=payload.get("references",[])
    claims=payload.get("claims",[])
    tests=payload.get("tests",[])
    requirements=payload.get("requirements",[])
    void=payload.get("void_review",{})
    drift=payload.get("drift",{})
    usable=payload.get("usable",False)

    cited_claims=sum(1 for c in claims if c.get("reference_ids"))
    ref_cov=(cited_claims/len(claims)) if claims else (1.0 if refs else 0.0)
    supported=sum(1 for c in claims if c.get("supported") is True)
    factual=(supported/len(claims)) if claims else 1.0
    req_done=sum(1 for r in requirements if r.get("met") is True)
    req_score=(req_done/len(requirements)) if requirements else 1.0
    test_score=1.0 if tests and all(t.get("passed") is True for t in tests) else 0.0 if not tests else sum(1 for t in tests if t.get("passed") is True)/len(tests)
    void_score=1.0 if str(void.get("decision","")).upper()=="ALLOW" and void.get("evidence_checked",False) else 0.0
    clarity=1.0 if usable else 0.0
    drift_score=1.0 if drift.get("checked") and not drift.get("detected") else 0.0

    values={
      "reference_coverage":ref_cov,
      "factual_support":factual,
      "requirement_match":req_score,
      "test_or_validation":test_score,
      "void_review":void_score,
      "clarity_and_usability":clarity,
      "drift_control":drift_score,
    }
    criteria=[]
    total=0.0
    for name,weight in DEFAULT_RUBRIC:
        sc=max(0.0,min(1.0,float(values[name])))
        total += sc*weight
        criteria.append(Criterion(name=name,weight=weight,score=sc,evidence=[]))

    missing=[]
    for c in claims:
        if not c.get("reference_ids"): missing.append(str(c.get("id") or c.get("text") or "unnamed claim"))

    repairs=[]
    for c in criteria:
        if c.score < 1.0:
            repairs.append({"criterion":c.name,"gap":round(1.0-c.score,3),"task":f"Improve {c.name} using new evidence or a targeted correction; do not rewrite passing dimensions."})
    if missing:
        repairs.append({"criterion":"reference_coverage","task":"Attach source IDs/paths and exact supporting evidence to every listed claim.","items":missing})

    accepted=total >= threshold and not missing and test_score==1.0 and void_score==1.0 and req_score==1.0
    return QualityReport(criteria=criteria,total=round(total,4),accepted=accepted,band=_band(total),repair_tasks=repairs,missing_references=missing)
