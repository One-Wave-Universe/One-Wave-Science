"""The router loop: orchestrator between State Machine A and State Machine
B, dispatching to the Phase 1 problem builder as a worker.

    STATE MACHINE A <-> ROUTER LOOP <-> STATE MACHINE B
                            |
                    Phase 1 worker (parser.core.build_problem)

The router loop is explicitly NOT a third state machine. It holds its own
small bookkeeping (curriculum position, current route, repeated-error
tracking) as instance fields on one RouterLoop object -- never as
module-level/global state -- so two independently constructed RouterLoop
instances given the same config, base_seed, and sequence of attempts
always produce the same sequence of RouteDecisions.
"""

from __future__ import annotations

from collections.abc import Mapping

from . import policy
from . import recall_integration
from . import state_machine_a as sm_a
from . import state_machine_b as sm_b
from .models import (
    EvaluationEvidence,
    EvaluationLifecycle,
    EvaluatorState,
    LearnerAttempt,
    LearnerTaskState,
    RouteDecision,
    initial_evaluator_state,
    initial_task_state,
)
from ..parser.core import build_problem
from ..parser.models import GeneratedProblem, RulePacket
from ..recall import worker as recall_worker
from ..recall.models import RecallConfig, RecallRecord


class RouterLoop:
    """One learner session's orchestrator. All state is instance state --
    see the module docstring for why that matters for determinism."""

    def __init__(
        self,
        *,
        config: policy.PolicyConfig,
        base_seed: int,
        packet_id_prefix: str = "cycle",
        recall_config: RecallConfig | None = None,
        recall_inverses: Mapping[str, str] | None = None,
    ):
        self.config = config
        self.base_seed = base_seed
        self.packet_id_prefix = packet_id_prefix
        self.task_state: LearnerTaskState = initial_task_state()
        self.evaluator_state: EvaluatorState = initial_evaluator_state()
        self.route: RouteDecision = policy.initial_route_decision(config, seed=base_seed)
        self.curriculum_index: int = 0
        self.cycle_count: int = 0
        self._last_error_kind: str | None = None
        self._consecutive_same_error: int = 0
        self._problems_by_id: dict[str, GeneratedProblem] = {}

        # Phase 3: recall bookkeeping, instance state like everything else
        # on this object -- see recall_integration.py for the demo
        # RULE_INVERSES config this defaults to.
        self.recall_config: RecallConfig = recall_config if recall_config is not None else RecallConfig()
        self.recall_inverses: dict[str, str] = dict(
            recall_inverses if recall_inverses is not None else recall_integration.RULE_INVERSES
        )
        self.recall_records: dict[str, RecallRecord] = {}
        self._known_recall_rule_ids = recall_integration.known_rule_ids(config, self.recall_inverses)

    def generate_problem(self) -> GeneratedProblem:
        """IDLE -> PRIMED -> EXECUTING.

        Calls the Phase 1 worker through its public build_problem()
        contract only -- never touches adapter internals. If Phase 1
        rejects the packet or the candidate fails verification, that
        exception propagates unchanged and task_state stays IDLE: an
        unverified problem is never assigned or presented.
        """
        packet = RulePacket(
            packet_id=f"{self.packet_id_prefix}-{self.cycle_count}",
            seed=self.route.seed,
            domain=self.route.domain,
            target_rules=self.route.target_rules,
            allowed_support_rules=self.route.allowed_support_rules,
            forbidden_rules=self.route.forbidden_rules,
            difficulty=self.route.difficulty,
        )
        problem = build_problem(packet)
        self._problems_by_id[problem.problem_id] = problem

        self.task_state = sm_a.assign_problem(
            self.task_state, problem.problem_id, self.route.target_rules
        )
        self.task_state = sm_a.present_to_learner(self.task_state)
        return problem

    def submit_attempt(self, attempt: LearnerAttempt) -> EvaluationEvidence:
        """EXECUTING -> VECTORING, then State Machine B evaluates and
        emits -- but does NOT acknowledge back to IDLE here.

        Validation happens before any state mutation: a malformed or
        stale attempt raises before task_state or evaluator_state changes
        at all, so it cannot mutate the active cycle. evaluator_state is
        left at EMITTED on return; route_next() is what consumes that
        emission and acknowledges B back to IDLE, so there is a window
        where B visibly holds evidence the router has not yet acted on,
        rather than resetting before the router ever reads it.
        """
        sm_b.validate_attempt(attempt, self.task_state)

        self.task_state = sm_a.receive_attempt(self.task_state)

        self.evaluator_state = sm_b.begin_evaluation(self.evaluator_state)
        evidence = sm_b.evaluate_attempt(attempt, self.task_state)
        self.evaluator_state = sm_b.emit_evidence(self.evaluator_state, evidence)
        return evidence

    def route_next(self) -> RouteDecision:
        """EMITTED -> IDLE for State Machine B, VECTORING -> RESOLVING ->
        IDLE for State Machine A. Applies the deterministic policy in
        policy.decide_next_route() and returns the RouteDecision that
        governs the next generate_problem() call.

        Takes no `evidence` argument: it reads
        `self.evaluator_state.last_evidence` -- the evidence State
        Machine B actually emitted -- so there is no parameter through
        which a caller could substitute forged or stale evidence. The
        problem_id match against task_state is a defensive check on top
        of that (it cannot fail via the public API, since submit_attempt()
        already validated the same match before evaluating).
        """
        if self.evaluator_state.lifecycle_state != EvaluationLifecycle.EMITTED:
            raise sm_b.IllegalEvaluationTransitionError(
                "route_next", EvaluationLifecycle.EMITTED, self.evaluator_state.lifecycle_state
            )
        evidence = self.evaluator_state.last_evidence
        if evidence.problem_id != self.task_state.current_problem_id:
            raise sm_b.StaleAttemptError(
                f"evidence for problem_id {evidence.problem_id!r} does not match the "
                f"active problem_id {self.task_state.current_problem_id!r}"
            )

        self.task_state = sm_a.apply_route_decision(self.task_state)

        if evidence.error_kind is not None and evidence.error_kind == self._last_error_kind:
            self._consecutive_same_error += 1
        else:
            self._consecutive_same_error = 1 if evidence.error_kind else 0
        self._last_error_kind = evidence.error_kind

        self.cycle_count += 1
        current_cycle = self.cycle_count

        # Phase 3: update recall records from the SAME authenticated
        # evidence just consumed above -- never a separate/parallel path,
        # so forged/stale/replayed evidence can no more reach recall state
        # than it can reach curriculum state.
        self._update_recall_from_evidence(evidence, cycle=current_cycle)

        next_route, next_index = policy.decide_next_route(
            config=self.config,
            current=self.route,
            curriculum_index=self.curriculum_index,
            outcome=evidence.outcome,
            rules_satisfied=not evidence.missing_rules,
            consecutive_same_error=self._consecutive_same_error,
            seed=self.base_seed + current_cycle,
        )
        due_rule_ids = self._due_recall_rule_ids(cycle=current_cycle)
        next_route = recall_integration.inject_due_recall(next_route, due_rule_ids)

        self.route = next_route
        self.curriculum_index = next_index

        self.evaluator_state = sm_b.acknowledge(self.evaluator_state)
        self.task_state = sm_a.resolve_cycle(self.task_state)
        return next_route

    def _update_recall_from_evidence(self, evidence: EvaluationEvidence, *, cycle: int) -> None:
        """For each rule this (just-finished) cycle targeted, record a
        recall success/miss if it was already tracked, or start tracking
        it if it was just demonstrated for the first time. A miss on a
        rule that isn't tracked yet is simply not a recall event (the
        rule hasn't been learned, so there's nothing to move closer).

        Builds the update on a local copy and only assigns it to
        self.recall_records once every rule in this cycle's target set has
        been processed without error -- if anything raises partway (e.g.
        an unrecognized rule_id), self.recall_records is left exactly as
        it was; a failure here can never partially mutate session state.
        """
        updated_records = dict(self.recall_records)
        for rule_id in self.route.target_rules:
            demonstrated = rule_id not in evidence.missing_rules
            existing = updated_records.get(rule_id)
            if existing is not None:
                updated = (
                    recall_worker.record_success(existing, cycle=cycle, config=self.recall_config)
                    if demonstrated
                    else recall_worker.record_miss(existing, cycle=cycle, config=self.recall_config)
                )
                updated_records[rule_id] = updated
                inverse_id = recall_worker.ready_for_reverse(updated, inverses=self.recall_inverses)
                if inverse_id is not None and inverse_id not in updated_records:
                    updated_records[inverse_id] = recall_worker.schedule_reverse(
                        inverse_id, cycle=cycle, config=self.recall_config
                    )
            elif demonstrated:
                updated_records[rule_id] = recall_integration.schedule_learned_rule(
                    rule_id,
                    cycle=cycle,
                    config=self.recall_config,
                    known_rules=self._known_recall_rule_ids,
                )
        self.recall_records = updated_records

    def _due_recall_rule_ids(self, *, cycle: int) -> tuple[str, ...]:
        return tuple(r.rule_id for r in recall_worker.due_rules(self.recall_records, cycle=cycle))

    def recall_snapshot(self) -> list[dict]:
        """A JSON-serializable snapshot of every tracked RecallRecord."""
        return recall_worker.snapshot(self.recall_records)

    def restore_recall(self, data: list[dict]) -> None:
        """Replace recall_records with records rebuilt from a snapshot
        (each individually re-validated by RecallRecord's constructor)."""
        self.recall_records = recall_worker.restore(data)

    def run_one_cycle(
        self, attempt_factory
    ) -> tuple[GeneratedProblem, EvaluationEvidence, RouteDecision]:
        """Convenience wrapper for the demo/tests: generate -> attempt ->
        route, in one call. `attempt_factory(problem) -> LearnerAttempt`
        builds the attempt from the just-generated problem, since a valid
        LearnerAttempt.problem_id can only be known after generate_problem()
        assigns one."""
        problem = self.generate_problem()
        attempt = attempt_factory(problem)
        evidence = self.submit_attempt(attempt)
        decision = self.route_next()
        return problem, evidence, decision
