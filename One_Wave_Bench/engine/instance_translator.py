"""Instance identity and translation framework for the mountable Field/Void loop.

Goal:
    Take a native program/instance that already performs a job, observe what
    makes it itself, then derive/test an adapter that mounts equivalent behavior
    onto the generic TwoStateLoop.

This module does not pretend translation can be inferred from names alone.
Identity is behavioral: state, input/output contract, timing, memory, preserved
invariants, thresholds, consequence, failure behavior, and the native balance
between Field-like generation, Void-like checking, and M4-like fast routing.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Protocol


@dataclass
class RoleEvidence:
    """Observed native behaviors used to shape the mounted loop.

    These are measurements/descriptions of what the old instance already does.
    They are not personality labels and they do not force a 50/50 Field/Void
    split.
    """

    generates_candidates: float = 0.0
    expands_state_space: float = 0.0
    explores_alternatives: float = 0.0
    validates_constraints: float = 0.0
    rejects_or_inhibits: float = 0.0
    preserves_continuity: float = 0.0
    routes_events: float = 0.0
    timing_sensitive: float = 0.0
    synchronizes_subsystems: float = 0.0


@dataclass
class LoopBiasProfile:
    """How strongly this instance naturally loads each loop function."""

    field: float
    void: float
    m4: float
    dominant: str
    evidence: RoleEvidence

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class InstanceIdentity:
    name: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    state_keys: List[str] = field(default_factory=list)
    memory_keys: List[str] = field(default_factory=list)
    timing_keys: List[str] = field(default_factory=list)
    thresholds: Dict[str, Any] = field(default_factory=dict)
    invariants: List[str] = field(default_factory=list)
    failure_modes: List[str] = field(default_factory=list)
    notes: Dict[str, Any] = field(default_factory=dict)
    loop_bias: Optional[LoopBiasProfile] = None


@dataclass
class TraceStep:
    case_id: str
    step: int
    input_value: Any
    state_before: Any
    output_value: Any
    state_after: Any
    consequence: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TraceDiff:
    case_id: str
    step: int
    input_match: bool
    output_match: bool
    state_match: bool
    consequence_match: bool
    native_output: Any
    mounted_output: Any
    native_state: Any
    mounted_state: Any
    notes: List[str] = field(default_factory=list)

    @property
    def equivalent(self) -> bool:
        return (
            self.input_match
            and self.output_match
            and self.state_match
            and self.consequence_match
        )


class NativeInstance(Protocol):
    """Minimal observable contract for a reference program."""

    name: str

    def snapshot(self) -> Any:
        """Return serializable state sufficient to compare behavior."""

    def step(self, value: Any) -> Any:
        """Run one native cycle and return native output."""


class MountedInstanceLike(Protocol):
    name: str

    def snapshot(self) -> Any:
        ...

    def step(self, value: Any) -> Any:
        ...


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(values) / len(values)


def profile_loop_bias(evidence: RoleEvidence) -> LoopBiasProfile:
    """Convert observed behavior into a Field/Void/M4 mounting profile.

    Each input is expected on 0..1. The profile is intentionally independent:
    an instance can score high on both Field and Void, or low on both. The
    largest score is only a useful mounting hint; it is not an ontology claim.
    """

    values = asdict(evidence)
    for name, value in values.items():
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be between 0 and 1")

    field_score = _mean(
        [
            evidence.generates_candidates,
            evidence.expands_state_space,
            evidence.explores_alternatives,
        ]
    )
    void_score = _mean(
        [
            evidence.validates_constraints,
            evidence.rejects_or_inhibits,
            evidence.preserves_continuity,
        ]
    )
    m4_score = _mean(
        [
            evidence.routes_events,
            evidence.timing_sensitive,
            evidence.synchronizes_subsystems,
        ]
    )

    scores = {"FIELD": field_score, "VOID": void_score, "M4": m4_score}
    highest = max(scores.values())
    winners = [name for name, score in scores.items() if score == highest]
    dominant = winners[0] if len(winners) == 1 else "BALANCED_OR_MIXED"

    return LoopBiasProfile(
        field=field_score,
        void=void_score,
        m4=m4_score,
        dominant=dominant,
        evidence=evidence,
    )


class IdentityScanner:
    """Collect explicit identity declarations plus observed state keys.

    This is deliberately conservative. It can discover structure, but semantic
    labels still need to be justified by behavior or supplied by the instance.
    """

    def scan(
        self,
        instance: NativeInstance,
        *,
        inputs: Iterable[str] = (),
        outputs: Iterable[str] = (),
        memory_keys: Iterable[str] = (),
        timing_keys: Iterable[str] = (),
        thresholds: Optional[Mapping[str, Any]] = None,
        invariants: Iterable[str] = (),
        failure_modes: Iterable[str] = (),
        notes: Optional[Mapping[str, Any]] = None,
        role_evidence: Optional[RoleEvidence] = None,
    ) -> InstanceIdentity:
        snap = instance.snapshot()
        if isinstance(snap, Mapping):
            state_keys = sorted(str(k) for k in snap.keys())
        else:
            state_keys = [type(snap).__name__]

        return InstanceIdentity(
            name=instance.name,
            inputs=list(inputs),
            outputs=list(outputs),
            state_keys=state_keys,
            memory_keys=list(memory_keys),
            timing_keys=list(timing_keys),
            thresholds=dict(thresholds or {}),
            invariants=list(invariants),
            failure_modes=list(failure_modes),
            notes=dict(notes or {}),
            loop_bias=profile_loop_bias(role_evidence) if role_evidence else None,
        )


class TraceRecorder:
    @staticmethod
    def run_case(instance: NativeInstance, case_id: str, values: Iterable[Any]) -> List[TraceStep]:
        trace: List[TraceStep] = []
        for step_index, value in enumerate(values, start=1):
            before = instance.snapshot()
            output = instance.step(value)
            after = instance.snapshot()
            trace.append(
                TraceStep(
                    case_id=case_id,
                    step=step_index,
                    input_value=value,
                    state_before=before,
                    output_value=output,
                    state_after=after,
                )
            )
        return trace


class EquivalenceTester:
    """Compare a native program against its mounted state-machine version."""

    def __init__(
        self,
        *,
        normalize_output: Optional[Callable[[Any], Any]] = None,
        normalize_state: Optional[Callable[[Any], Any]] = None,
        normalize_consequence: Optional[Callable[[Any], Any]] = None,
    ) -> None:
        self.normalize_output = normalize_output or (lambda value: value)
        self.normalize_state = normalize_state or (lambda value: value)
        self.normalize_consequence = normalize_consequence or (lambda value: value)

    def compare(self, native: List[TraceStep], mounted: List[TraceStep]) -> List[TraceDiff]:
        if len(native) != len(mounted):
            raise ValueError("Trace lengths differ; translator changed cycle count")

        diffs: List[TraceDiff] = []
        for n, m in zip(native, mounted):
            notes: List[str] = []
            input_match = n.input_value == m.input_value
            output_match = self.normalize_output(n.output_value) == self.normalize_output(m.output_value)
            state_match = self.normalize_state(n.state_after) == self.normalize_state(m.state_after)
            consequence_match = self.normalize_consequence(n.consequence) == self.normalize_consequence(m.consequence)

            if not output_match:
                notes.append("output semantics changed")
            if not state_match:
                notes.append("persistent identity/state changed")
            if not consequence_match:
                notes.append("consequence/feedback changed")

            diffs.append(
                TraceDiff(
                    case_id=n.case_id,
                    step=n.step,
                    input_match=input_match,
                    output_match=output_match,
                    state_match=state_match,
                    consequence_match=consequence_match,
                    native_output=n.output_value,
                    mounted_output=m.output_value,
                    native_state=n.state_after,
                    mounted_state=m.state_after,
                    notes=notes,
                )
            )
        return diffs


@dataclass
class TranslationCandidate:
    """A proposed adapter mapping, derived from trace comparison."""

    instance_name: str
    native_to_local: Dict[str, str] = field(default_factory=dict)
    local_to_native: Dict[str, str] = field(default_factory=dict)
    preserved_invariants: List[str] = field(default_factory=list)
    unresolved_fields: List[str] = field(default_factory=list)
    failed_cases: List[str] = field(default_factory=list)
    loop_bias: Optional[LoopBiasProfile] = None
    mounting_notes: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


def derive_candidate(identity: InstanceIdentity, diffs: Iterable[TraceDiff]) -> TranslationCandidate:
    """Build the conservative translation worklist from observed mismatches.

    It intentionally does not auto-invent semantic mappings. Unknown mappings
    remain unresolved until tests or domain knowledge identify them.
    """

    failed = []
    for diff in diffs:
        if not diff.equivalent:
            failed.append(f"{diff.case_id}:{diff.step}")

    mounting_notes: List[str] = []
    if identity.loop_bias:
        bias = identity.loop_bias
        if bias.field > bias.void:
            mounting_notes.append("preserve wider/faster Field proposal path")
        if bias.void > bias.field:
            mounting_notes.append("preserve stronger Void validation/continuity path")
        if bias.m4 >= 0.5:
            mounting_notes.append("instance needs explicit fast routing/timing state")
        else:
            mounting_notes.append("M4 may remain thin or identity-like at this scale")

    return TranslationCandidate(
        instance_name=identity.name,
        preserved_invariants=list(identity.invariants),
        unresolved_fields=list(identity.state_keys),
        failed_cases=failed,
        loop_bias=identity.loop_bias,
        mounting_notes=mounting_notes,
    )
