"""Instance identity and translation framework for the mountable Field/Void loop.

Goal:
    Take a native program/instance that already performs a job, observe what
    makes it itself, then derive/test an adapter that mounts equivalent behavior
    onto the generic TwoStateLoop.

This module does not pretend translation can be inferred from names alone.
Identity is behavioral: state, input/output contract, timing, memory, preserved
invariants, thresholds, consequence, and failure behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Protocol


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

    return TranslationCandidate(
        instance_name=identity.name,
        preserved_invariants=list(identity.invariants),
        unresolved_fields=list(identity.state_keys),
        failed_cases=failed,
    )
