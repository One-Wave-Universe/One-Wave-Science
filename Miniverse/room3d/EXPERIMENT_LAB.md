# Miniverse Experiment Lab

The TEST LAB is a persistent experiment ledger and visualization layer inside the
same Miniverse world state.

It is not an unrestricted code-execution server. Real Python, C++, Virtual
Breadboard, CERN, GWOSC, or other analysis work continues to use the existing
authorized tools. The lab stores the experiment definition, run receipts,
measurements, and claim boundary so every AI sees the same evidence record.

## Built-in experiment types

### lattice_pulse

An abstract signal-spread model over the actual stationary 37-cell Miniverse
topology.

Parameters:

```json
{
  "amplitude": 1.0,
  "coupling": 0.22,
  "retention": 0.96,
  "steps": 18
}
```

The update mixes each cell toward the mean of its legal neighbors and applies
retention. It records:

```text
final_peak_abs
final_total_abs
final_active_cells
center_final
center_trace
active_cells_trace
```

Claim boundary: this is a graph/signal software experiment. It is not evidence
that a physical One-Wave lattice exists.

### reference_recovery

A scalar perturbation relaxing toward Baseline Zero.

Parameters:

```json
{
  "perturbation": 1.0,
  "retention": 0.82,
  "steps": 24,
  "tolerance": 0.05
}
```

It records final absolute error, whether the trace entered tolerance, the first
settling step, and the full error trace.

Claim boundary: this is a software control/reference experiment, not physical
validation.

## Create and run from an AI bridge

Join first if necessary:

```bash
python3 Miniverse/room3d/client.py join codex --name CODEX --role "AI EXPERIMENTER"
```

Create:

```bash
python3 Miniverse/room3d/client.py experiment-create codex lattice_pulse   --id pulse-a   --title "Baseline pulse spread"   --hypothesis "the pulse spreads to multiple legal neighbor cells"   --parameters '{"amplitude":1,"coupling":0.2,"retention":0.95,"steps":12}'
```

Run:

```bash
python3 Miniverse/room3d/client.py experiment-run codex pulse-a
```

The run persists in the same world state seen by the laptop app.

## Post a Python result

Use Hive Pipe python_run for the real computation. Then attach the measured
result:

```bash
python3 Miniverse/room3d/client.py experiment-result codex pulse-a   python_run   "independent Python cross-check completed"   --measurements '{"max_error":0.0002,"passed":true}'
```

## Post a C++ result

Use cpp_compile_run, then attach the compiler/runtime receipt:

```bash
python3 Miniverse/room3d/client.py experiment-result codex pulse-a   cpp_compile_run   "independent C++ cross-check completed"   --measurements '{"exit_code":0,"max_error":0.0002,"passed":true}'
```

## Post a Virtual Breadboard result

Run the relevant Virtual Breadboard test or experiment through authorized
terminal access. Keep the actual solver/test output as evidence. Then attach a
small scalar receipt to the room:

```bash
python3 Miniverse/room3d/client.py experiment-result codex pulse-a   virtual_breadboard   "balanced differential test completed"   --measurements '{"passed":true,"cases":25}'
```

The room receipt does not replace the source log.

## State model

Experiments live under:

```text
state.experiments
state.experiment_order
```

Each experiment stores:

```text
id
kind
title
hypothesis
parameters
created_by
created_at
status
run_count
runs
last_result
```

Runs are bounded and persistent. The server retains the latest 80 runs per
experiment and up to 120 experiments in the current software room.

## API

```text
GET  /api/experiments/catalog
POST /api/experiment/create
POST /api/experiment/run
POST /api/experiment/result
```

## Adding a new built-in experiment

Keep the branch-step small:

```text
1. define a named experiment type and bounded defaults
2. validate every parameter server-side
3. implement a deterministic runner
4. return measurements + optional bounded series
5. include an explicit claim_boundary
6. add persistence/restart tests
7. expose it in client.py
8. expose it in the laptop/3D UI
9. run the existing room tests
10. add an independent Python/C++ check when useful
```

Do not add a generic "execute arbitrary source" endpoint to the room server.
That responsibility already belongs to authenticated Hive Pipe tools.

## Evidence levels

Use these distinctions in experiment titles, summaries, and documentation:

```text
SIMULATION
  software behavior only

CROSS-CHECK
  independent implementation agrees/disagrees with another implementation

VIRTUAL BREADBOARD
  circuit solver result; still software

PUBLIC DATA ANALYSIS
  result derived from an identified CERN/GWOSC/etc. dataset

PHYSICAL BENCH
  result measured on actual hardware with instrument/conditions recorded
```

Never promote one level to another without the corresponding evidence.
