"""Step 11 external-review packet verification."""

from dataclasses import FrozenInstanceError
from pathlib import Path
import sys

FIELD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIELD_ROOT))

from field.diff_check import DiffEvidence
from field.proposal import ImplementationProposal
from field.review_packet import (
    PENDING_EXTERNAL_REVIEW,
    ReviewPacketError,
    build_review_packet,
)
from field.task_intake import TaskSpec
from field.test_runner import TestEvidence


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def make_inputs():
    task = TaskSpec(
        summary="change fixture output",
        scope=("fixture.py",),
        success_criteria=("fixture test passes",),
    )
    proposal = ImplementationProposal(
        intended_change="change fixture output once",
        reason="requested bounded change",
        files_expected=("fixture.py",),
        invariants=("unrelated files unchanged",),
        expected_result="fixture output updated",
        success_test="python3 -m pytest -q",
    )
    diff = DiffEvidence(
        changed_files=("fixture.py",),
        unexpected_files=(),
        missing_expected_files=(),
        unified_diff="--- a/fixture.py\n+++ b/fixture.py\n-old\n+new\n",
        matches_proposal=True,
    )
    test = TestEvidence(
        command="python3 -m pytest -q",
        argv=("python3", "-m", "pytest", "-q"),
        stdout="1 passed\n",
        stderr="",
        exit_code=0,
        timed_out=False,
        passed=True,
    )
    return task, proposal, diff, test


def main() -> int:
    task, proposal, diff, test = make_inputs()
    packet = build_review_packet(
        goal="Update one fixture safely",
        task=task,
        proposal=proposal,
        diff_evidence=diff,
        test_evidence=test,
        attempts=("attempt 1: pass",),
        remaining_uncertainty=("external architecture review still required",),
        candidate_status="review_ready_candidate",
    )

    require(packet.goal == "Update one fixture safely", repr(packet.goal))
    require(packet.task == task, repr(packet.task))
    require(packet.proposal == proposal, repr(packet.proposal))
    require(packet.files_changed == ("fixture.py",), repr(packet.files_changed))
    require(packet.unified_diff == diff.unified_diff, repr(packet.unified_diff))
    require(packet.test_evidence == test, repr(packet.test_evidence))
    require(packet.attempts == ("attempt 1: pass",), repr(packet.attempts))
    require(packet.remaining_uncertainty, repr(packet.remaining_uncertainty))
    require(packet.candidate_status == "REVIEW_READY_CANDIDATE", packet.candidate_status)
    require(packet.architecture_verdict == PENDING_EXTERNAL_REVIEW, packet.architecture_verdict)
    print("PASS: complete external-review packet generated")

    try:
        packet.architecture_verdict = "APPROVED"
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("review packet architecture verdict was mutable")
    print("PASS: architecture verdict is immutable pending external review")

    try:
        build_review_packet(
            goal="Update one fixture safely",
            task=task,
            proposal=proposal,
            diff_evidence=diff,
            test_evidence=test,
            attempts=("attempt 1: pass",),
            remaining_uncertainty=(),
            candidate_status="APPROVED",
        )
    except ReviewPacketError:
        pass
    else:
        raise AssertionError("Field self-approval candidate status was accepted")
    print("PASS: Field self-approval status rejected")

    bad_diff = DiffEvidence(
        changed_files=("fixture.py", "extra.py"),
        unexpected_files=("extra.py",),
        missing_expected_files=(),
        unified_diff="diff evidence",
        matches_proposal=False,
    )
    try:
        build_review_packet(
            goal="Update one fixture safely",
            task=task,
            proposal=proposal,
            diff_evidence=bad_diff,
            test_evidence=test,
            attempts=("attempt 1: mismatch",),
            remaining_uncertainty=(),
            candidate_status="review_ready_candidate",
        )
    except ReviewPacketError:
        pass
    else:
        raise AssertionError("proposal-mismatching diff was accepted for review-ready packet")
    print("PASS: mismatching diff rejected from review-ready packet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
