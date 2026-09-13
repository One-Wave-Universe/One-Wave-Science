# Sandbox Lattice + Sensory Experiment Batch — 50 Executed Tests

**Status:** software simulation qualification only.

This batch exercises a fixed hex-lattice reference, moving active frame, scalar disturbance propagation, virtual sensory transduction, synthetic internal body telemetry, body/world coupling, Baseline Zero/HOLD/RECALL behavior, and structured `WHY FORWARD` escalation.

## Hard claim boundary

- These are sandbox software experiments. A PASS does **not** establish a physical superfluid/crystal lattice.
- `BodyTelemetry` is synthetic control state: energy budget, load, actuator strain, integrity, uncertainty, attention/compute budget, sensor confidence, and timing drift.
- These variables do **not** establish subjective sensation, pain, emotion, consciousness, or sentience.
- Rest lattice identity/topology stays separate from moving/dynamic process state.
- Expected behavior and measured simulation results stay distinct from bench/physical results.

## Reproduce

```bash
python Miniverse/sandbox_experiments.py
python -m pytest -q Miniverse/test_sandbox_experiments.py
```

Local qualification receipt for this branch build: **50/50 experiment checks passed; 3/3 pytest checks passed.**

## Experiment matrix

| ID | Group | Experiment | Measured simulation result |
|---|---|---|---|
| SLS-001 | lattice | pulse propagates from origin | PASS; ring1_peak=0.28381118129629623 |
| SLS-002 | lattice | opposed pulse interference | PASS; opposed=0.0, same_sign=0.13097116939942383 |
| SLS-003 | lattice | finite boundary stays bounded | PASS; energy=5.483769927543171, peak=1.286650104502317 |
| SLS-004 | lattice | damping ladder | PASS; high=0.7179871667649314, low=11.973200900877844 |
| SLS-005 | lattice | coupling changes spread | PASS; fast=1.0266032538615637, slow=0.1308691314351691 |
| SLS-006 | lattice | dynamic state cannot rewrite rest lattice | PASS; unchanged=True |
| SLS-007 | lattice | neighbor reciprocity | PASS; cells=61 |
| SLS-008 | lattice | checkpoint recall restores field | PASS; disturbed=2.5328232625, restored=0.0 |
| SLS-009 | lattice | inverse route recovers exact frame | PASS; end=((0, 0), 0, False), start=((0, 0), 0, False) |
| SLS-010 | lattice | rotation maps local movement | PASS; cell=[1, -1], orientation=1 |
| SLS-011 | sensory | field becomes touch reading | PASS; confidence=1.0, value=0.4 |
| SLS-012 | sensory | gradient yields direction | PASS; delta=0.6, direction=0 |
| SLS-013 | sensory | temporal delta yields motion channel | PASS; velocity=0.8549999999999998 |
| SLS-014 | sensory | saturation clamps extreme input | PASS; value=0.5 |
| SLS-015 | sensory | noise lowers confidence | PASS; clean=1.0, noisy=0.8 |
| SLS-016 | sensory | dropout has zero confidence | PASS; confidence=0.0 |
| SLS-017 | sensory | timestamps expose stale samples | PASS; new=4, old=0 |
| SLS-018 | sensory | quantization is explicit | PASS; value=0.2 |
| SLS-019 | sensory | agreeing redundant sensors fuse | PASS; confidence=0.8154627539503386, value=0.30941176470588233 |
| SLS-020 | sensory | contradiction raises uncertainty | PASS; confidence=0.2, uncertainty=1.0 |
| SLS-021 | body-state | energy drains and recovers | PASS; drained=0.9625000000000002, recovered=1.0, start=1.0 |
| SLS-022 | body-state | load rises then cools | PASS; cool=0.0, hot=0.08 |
| SLS-023 | body-state | blocked actuator raises strain | PASS; strain=0.18 |
| SLS-024 | body-state | integrity channel supports repair | PASS; after=0.7, before=0.4 |
| SLS-025 | body-state | uncertainty tracks disagreement | PASS; uncertainty=0.8 |
| SLS-026 | body-state | clock drift threshold | PASS; drift=0.08 |
| SLS-027 | body-state | compute budget is consumed | PASS; after=0.968, start=1.0 |
| SLS-028 | body-state | combined load proxy | PASS; load=0.8500000000000001 |
| SLS-029 | body-state | sensor confidence enters body state | PASS; confidence=0.6 |
| SLS-030 | body-state | Baseline Zero restores channels | PASS; max_delta=0.0 |
| SLS-031 | coupling | action creates tagged self-wave | PASS; cell=[1, 0], wave=0.4 |
| SLS-032 | coupling | efference cancellation | PASS; residual=0.0 |
| SLS-033 | coupling | self/external provenance stays distinct | PASS; external=external, self_source=self |
| SLS-034 | coupling | body-map mismatch detectable | PASS; distance=1 |
| SLS-035 | coupling | delayed feedback differs | PASS; delayed=0.8442744208333332, immediate=0.3 |
| SLS-036 | coupling | actuator failure WHY FORWARD | PASS; forwards=1 |
| SLS-037 | coupling | relocate and exact return | PASS; end=[0, 0] |
| SLS-038 | coupling | active sensing reveals source | PASS; after=0.7, before=0.0 |
| SLS-039 | coupling | cross-modal conflict lowers confidence | PASS; confidence=0.25, uncertainty=1.0 |
| SLS-040 | coupling | prediction error WHY FORWARD | PASS; urgency=0.7 |
| SLS-041 | memory | HOLD does not rewrite baseline | PASS; baseline_energy=1.0, held_energy=0.2 |
| SLS-042 | memory | rollback recovers corruption | PASS; restored=0.4 |
| SLS-043 | memory | restart preserves serialized body state | PASS; energy=0.55 |
| SLS-044 | memory | partial recall marks missing fields | PASS; missing=['task'] |
| SLS-045 | memory | plausible fill not auto-promoted | PASS; promoted=False, proposal=unknown-object |
| SLS-046 | memory | stable novelty waits for oversight | PASS; committed=False |
| SLS-047 | memory | sensor fault not learned as baseline | PASS; baseline=1.0 |
| SLS-048 | memory | baseline commit requires repetition + approval | PASS; approved=True, count=8, new=0.92 |
| SLS-049 | memory | seeded replay deterministic | PASS; run_a=[1.696876144004, 0.92, 3.1087066365], run_b=[1.696876144004, 0.92, 3.1087066365] |
| SLS-050 | end-to-end | lattice+sense+body+receipt boundary | PASS; actions=1, confidence=0.96, forwards=0, generation=1, reading=0.1931626935988044, topology_unchanged=True |

## Batch structure

Experiments 001–010 cover lattice dynamics and reference invariants; 011–020 sensory transduction and robustness; 021–030 synthetic internal body state; 031–040 body/world coupling and prediction; 041–049 persistence, recall, learning gates, and replay; 050 is the end-to-end integration check.

## Required interpretation

A failed experiment should remain a failed receipt until the implementation or the stated hypothesis changes. Do not tune thresholds merely to turn red results green. If this sandbox is later connected to physical devices, use a separate qualification label such as `DEVICE VERIFIED` or `BENCH RESULT`; never reuse these software PASS receipts as physical evidence.
