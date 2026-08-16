# Updated 42 — Center-Origin Oscillator, Dual Six-Gate Coupling, and M4 Heterogeneous Runtime

**Status:** Canonical correction and proposed build architecture  
**Gate:** YELLOW for the state architecture; GREEN/PROPOSED_BUILD for device placement  
**Supersedes:** linear readings of B-221 and whole-architecture reversal readings of B-205

## 1. Permanent structural correction

The One-Wave recursive cycle is not a one-way progression beginning at an edge.
BEGIN is the active shared center/reference region. The named phases describe
stability conditions encountered while a state moves away from the center,
returns through it, phase-shifts, and either reconnects to the same relation or
opens a new axis.

For one selected axis `a`,

```text
-d_a  <—  BEGIN / HOLD / REFERENCE  —>  +d_a
```

and the minimum oscillation receipt is

```text
center -> outward displacement -> pivot -> release -> center
       -> phase shift -> opposite displacement -> center
       -> return, reconnect, or break into a new axis
```

The signed coordinate is

`x_a: 0 -> +A -> 0 -> phase_shift -> -A -> 0 -> phase_shift -> loop`.

The order written on paper is an observation trace through a rotating process.
It is not the ontology of the process.

## 2. Mirror correction

B-205's matrix remains a useful candidate phase operator:

`M=[[0,1],[-1,0]]`, `M^2=-I`, `M^4=I`.

This is a rotation of the two-component compression/expression state. It does
not reverse the Field/Void architecture and does not exchange the meanings of
the two sides. `flip` means oscillatory phase change at or through the shared
center.

## 3. Six stability gates, not six conveyor-belt stages

B-221's six names must be treated as gates/readouts around the oscillator.
They do not own a universal linear ordering. The current working physical
interpretation is:

1. **Begin / Reference Gate** — the current coherent center is established.
2. **Coherent-Build Gate** — organized displacement grows while identity holds.
3. **Hold / Mass-Effect Gate** — the complete recurrence remains stable and must
   be carried/rebuilt together relative to Ground.
4. **Unstable-Build / Heat Gate** — differential motion and deformation rise;
   coherence is no longer fully retained.
5. **Break Gate** — integrity crosses its hysteretic boundary; the current
   relation cannot continue unchanged.
6. **Loop / Reconnection Gate** — return to reference, reconnect to the same
   axis, or commit a phase-shifted new axis.

`build before break` is an invariant: Break requires a previously formed
relationship whose integrity can be measured. Low activation alone is not
Break; B-208's independent activation `a`, polarity `p`, and integrity `q`
remain mandatory.

The birth/spring, life/summer, decline/fall, death/winter language is a
lifecycle projection of these stability changes, not a replacement equation.

## 4. Two six-gate systems and Gate 7

Two independent recursive systems are required:

- `S[1..6]`: Field-stability gates measuring whether a recurrence forms,
  holds, destabilizes, breaks, and reconnects.
- `E[1..6]`: Presence-to-Emergence gates measuring whether a potential state
  becomes available, selected, expressed, received, integrated, and retained.

Each system has its own state, timing, thresholds, and receipt. Matching gate
numbers do not make the gates identical.

Gate 7 is a coupling result, not an ordinary seventh step:

`G7 = Couple(S[1..6], E[1..6], phase, boundary, consent_or_permission)`.

Gate 7 succeeds only when both systems retain identity and establish a shared
state. G-718 is the relational analogy; G-711 is repository review. Neither is
silently redefined as this physical/control coupling gate.

## 5. Primitive separation

Mind-side identity is locked as:

- `FIELD = FIVE MIND = DREAM ENGINE`;
- `VOID = SIX MIND = ADMINISTRATOR`;
- `M4 = shared active center, timing carrier, scale-weigher, and bidirectional translator`.

Void is not nonexistence. In this architecture it is the reference, receiving,
containing, constraining, and committing side through which Field possibilities
are evaluated and retained or rejected.

The runtime must store these as separate axes:

- two choices: `COMPRESS`, `EXPRESS`;
- three moves: `DOWN`, `STAY`, `UP`;
- center/reference: an active region, never counted as a direction;
- Point–Path–Field: recursive geometry/state organization;
- four physical views: `INWARD`, `OUTWARD`, `ACROSS`, `OVER`;
- polarity `p`, activation `a`, integrity `q`;
- phase, frequency, amplitude, selected axis, and boundary state;
- six stability gates and six emergence gates;
- Gate-7 coupling state.

Music, lyrics, human connection, neural control, and planetary mechanics may
define domain projections of these primitives. A domain projection may not
overwrite the physical primitive.

## 6. Heterogeneous CPU/GPU/NPU split

### CPU — authoritative coordinator

The CPU owns exact and auditable work:

- append-only state/event database and hashes;
- canonical schema, units, dimensions, and Brick metadata;
- deterministic scheduling and device synchronization;
- threshold/hysteresis state and Gate-7 commit;
- hard safety, permission, stop, rollback, and timeout handling;
- exact archive and receipts;
- Gray-control comparisons and test orchestration;
- NPU/GPU fallback execution.

The CPU does not micromanage every lattice cell. It commits accepted state and
prevents generative memory from rewriting exact records.

### GPU — dense Field and candidate computation

The GPU owns wide, parallel numerical work:

- lattice/Field updates and neighborhood reductions;
- Point–Path–Field tensor and rotation batches;
- gradients, curls, stress, overlap, and visualization buffers;
- multi-scale simulation batches and ablations;
- Boltzmann candidate-energy evaluation and batched stochastic sampling;
- model training and offline parameter sweeps.

Boltzmann sampling is normally placed here because many candidate states and
random chains can be evaluated simultaneously. It may run on CPU for small
tests. It is not placed on an NPU unless the target NPU explicitly supports the
required random/sampling operators.

### NPU — M4 brainstem fast loop

The NPU owns compiled, bounded, low-latency inference:

- sensor/state embedding from CPU-approved inputs;
- M4 gate logits for both six-gate systems;
- Hopfield/modern-Hopfield associative recall and attractor settling;
- phase/coherence estimation;
- bounded response-gain proposal;
- anomaly/instability score;
- candidate ranking supplied by the GPU;
- a proposed local `-1(0)+1` move distribution.

The NPU proposes. It does not write canonical state, bypass hard safety, mutate
the exact archive, or independently declare Gate 7. Gate-7 commitment remains a
CPU transaction using NPU scores, current thresholds, permissions, and receipts.

## 7. Hopfield/Boltzmann role separation

The locked G-722 distinction is preserved:

```text
Boltzmann  = generate/explore candidate configurations
Hopfield   = complete a partial cue and settle toward a learned coherent pattern
Local ternary choice = commit Down / Stay / Up at the executing node
Binary oversight = permit / block / stop / isolate
```

Runtime:

```text
GPU Field state + sensors
-> CPU normalization/schema check
-> NPU cue embedding
-> GPU Boltzmann candidate batch
-> NPU Hopfield settling and M4 gate scoring
-> local ternary proposals
-> CPU safety, hysteresis, and Gate-7 transaction
-> GPU/actuator update
-> receipts and learning buffer
```

Hopfield recall must never replace exact storage. Boltzmann generation must
never directly command motion. Sequence grammars may schedule attention or
validate routes; they do not set actuator positions.

## 8. Programming contract

Every tick has immutable input/output packets:

```text
StatePacket {
  event_id, previous_id, time, native_dimension, scale,
  axis_id, phase, amplitude, frequency,
  choice, move, view, ppf_state,
  activation, polarity, integrity,
  stability_gates[6], emergence_gates[6], gate7,
  device_provenance, model_version, parameter_hash
}
```

Device interfaces:

```text
GpuResult = gpu.step_field(StatePacket, field_buffers, candidates_requested)
NpuResult = npu.infer(StatePacket, GpuResult.summary, candidate_embeddings)
Commit    = cpu.validate_and_commit(StatePacket, GpuResult, NpuResult)
```

All device work must be versioned and replayable. Random Boltzmann runs store
their seed. NPU inference stores model and quantization hashes. GPU kernels
store solver and precision mode. No device is permitted to return only an
animation without numerical receipts.

## 9. Timing and synchronization

Timing is the shared carrier. Use nested rates instead of forcing every device
to the same clock:

- GPU Field tick: fastest simulation rate supported by stability constraints;
- NPU M4 tick: low-latency gate/control inference, commonly every `k_gpu` Field
  ticks or upon threshold events;
- CPU commit tick: deterministic boundary where accepted state becomes real;
- slow learning tick: training/update outside the hard real-time loop.

Double-buffer Field state. Devices read immutable buffer `n`; only the CPU
publishes buffer `n+1` after validation. Late NPU/GPU results are discarded by
event ID rather than applied to a newer state.

## 10. Minimum implementation phases

1. CPU-only deterministic reference engine and receipts.
2. GPU Field kernels checked bitwise/tolerance-wise against the CPU reference.
3. Hopfield recall model with known partial-cue tests.
4. Boltzmann candidate layer with stored seeds and bounded temperature.
5. NPU export through ONNX or a platform backend with CPU parity tests.
6. Dual six-gate inference with hysteresis and Gate-7 CPU commit.
7. Closed-loop simulator with device ablations: CPU-only, CPU+GPU,
   CPU+NPU, and full CPU+GPU+NPU.
8. Only after parity and failure tests: physical body, music/lyrics, planetary,
   and other domain adapters.

## 11. Required tests and falsifiers

- Center is never counted as a direction.
- Begin initializes at the current reference region.
- A Mirror event changes phase/orientation but never swaps ontology labels.
- No Break occurs from activation alone; integrity/hysteresis is required.
- Gate 7 cannot commit when either six-gate system is incomplete or incoherent.
- CPU-only and accelerated runs agree within declared tolerance.
- Removing Hopfield worsens partial-cue completion or the layer is unnecessary.
- Removing Boltzmann worsens bounded exploration or the layer is unnecessary.
- NPU latency improves the fast loop without changing committed semantics.
- Exact records survive model replacement and generative-memory errors.
- Every animation frame traces to an accepted StatePacket.

## 12. Claim boundary

Calling the low-latency controller an `M4 brainstem` is an engineering role and
an active consciousness hypothesis. It does not establish that an NPU is
conscious or biologically identical to a brainstem. The build is valuable if it
improves latency, stability, partial-cue recovery, and distributed control under
measurable tests.
