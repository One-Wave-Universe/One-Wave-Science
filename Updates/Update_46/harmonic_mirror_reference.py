"""One-Wave Update 46 harmonic mirror reference implementation."""
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
    if n < 1:
        raise ValueError("n must start at 1")
    carrier = 2 * (n + 1)
    return HarmonicPacket(n, carrier, carrier - 1, carrier + 1)


def alphabet_packet(n: int) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    if n < 1:
        raise ValueError("n must start at 1")
    odd = 2 * n - 1
    even = 2 * n
    return (odd, even, odd), (odd, even, odd + 2)


@dataclass
class DrivenMirror:
    sigma: float
    phase: float = 0.0
    modulus: float = 12.0

    def step(self) -> tuple[float, float, float]:
        self.sigma = (2 * self.sigma + 2 * sin(self.phase) + 2) % self.modulus
        self.phase = (self.phase + 1.0) % (2 * pi)
        lower = (self.sigma - 1) % self.modulus
        upper = (self.sigma + 1) % self.modulus
        # Circular directed separation is fixed at two units.
        assert abs(((upper - lower) % self.modulus) - 2.0) < 1e-9
        return lower, self.sigma, upper


if __name__ == "__main__":
    for i in range(1, 13):
        print(harmonic_packet(i))
    system = DrivenMirror(sigma=0.0)
    for _ in range(12):
        print(system.step())
