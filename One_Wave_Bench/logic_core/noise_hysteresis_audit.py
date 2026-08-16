"""Deterministic Monte Carlo audit for commitment threshold chatter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple

import numpy as np

from commitment_map import CommitmentParameters, read_commitment_level


@dataclass(frozen=True)
class SequenceAudit:
    sample_count: int
    hysteretic_transitions: int
    memoryless_transitions: int
    hysteretic_levels: Tuple[int, ...]
    memoryless_levels: Tuple[int, ...]


def _transition_count(levels: Iterable[int]) -> int:
    levels = tuple(levels)
    return sum(left != right for left, right in zip(levels, levels[1:]))


def audit_observations(
    observations: Iterable[float],
    initial_level: int,
    parameters: CommitmentParameters = CommitmentParameters(),
) -> SequenceAudit:
    observations = tuple(float(value) for value in observations)
    hysteretic = []
    previous = initial_level
    for observed in observations:
        previous = read_commitment_level(observed, previous, parameters)
        hysteretic.append(previous)

    # Control: entry thresholds only, with no state memory.
    memoryless = [read_commitment_level(value, 0, parameters) for value in observations]
    return SequenceAudit(
        sample_count=len(observations),
        hysteretic_transitions=_transition_count(hysteretic),
        memoryless_transitions=_transition_count(memoryless),
        hysteretic_levels=tuple(hysteretic),
        memoryless_levels=tuple(memoryless),
    )


@dataclass(frozen=True)
class MonteCarloAudit:
    trials: int
    samples_per_trial: int
    true_latent: float
    noise_sigma: float
    mean_hysteretic_transitions: float
    mean_memoryless_transitions: float
    chatter_reduction_fraction: float
    full_entry_probability: float


def monte_carlo_audit(
    true_latent: float,
    noise_sigma: float,
    initial_level: int,
    trials: int = 256,
    samples_per_trial: int = 512,
    seed: int = 730,
    parameters: CommitmentParameters = CommitmentParameters(),
) -> MonteCarloAudit:
    if noise_sigma < 0.0 or trials <= 0 or samples_per_trial <= 0:
        raise ValueError("noise must be nonnegative and counts positive")
    rng = np.random.default_rng(seed)
    h_counts = []
    m_counts = []
    full_entries = 0
    for _ in range(trials):
        observations = true_latent + rng.normal(0.0, noise_sigma, samples_per_trial)
        audit = audit_observations(observations, initial_level, parameters)
        h_counts.append(audit.hysteretic_transitions)
        m_counts.append(audit.memoryless_transitions)
        if any(abs(level) == 3 for level in audit.hysteretic_levels):
            full_entries += 1
    mean_h = float(np.mean(h_counts))
    mean_m = float(np.mean(m_counts))
    reduction = 0.0 if mean_m == 0.0 else 1.0 - mean_h / mean_m
    return MonteCarloAudit(
        trials=trials,
        samples_per_trial=samples_per_trial,
        true_latent=true_latent,
        noise_sigma=noise_sigma,
        mean_hysteretic_transitions=mean_h,
        mean_memoryless_transitions=mean_m,
        chatter_reduction_fraction=reduction,
        full_entry_probability=full_entries / trials,
    )

