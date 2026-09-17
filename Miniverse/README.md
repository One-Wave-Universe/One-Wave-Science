# Miniverse self-loop and sandbox world

Permission is the contract, not a chat prompt.

## Self-loop

```bash
python Miniverse/self_loop.py
python Miniverse/test_self_loop.py
```

- `DROP` noise locally
- `LOCAL` act from the boot contract
- `HOLD` unknown sources (do not invent authority)
- `FORWARD` only with `why_forward`
- Baseline Zero generation stays `0` inside this loop

## Sandboxed lattice + sensory + internal body state

```bash
python Miniverse/sandbox_experiments.py
python -m pytest -q Miniverse/test_sandbox_experiments.py
```

The sandbox keeps the authoritative hex-lattice rest topology fixed while a dynamic scalar field, active frame, virtual sensors, and synthetic body telemetry change on top of it.

Current qualification batch:

- `SANDBOX_LATTICE_SENSORY_EXPERIMENTS_001_050.md` — human-readable 50-test receipt and experiment matrix.
- `sandbox_lattice.py` — deterministic lattice world, active frame, virtual sensors, body telemetry, checkpoints, recall, and `WHY FORWARD` packets.
- `sandbox_experiments.py` — executable SLS-001 through SLS-050 suite.
- `test_sandbox_experiments.py` — suite count, all-pass, fixed-rest-topology stress check, and reciprocal-edge checks.

Claim boundary: these are software simulation experiments only. Synthetic body telemetry is control/health state; it is not evidence of subjective sensation or consciousness, and simulation PASS is not physical proof of a lattice.
