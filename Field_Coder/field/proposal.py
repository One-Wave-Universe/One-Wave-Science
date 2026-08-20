"""Grounded single-change proposal contract for Field Coder Step 05."""

from __future__ import annotations

from dataclasses import dataclass

from field.repo_reader import RepoContext
from field.task_intake import TaskSpec


class ProposalError(ValueError):
    """Raised when a candidate implementation proposal violates the contract."""


@dataclass(frozen=True)
class ProposalDraft:
    changes: tuple[str, ...]
    reason: str
    files_expected: tuple[str, ...]
    invariants: tuple[str, ...]
    expected_result: str
    success_test: str


@dataclass(frozen=True)
class ImplementationProposal:
    intended_change: str
    reason: str
    files_expected: tuple[str, ...]
    invariants: tuple[str, ...]
    expected_result: str
    success_test: str


def _require_text(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProposalError(f"{label} must not be empty")
    return value.strip()


def build_proposal(
    task: TaskSpec,
    context: RepoContext,
    draft: ProposalDraft,
) -> ImplementationProposal:
    """Validate and normalize exactly one proposal grounded in task/context evidence."""
    task.validate()

    if len(draft.changes) != 1:
        raise ProposalError("proposal must contain exactly one intended change")
    intended_change = _require_text(draft.changes[0], "intended change")
    reason = _require_text(draft.reason, "reason")
    expected_result = _require_text(draft.expected_result, "expected result")
    success_test = _require_text(draft.success_test, "success test")

    if not draft.files_expected:
        raise ProposalError("files expected must not be empty")
    if not draft.invariants:
        raise ProposalError("invariants must not be empty")
    if any(not item.strip() for item in draft.invariants):
        raise ProposalError("invariants contain an empty item")

    task_scope = set(task.scope)
    context_files = {item.path for item in context.files}
    normalized_files = tuple(item.strip() for item in draft.files_expected)
    if any(not item for item in normalized_files):
        raise ProposalError("files expected contain an empty item")

    for path in normalized_files:
        if path not in task_scope:
            raise ProposalError(f"proposal target outside task scope: {path}")
        if path not in context_files:
            raise ProposalError(f"proposal target missing from repo context: {path}")

    return ImplementationProposal(
        intended_change=intended_change,
        reason=reason,
        files_expected=normalized_files,
        invariants=tuple(item.strip() for item in draft.invariants),
        expected_result=expected_result,
        success_test=success_test,
    )
