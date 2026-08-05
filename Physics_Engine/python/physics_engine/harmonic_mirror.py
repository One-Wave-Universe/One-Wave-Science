"""The Update 46 harmonic mirror system -- One-Wave's own wave/field
math, not particle physics. Implements
UPDATED_46_CONTINUOUS_MIRROR_HEARING_AND_ROTATION_CANON.md sections 2
and 5 exactly:

- harmonic_packet(n): the fixed packet H(n, sigma) = [n, 2(n+1),
  2(n+1)+sigma] -- a note identity's carrier and its two mirrored
  resolutions.
- alphabet_packet(n): the parallel alphabet oscillator, L-(n) and
  L+(n), sharing the same 2n-1/2n/2n+-1 shape.
- DrivenMirror: the shared-carrier recurrence that drives H- and H+
  from one moving carrier (phi, Sigma) rather than evolving them as two
  independent waves -- the canon's explicit rule in section 5.

Folded in from Updates/Update_46/harmonic_mirror_reference.py, the
reference implementation shipped with the canon update itself, and
tested against that document's own worked examples.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi, sin


@dataclass(frozen=True)
class HarmonicPacket:
    identity: int
    carrier: int
    lower: int
    upper: int


def harmonic_packet(n: int) -> HarmonicPacket:
    """H(n, sigma) = [n, 2(n+1), 2(n+1)+sigma] for sigma in {-1, +1} --
    canon section 2. E.g. harmonic_packet(1) is the canon's own
    worked example: A- = 1,4,3 and A+ = 1,4,5 share carrier 4."""
    if n < 1:
        raise ValueError("n must start at 1 (A = 1)")
    carrier = 2 * (n + 1)
    return HarmonicPacket(identity=n, carrier=carrier, lower=carrier - 1, upper=carrier + 1)


def alphabet_packet(n: int) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """L-(n) = (2n-1, 2n, 2n-1), L+(n) = (2n-1, 2n, 2n+1) -- canon
    section 3. alphabet_packet(1) is the canon's own worked example:
    A- = 1 -> 2 -> 1, A+ = 1 -> 2 -> 3."""
    if n < 1:
        raise ValueError("n must start at 1 (A = 1)")
    odd = 2 * n - 1
    even = 2 * n
    return (odd, even, odd), (odd, even, odd + 2)


@dataclass
class DrivenMirror:
    """The shared moving carrier from canon section 5: 'Do not
    recursively evolve H+ and H- as independent carriers. Both surfaces
    are generated from one shared moving carrier.' Sigma(n+1) is
    computed from phi(n), the carrier phase *before* it advances for
    this step -- matching the canon's own equation order exactly."""

    sigma: float
    phase: float = 0.0
    modulus: float = 12.0

    def step(self) -> tuple[float, float, float]:
        self.sigma = (2 * self.sigma + 2 * sin(self.phase) + 2) % self.modulus
        self.phase = (self.phase + 1.0) % (2 * pi)
        lower = (self.sigma - 1) % self.modulus
        upper = (self.sigma + 1) % self.modulus
        return lower, self.sigma, upper
