"""CPU-native 3-loop triad. Jetson is not required."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

DC_CHOICES = ("FIELD", "VOID")
AC_MOVES = ("DOWN", "HOLD", "UP")
QC_VIEWS = ("DIRECTION", "PHASE", "STRENGTH", "REFERENCE")
QC_ACTIONS = ("INWARD", "OUTWARD", "ACROSS", "OVER")
VERBS = ("Idle", "Primed", "Executing", "Vectoring", "Resolving")


@dataclass(frozen=True)
class TriadState:
    dc: str
    ac: str
    qc_view: str
    qc_action: Optional[str]
    verb: str
    committed: bool
    device: str = "CPU_REFERENCE"


def cycle(dc: str, ac: str, qc_view: str, qc_action: Optional[str] = None, verb: str = "Executing") -> TriadState:
    if dc not in DC_CHOICES:
        raise ValueError("dc must be FIELD or VOID")
    if ac not in AC_MOVES:
        raise ValueError("ac must be DOWN HOLD or UP")
    if qc_view not in QC_VIEWS:
        raise ValueError("unknown qc view")
    if qc_action is not None and qc_action not in QC_ACTIONS:
        raise ValueError("unknown qc action")
    if verb not in VERBS:
        raise ValueError("unknown verb")
    committed = dc == "VOID" and verb == "Resolving"
    return TriadState(
        dc=dc,
        ac=ac,
        qc_view=qc_view,
        qc_action=qc_action,
        verb=verb,
        committed=committed,
        device="CPU_REFERENCE",
    )


def stop() -> TriadState:
    return cycle("VOID", "HOLD", "REFERENCE", "OVER", "Resolving")
