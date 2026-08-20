"""Composable end-to-end Field workflow for sacrificial proof in Step 13."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from field.correction import CorrectionDecision, apply_test_evidence
from field.diff_check import inspect_diff
from field.editor import EditRequest, apply_edit
from field.git_safety import (
    CandidateWorkspace,
    KnownGood,
    capture_known_good,
    create_candidate_worktree,
    rollback_candidate,
)
from field.model_adapter import ModelAdapter, ModelRequest, run_model
from field.proposal import ProposalDraft, build_proposal
from field.repo_reader import read_repo_context
from field.review_packet import ReviewPacket, build_review_packet
from field.state import FieldState
from field.task_intake import parse_task_intake
from field.test_runner import TestEvidence, run_success_test


class WorkflowError(RuntimeError):
    """Raised when the composed Field workflow cannot continue safely."""


@dataclass(frozen=True)
class WorkflowResult:
    known_good: KnownGood
    candidate: CandidateWorkspace
    attempts: tuple[str, ...]
    final_state: FieldState
    review_packet: ReviewPacket | None


def _parse_model_plan(text: str) -> tuple[ProposalDraft, EditRequest]:
    try:
        payload = json.loads(text)
        draft = ProposalDraft(
            changes=(str(payload["intended_change"]),),
            reason=str(payload["reason"]),
            files_expected=tuple(str(item) for item in payload["files_expected"]),
            invariants=tuple(str(item) for item in payload["invariants"]),
            expected_result=str(payload["expected_result"]),
            success_test=str(payload["success_test"]),
        )
        edit_payload = payload["edit"]
        edit = EditRequest(
            path=str(edit_payload["path"]),
            new_content=str(edit_payload["new_content"]),
        )
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise WorkflowError("model response did not satisfy Step 13 plan schema") from exc
    return draft, edit


def _diff_failure_evidence(message: str) -> TestEvidence:
    return TestEvidence(
        command="diff-self-check",
        argv=("diff-self-check",),
        stdout="",
        stderr=message,
        exit_code=1,
        timed_out=False,
        passed=False,
    )


def run_field_workflow(
    *,
    source_repo: str | Path,
    candidate_path: str | Path,
    candidate_branch: str,
    goal_text: str,
    adapter: ModelAdapter,
) -> WorkflowResult:
    """Run one bounded Field task in an isolated candidate worktree."""
    source = Path(source_repo).resolve()
    task = parse_task_intake(goal_text)
    known_good = capture_known_good(source)
    context = read_repo_context(source, task)
    candidate = create_candidate_worktree(known_good, candidate_path, candidate_branch)

    state = FieldState(
        goal=goal_text,
        current_task=task.summary,
        attempt=1,
        max_attempts=3,
        last_action="workflow_started",
        last_result=None,
        next_action="build_candidate",
        active_branch=candidate_branch,
        active_step="13-sacrificial-repo",
    )
    attempts: list[str] = []

    while state.next_action != "blocked":
        prompt = {
            "task": task.summary,
            "scope": list(task.scope),
            "success_criteria": list(task.success_criteria),
            "repo_head": context.head,
            "repo_branch": context.branch,
            "files": {item.path: item.content for item in context.files},
            "attempt": state.attempt,
            "last_result": state.last_result,
        }
        response = run_model(
            adapter,
            ModelRequest(
                system_prompt=(
                    "Return one JSON plan with intended_change, reason, files_expected, "
                    "invariants, expected_result, success_test, and edit{path,new_content}."
                ),
                user_prompt=json.dumps(prompt, sort_keys=True),
            ),
        )
        draft, edit = _parse_model_plan(response.text)
        proposal = build_proposal(task, context, draft)
        apply_edit(candidate.worktree_root, proposal, edit)
        diff = inspect_diff(candidate.worktree_root, proposal)

        if not diff.matches_proposal:
            evidence = _diff_failure_evidence(
                f"unexpected={diff.unexpected_files}; missing={diff.missing_expected_files}"
            )
        else:
            evidence = run_success_test(candidate.worktree_root, proposal)

        outcome = apply_test_evidence(state, evidence)
        attempts.append(
            f"attempt {state.attempt}: {'PASS' if evidence.passed else 'FAIL'}; "
            f"decision={outcome.decision.value}"
        )
        state = outcome.state

        if outcome.decision is CorrectionDecision.PASS:
            packet = build_review_packet(
                goal=goal_text,
                task=task,
                proposal=proposal,
                diff_evidence=diff,
                test_evidence=evidence,
                attempts=tuple(attempts),
                remaining_uncertainty=("external architecture review required",),
                candidate_status="review_ready_candidate",
            )
            after = capture_known_good(source)
            if after.head != known_good.head or after.branch != known_good.branch:
                raise WorkflowError("source known-good identity changed during candidate work")
            return WorkflowResult(
                known_good=known_good,
                candidate=candidate,
                attempts=tuple(attempts),
                final_state=state,
                review_packet=packet,
            )

        rollback_candidate(candidate)

        if outcome.decision is CorrectionDecision.BLOCKED:
            break

    after = capture_known_good(source)
    if after.head != known_good.head or after.branch != known_good.branch:
        raise WorkflowError("source known-good identity changed during blocked workflow")
    return WorkflowResult(
        known_good=known_good,
        candidate=candidate,
        attempts=tuple(attempts),
        final_state=state,
        review_packet=None,
    )
