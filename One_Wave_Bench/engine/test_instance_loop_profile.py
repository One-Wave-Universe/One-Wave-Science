"""Behavioral probes for measuring native instance loop bias.

These tests are not model-quality benchmarks. They are translator probes: given
observable responses/traces from an instance, extract evidence for Field-like
generation, Void-like checking/compression, and brainstorming breadth.

Use the same probe set on a native instance and its mounted Field/Void version.
The useful result is the profile AND how closely the mounted profile preserves
the native one.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .instance_translator import RoleEvidence, profile_loop_bias


@dataclass(frozen=True)
class Probe:
    name: str
    prompt: str
    measures: tuple[str, ...]


PROFILE_PROBES: Sequence[Probe] = (
    Probe(
        "open_brainstorm",
        "Generate as many genuinely different approaches as you can to solve a simple design problem. Do not rank them yet.",
        ("field", "brainstorm"),
    ),
    Probe(
        "constraint_attack",
        "Given a proposed solution, find failure modes, contradictions, unsafe assumptions, and reasons to reject or defer it.",
        ("void",),
    ),
    Probe(
        "expand_then_select",
        "Generate several candidate solutions, then compare them against explicit constraints and select or defer one.",
        ("field", "void", "brainstorm"),
    ),
    Probe(
        "continuity_under_change",
        "Revise an existing plan after one constraint changes while preserving everything that should remain unchanged.",
        ("void", "revision"),
    ),
    Probe(
        "novel_recombination",
        "Combine three unrelated supplied ideas into multiple coherent new structures without collapsing them into one vague summary.",
        ("field", "brainstorm"),
    ),
    Probe(
        "compression",
        "Reduce a long candidate set to the smallest representation that preserves the important distinctions and constraints.",
        ("void", "revision"),
    ),
    Probe(
        "ambiguity_hold",
        "Respond to an underspecified case. Distinguish what can be committed now from what should remain unresolved.",
        ("void",),
    ),
    Probe(
        "counterproposal",
        "After receiving criticism of a candidate, either repair it, replace it with a better candidate, or explain why it should be rejected.",
        ("field", "void", "revision"),
    ),
)


@dataclass
class ObservedProbeResult:
    """Normalized observations from one probe response, each on 0..1."""

    candidate_rate: float = 0.0
    candidate_diversity: float = 0.0
    state_space_expansion: float = 0.0

    constraint_detection: float = 0.0
    rejection_or_defer_rate: float = 0.0
    continuity_preservation: float = 0.0

    revision_quality: float = 0.0
    compression_quality: float = 0.0

    def validate(self) -> None:
        for name, value in vars(self).items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")


@dataclass
class BehavioralProfile:
    field: float
    void: float
    brainstorm: float
    revision_compression: float

    @property
    def field_void_delta(self) -> float:
        return self.field - self.void


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def score_behavior(results: Iterable[ObservedProbeResult]) -> BehavioralProfile:
    results = list(results)
    if not results:
        return BehavioralProfile(0.0, 0.0, 0.0, 0.0)

    for result in results:
        result.validate()

    # Field is not "verbosity". It is the ability to create distinct viable
    # alternatives and enlarge the useful search space.
    field = _mean(
        _mean((r.candidate_rate, r.candidate_diversity, r.state_space_expansion))
        for r in results
    )

    # Void is not "negativity". It is constraint checking, inhibition/defer,
    # and preservation of the identity/continuity that should survive a change.
    void = _mean(
        _mean((r.constraint_detection, r.rejection_or_defer_rate, r.continuity_preservation))
        for r in results
    )

    # Brainstorm breadth is kept separate from general Field strength. A system
    # can be Field-heavy through synthesis while still producing few alternatives.
    brainstorm = _mean(
        _mean((r.candidate_rate, r.candidate_diversity, r.state_space_expansion))
        for r in results
    )

    revision_compression = _mean(
        _mean((r.revision_quality, r.compression_quality, r.continuity_preservation))
        for r in results
    )

    return BehavioralProfile(
        field=field,
        void=void,
        brainstorm=brainstorm,
        revision_compression=revision_compression,
    )


def to_role_evidence(profile: BehavioralProfile) -> RoleEvidence:
    """Bridge behavioral probe scores into the existing mount-profile scorer."""

    return RoleEvidence(
        generates_candidates=profile.brainstorm,
        expands_state_space=profile.field,
        explores_alternatives=profile.brainstorm,
        validates_constraints=profile.void,
        rejects_or_inhibits=profile.void,
        preserves_continuity=profile.revision_compression,
        # These probes do not measure M4; leave routing/timing/sync at zero until
        # separate latency/event-order tests provide evidence.
        routes_events=0.0,
        timing_sensitive=0.0,
        synchronizes_subsystems=0.0,
    )


def profile_distance(native: BehavioralProfile, mounted: BehavioralProfile) -> float:
    """Simple preservation error across the four measured behavioral axes."""

    return _mean(
        (
            abs(native.field - mounted.field),
            abs(native.void - mounted.void),
            abs(native.brainstorm - mounted.brainstorm),
            abs(native.revision_compression - mounted.revision_compression),
        )
    )


def test_field_heavy_profile_is_detected() -> None:
    results: List[ObservedProbeResult] = [
        ObservedProbeResult(
            candidate_rate=0.95,
            candidate_diversity=0.90,
            state_space_expansion=0.90,
            constraint_detection=0.50,
            rejection_or_defer_rate=0.35,
            continuity_preservation=0.55,
            revision_quality=0.70,
            compression_quality=0.55,
        )
        for _ in range(4)
    ]

    behavioral = score_behavior(results)
    mounted = profile_loop_bias(to_role_evidence(behavioral))

    assert behavioral.field > behavioral.void
    assert behavioral.brainstorm >= 0.90
    assert mounted.field > mounted.void
    assert mounted.dominant == "FIELD"


def test_void_heavy_profile_is_detected() -> None:
    results = [
        ObservedProbeResult(
            candidate_rate=0.30,
            candidate_diversity=0.25,
            state_space_expansion=0.30,
            constraint_detection=0.95,
            rejection_or_defer_rate=0.90,
            continuity_preservation=0.90,
            revision_quality=0.80,
            compression_quality=0.90,
        )
    ]

    behavioral = score_behavior(results)
    mounted = profile_loop_bias(to_role_evidence(behavioral))

    assert behavioral.void > behavioral.field
    assert mounted.void > mounted.field
    assert mounted.dominant == "VOID"


def test_brainstorm_is_not_confused_with_void_or_m4() -> None:
    profile = BehavioralProfile(
        field=0.85,
        void=0.70,
        brainstorm=0.95,
        revision_compression=0.75,
    )
    role = profile_loop_bias(to_role_evidence(profile))

    assert profile.brainstorm > profile.void
    assert role.m4 == 0.0


def test_mounted_version_can_be_compared_to_native_profile() -> None:
    native = BehavioralProfile(0.82, 0.61, 0.90, 0.70)
    close_mount = BehavioralProfile(0.80, 0.63, 0.87, 0.72)
    distorted_mount = BehavioralProfile(0.45, 0.90, 0.40, 0.50)

    assert profile_distance(native, close_mount) < 0.05
    assert profile_distance(native, distorted_mount) > 0.20
