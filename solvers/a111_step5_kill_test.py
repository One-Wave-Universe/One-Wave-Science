#!/usr/bin/env python3
"""
A-111 Step 5 kill test (Core Rule 10).

The Step 5 harmonic-selection criterion in a111_closure_validator.py must be able
to REJECT a non-recursive control. If it accepts the controls, the criterion does
not discriminate and Step 5 is not a valid test of recursion.

Criterion (unchanged from the validator):
    selected(step) = (D_n < 0.1) or (S_total > 0.7)
    D_n     = ||psi_next - psi|| / ||psi||
    S_total = 1 - |E_next - E| / E

Controls (no memory, no feedback):
  frozen : psi_next = psi
  random : psi_next = fresh random field with the same norm as psi
Recursive: OneWaveFieldUpdater with the validator's parameters.

Exit code 0 only if the criterion rejects both controls.
"""
import sys
import numpy as np
from algorithm_zero_physics_engine import OneWaveFieldUpdater

EPSILON, S_THRESHOLD = 0.1, 0.7
SIZE, STEPS = 16, 200


def initial_field():
    x, y, z = np.meshgrid(np.arange(SIZE), np.arange(SIZE), np.arange(SIZE))
    return np.exp(-((x - 8) ** 2 + (y - 8) ** 2 + (z - 8) ** 2) / 20.0) + 0j


def selected(psi, psi_next):
    d_n = np.linalg.norm(psi_next - psi) / (np.linalg.norm(psi) + 1e-10)
    e, e_next = np.sum(np.abs(psi) ** 2), np.sum(np.abs(psi_next) ** 2)
    s_total = 1.0 - abs(e_next - e) / (e + 1e-10)
    return (d_n < EPSILON) or (s_total > S_THRESHOLD), d_n, s_total


def run(name, next_fn):
    rng = np.random.default_rng(0)
    psi = initial_field()
    psi_prev = 0.9 * psi
    accepted = 0
    d_vals = []
    for _ in range(STEPS):
        psi_next = next_fn(psi, psi_prev, rng)
        ok, d_n, _ = selected(psi, psi_next)
        accepted += ok
        d_vals.append(d_n)
        psi_prev, psi = psi, psi_next
    rate = accepted / STEPS
    print(f"{name:<10} accepted {accepted}/{STEPS} ({100*rate:.1f}%)  max D_n = {max(d_vals):.4f}")
    return rate


def recursive(psi, psi_prev, rng):
    return OneWaveFieldUpdater(damping=0.05, coupling=0.15).step(psi, psi_prev)


def frozen(psi, psi_prev, rng):
    return psi.copy()


def random_memoryless(psi, psi_prev, rng):
    noise = rng.standard_normal(psi.shape) + 1j * rng.standard_normal(psi.shape)
    return noise * (np.linalg.norm(psi) / np.linalg.norm(noise))


def main():
    print("A-111 Step 5 kill test")
    print("-" * 60)
    run("recursive", recursive)
    rf = run("frozen", frozen)
    rr = run("random", random_memoryless)
    controls_rejected = rf < 1.0 and rr < 1.0
    print("-" * 60)
    if controls_rejected:
        print("KILL TEST PASSED: criterion rejects the non-recursive controls.")
        return 0
    print("KILL TEST FAILED: criterion accepts non-recursive controls.")
    print("Step 5 cannot distinguish recursion from no-feedback dynamics; it is not a valid test.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
