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

from . import policy
from . import state_machine_a as sm_a
from . import state_machine_b as sm_b
from .models import (
    EvaluationEvidence,
    EvaluatorState,
    LearnerAttempt,
    LearnerTaskState,
    RouteDecision,
    initial_evaluator_state,
    initial_task_state,
)
from ..parser.core import build_problem
from ..parser.models import GeneratedProblem, RulePacket


class RouterLoop:
    """One learner session's orchestrator. All state is instance state --
    see the module docstring for why that matters for determinism."""

    def __init__(
        self,
        *,
        config: policy.PolicyConfig,
        base_seed: int,
        packet_id_prefix: str = "cycle",
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
        """EXECUTING -> VECTORING, then State Machine B evaluates.

        Validation happens before any state mutation: a malformed or
        stale attempt raises before task_state or evaluator_state changes
        at all, so it cannot mutate the active cycle.
        """
        sm_b.validate_attempt(attempt, self.task_state)

        self.task_state = sm_a.receive_attempt(self.task_state)

        self.evaluator_state = sm_b.begin_evaluation(self.evaluator_state)
        evidence = sm_b.evaluate_attempt(attempt, self.task_state)
        self.evaluator_state = sm_b.emit_evidence(self.evaluator_state, evidence)
        self.evaluator_state = sm_b.acknowledge(self.evaluator_state)
        return evidence

    def route_next(self, evidence: EvaluationEvidence) -> RouteDecision:
        """VECTORING -> RESOLVING -> IDLE. Applies the deterministic
        policy in policy.decide_next_route() and returns the RouteDecision
        that governs the next generate_problem() call."""
        self.task_state = sm_a.apply_route_decision(self.task_state)

        if evidence.error_kind is not None and evidence.error_kind == self._last_error_kind:
            self._consecutive_same_error += 1
        else:
            self._consecutive_same_error = 1 if evidence.error_kind else 0
        self._last_error_kind = evidence.error_kind

        self.cycle_count += 1
        next_route, next_index = policy.decide_next_route(
            config=self.config,
            current=self.route,
            curriculum_index=self.curriculum_index,
            outcome=evidence.outcome,
            consecutive_same_error=self._consecutive_same_error,
            seed=self.base_seed + self.cycle_count,
        )
        self.route = next_route
        self.curriculum_index = next_index

        self.task_state = sm_a.resolve_cycle(self.task_state)
        return next_route

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
        decision = self.route_next(evidence)
        return problem, evidence, decision
