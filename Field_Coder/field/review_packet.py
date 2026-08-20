"""External-review packet for Field Coder Step 11."""

from __future__ import annotations

from dataclasses import dataclass

from field.diff_check import DiffEvidence
from field.proposal import ImplementationProposal
from field.task_intake import TaskSpec
from field.test_runner import TestEvidence


class ReviewPacketError(ValueError):
    """Raised when Field attempts to emit an invalid review packet."""


PENDING_EXTERNAL_REVIEW = "PENDING_EXTERNAL_REVIEW"
_FORBIDDEN_SELF_APPROVAL = {
    "APPROVED",
    "ARCHITECTURE_APPROVED",
    "VOID_APPROVED",
    "ADMIN_APPROVED",
}


@dataclass(frozen=True)
class ReviewPacket:
    goal: str
    task: TaskSpec
    proposal: ImplementationProposal
    files_changed: tuple[str, ...]
    unified_diff: str
    test_evidence: TestEvidence
    attempts: tuple[str, ...]
    remaining_uncertainty: tuple[str, ...]
    candidate_status: str
    architecture_verdict: str = PENDING_EXTERNAL_REVIEW


def build_review_packet(
    *,
    goal: str,
    task: TaskSpec,
    proposal: ImplementationProposal,
    diff_evidence: DiffEvidence,
    test_evidence: TestEvidence,
    attempts: tuple[str, ...],
    remaining_uncertainty: tuple[str, ...],
    candidate_status: str,
) -> ReviewPacket:
    """Build an evidence packet that explicitly requires external architecture review."""
    if not isinstance(goal, str) or not goal.strip():
        raise ReviewPacketError("goal must not be empty")
    task.validate()
    if not diff_evidence.matches_proposal:
        raise ReviewPacketError("review packet requires proposal-matching diff evidence")
    if not diff_evidence.changed_files:
        raise ReviewPacketError("review packet requires changed-file evidence")
    if not diff_evidence.unified_diff.strip():
        raise ReviewPacketError("review packet requires unified diff evidence")
    if not attempts or any(not item.strip() for item in attempts):
        raise ReviewPacketError("attempt evidence must not be empty")
    if any(not item.strip() for item in remaining_uncertainty):
        raise ReviewPacketError("remaining uncertainty contains an empty item")
    normalized_status = candidate_status.strip().upper()
    if not normalized_status:
        raise ReviewPacketError("candidate status must not be empty")
    if normalized_status in _FORBIDDEN_SELF_APPROVAL or "APPROVED" in normalized_status:
        raise ReviewPacketError("Field cannot approve its own architecture")

    return ReviewPacket(
        goal=goal.strip(),
        task=task,
        proposal=proposal,
        files_changed=diff_evidence.changed_files,
        unified_diff=diff_evidence.unified_diff,
        test_evidence=test_evidence,
        attempts=tuple(item.strip() for item in attempts),
        remaining_uncertainty=tuple(item.strip() for item in remaining_uncertainty),
        candidate_status=normalized_status,
        architecture_verdict=PENDING_EXTERNAL_REVIEW,
    )
