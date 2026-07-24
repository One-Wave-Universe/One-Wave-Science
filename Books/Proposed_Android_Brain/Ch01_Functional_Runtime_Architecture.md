# Chapter 1 — Functional Runtime Architecture

Status: PROPOSED BUILD

## Hardware-Agnostic Architecture

```text
Sensors / current field
<-> choice and candidate generation
<-> simulated movement
<-> M4 mirror and scale weighing
<-> state / risk / readiness report
<-> accepted commitment
<-> body movement and recursive feedback
```

All gate relationships are duplex. Forward proposals and reverse constraints travel together.

## Proposed Compute Mapping

One possible Jetson-class implementation:

- GPU: Dream Engine candidate generation and parallel simulation.
- CPU: Administrator, identity, permission, and commitment logic.
- persistent low-latency service: M4 weighing and modulation.
- protected storage: Reference Ground.
- volatile or recoverable workspace: Working Ground.

This role mapping is a design proposal. The silicon is not literally transformed into biological brain regions.


## Symbolic Route and Validation Layer

The runtime may compile words or symbolic instructions through G-721 without treating the alphabet as the physical movement system.

```text
word or cue
-> G-721 mirrored alphabet coordinate path
-> live -1(0)+1 branch choice
-> declared G-721a through G-721e route/rail scheduler or validator
-> G-722 procedural-memory reconstruction and settling
-> wheel/body movement translation
-> sensory correction
```

The systems remain separate:

- Hopfield/Boltzmann principles store or reconstruct relationships;
- G-721 identifies symbolic coordinates and route differentials;
- G-721a provides the fixed Fibonacci regression path;
- G-721b through G-721e test broader route and rail grammars;
- G-722 combines Boltzmann candidate reconstruction with Hopfield attractor settling;
- G-723 audits expansion, correction, rhythm, and drift when a qualifying recurrence is available;
- the wheel system translates route information into live movement geometry;
- binary oversight may allow, block, or flag;
- foundational choice remains bottom-up `-1(0)+1`.

A Fibonacci validator mismatch may stop or flag an exact programmed route. It may not force the body to continue when live sensory choice selects Hold or correction.

## Commit Rule

```text
promote Working Ground to Reference Ground
only when
Gate 5 state report matches Gate 6 acceptance
```

Every promotion stores:

- prior state,
- proposed delta,
- reason for acceptance,
- M4 scale report,
- rollback path.

## Throttle and Modulation

The current 12:1 maximum imbalance is a proposed engineering ceiling, not a derived biological constant. Approaching the ceiling should trigger:

- slowdown,
- redistribution,
- synchronization attempt,
- hold,
- or safe reset.

The runtime must also support intentional energy reduction. Down-modulation is a normal control action, not a fault.

## Tests

1. Compare flat controller vs. separated Dream/M4/Administrator runtime.
2. Introduce conflicting high-value candidates and measure stability.
3. Remove M4 and test for overreaction or indecision.
4. Delay Administrator acceptance and test whether Working Ground remains recoverable.
5. Force a throttle excursion and verify safe return rather than domination or runaway.
6. Test whether local units retain autonomy under targeted correction.
