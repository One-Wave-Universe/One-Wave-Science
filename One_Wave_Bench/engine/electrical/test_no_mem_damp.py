#!/usr/bin/env python3
"""Quick stability test without memory input damping resistors."""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_hexagon_hbridge_stable_no_mem_damp import P0HexagonHBridgeStableNoMemDamp
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


print("\n" + "="*80)
print("TESTING: Stable circuit WITHOUT memory input damping resistors")
print("="*80)
print("\nBuilding circuit...")

builder = P0HexagonHBridgeStableNoMemDamp(v_supply=1.0)
circuit, initial_state = builder.build()
controller = CircuitController(circuit, initial_state)

print("Running baseline stability test (300us, no drive)...")
print("  ", end="", flush=True)

n_steps = 300000  # 300us at 1us/step
diverged = False

for step in range(n_steps):
    try:
        controller.run_step(1e-6)
        state = controller._make_state()

        a_sense = state.node_voltages.get('sense_A_pos', 0.5)
        b_memory = state.node_voltages.get('memory_B_pos_in', 0.5)
        c_pos = state.node_voltages.get('c_pos', 0.5)

        # Check for actual divergence (wide bounds)
        if a_sense > 2.0 or a_sense < -1.0 or b_memory > 2.0 or b_memory < -1.0:
            print(f"\n  DIVERGE at t={(step*1e-6)*1e6:.1f}us")
            print(f"    a_sense={a_sense:.3f}V, b_mem={b_memory:.3f}V, c_pos={c_pos:.3f}V")
            diverged = True
            break

        if step % 1000 == 0 and step > 0:
            print(f".", end="", flush=True)

    except Exception as e:
        print(f"\n  EXCEPTION at step {step}: {e}")
        diverged = True
        break

if not diverged:
    print("\n  [OK] STABLE for 300us")
    print("\nSuccess! Circuit WITHOUT memory damping is numerically stable.")
else:
    print("\nFailed. Circuit still diverges without memory damping.")

print("="*80 + "\n")
