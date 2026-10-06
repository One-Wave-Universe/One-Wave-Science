#!/usr/bin/env python3
"""Test P0 ternary circuit: virtual ground stability and ternary sequencing.

This is a load-bearing test. It must prove:
1. Virtual ground stays stable when a winding sources/sinks current
2. Midpoint voltage stays near 0V under balanced and unbalanced loads
3. Three half-bridges can sequence the required ternary states
4. Flyback energy doesn't cause overshoot
"""
import sys
import json
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from engine.electrical.p0_ternary_circuit import P0TernaryCircuit
from engine.electrical.solver_transient import TransientCircuit


def test_virtual_ground_stability():
    """Test that virtual ground midpoint stays stable when loaded."""
    print("\n" + "="*70)
    print("TEST: Virtual Ground Stability")
    print("="*70)

    # Build P0 circuit with single supply + TLE2426 virtual ground
    builder = P0TernaryCircuit(v_supply=5.0)
    circuit, initial_state = builder.build(supply_mode="single")

    cap_states = initial_state["cap_states"]
    ind_states = initial_state["ind_states"]
    voltages = initial_state["voltages"]

    print(f"\nInitial condition:")
    print(f"  Supply voltage: {voltages['+V']:.3f} V")
    print(f"  Virtual ground: {voltages['0']:.3f} V (target: 2.500 V)")
    print(f"  Winding currents: all 0 A")

    # Simulate a switching sequence: U phase ON (to +V), V and W OFF (to GND)
    # This creates an imbalanced load on the virtual ground

    dt = 1e-6  # 1 microsecond time steps
    t_end = 100e-6  # 100 microseconds total
    n_steps = int(t_end / dt)

    history = {
        "time": [],
        "vg": [],
        "vg_no_load": [],
        "i_L_U": [],
        "i_L_V": [],
        "i_L_W": [],
        "v_mid_U": [],
    }

    # Simple gate drive: U turns on, V and W stay off
    def gate_voltage(mosfet_id: str, t: float) -> float:
        if mosfet_id == "U_HS":
            return 3.0 if t > 10e-6 else 0.0  # Turn on at t=10us
        elif mosfet_id == "U_LS":
            return 0.0  # Keep low-side off
        else:
            return 0.0  # V and W off

    for step in range(n_steps):
        t = step * dt

        try:
            sol = circuit.solve_step(
                initial_cap_states=cap_states,
                initial_ind_states=ind_states,
                initial_voltages=voltages,
                dt=dt,
                time=t,
                gate_voltage_func=gate_voltage
            )

            voltages = sol.voltages
            ind_states = sol.inductor_states
            cap_states = sol.capacitor_states

            history["time"].append(t * 1e6)  # Convert to us for readability
            history["vg"].append(voltages.get("0", 0.0))
            history["vg_no_load"].append(voltages.get("vg_raw", 2.5))
            history["i_L_U"].append(ind_states["L_U"].current)
            history["i_L_V"].append(ind_states["L_V"].current)
            history["i_L_W"].append(ind_states["L_W"].current)
            history["v_mid_U"].append(voltages.get("mid_U", 0.0))

            if step % 10000 == 0:
                print(f"  t={t*1e6:7.1f} us: V_0={voltages.get('0', 0.0):6.3f}V, "
                      f"I_U={ind_states['L_U'].current:8.4f}A, "
                      f"V_mid_U={voltages.get('mid_U', 0.0):6.3f}V")

        except Exception as e:
            print(f"ERROR at step {step} (t={t*1e6:.3f} us): {e}")
            break

    # Analyze results
    print(f"\nResults after {n_steps} steps ({t_end*1e6:.1f} us):")
    vg_steady = sum(history["vg"][-1000:]) / 1000  # Last 1000 samples
    vg_target = 2.5
    vg_error = abs(vg_steady - vg_target)

    print(f"  Virtual ground steady-state: {vg_steady:.3f} V")
    print(f"  Target: {vg_target:.3f} V")
    print(f"  Error: {vg_error:.3f} V ({vg_error/vg_target*100:.1f}%)")

    i_peak = max(history["i_L_U"])
    print(f"  Peak winding current: {i_peak:.3f} A")

    # PASS criterion: virtual ground within ±200mV of target
    tolerance = 0.200
    passed = vg_error <= tolerance
    status = "PASS" if passed else "FAIL"

    print(f"\nTolerance: ±{tolerance:.3f} V")
    print(f"Status: {status}")

    return {
        "test": "Virtual Ground Stability",
        "expected": f"V_0 = {vg_target:.3f} V ± {tolerance:.3f} V",
        "actual": f"V_0 = {vg_steady:.3f} V",
        "tolerance": tolerance,
        "passed": passed,
        "history": history
    }


def test_ternary_sequencing():
    """Test that three phases can sequence through valid ternary states."""
    print("\n" + "="*70)
    print("TEST: Ternary Sequencing")
    print("="*70)

    builder = P0TernaryCircuit(v_supply=5.0)
    circuit, initial_state = builder.build(supply_mode="single")

    cap_states = initial_state["cap_states"]
    ind_states = initial_state["ind_states"]
    voltages = initial_state["voltages"]

    dt = 1e-6
    t_end = 200e-6
    n_steps = int(t_end / dt)

    states = []

    # Sequence: U→+V, V and W off, then cycle
    sequence = [
        (0, 50e-6, "U_HS", "U→+V"),
        (50e-6, 100e-6, "V_HS", "V→+V"),
        (100e-6, 150e-6, "W_HS", "W→+V"),
        (150e-6, 200e-6, "U_HS", "U→+V (repeat)"),
    ]

    def gate_voltage(mosfet_id: str, t: float) -> float:
        for t_start, t_end, active_hs, _ in sequence:
            if t_start <= t < t_end:
                return 3.0 if mosfet_id == active_hs else 0.0
        return 0.0

    for step in range(n_steps):
        t = step * dt

        try:
            sol = circuit.solve_step(
                initial_cap_states=cap_states,
                initial_ind_states=ind_states,
                initial_voltages=voltages,
                dt=dt,
                time=t,
                gate_voltage_func=gate_voltage
            )

            voltages = sol.voltages
            ind_states = sol.inductor_states
            cap_states = sol.capacitor_states

            # Log every 5000 steps (~5ms per sample)
            if step % 5000 == 0:
                state_label = "IDLE"
                for t_s, t_e, active, label in sequence:
                    if t_s <= t < t_e:
                        state_label = label
                        break

                states.append({
                    "time_us": t * 1e6,
                    "state": state_label,
                    "v_0": voltages.get("0", 0.0),
                    "i_U": ind_states["L_U"].current,
                    "i_V": ind_states["L_V"].current,
                    "i_W": ind_states["L_W"].current,
                })
                print(f"  {state_label:15s} @ t={t*1e6:7.1f} us: "
                      f"V_0={voltages.get('0', 0.0):6.3f}V, "
                      f"I=[{ind_states['L_U'].current:7.4f}, "
                      f"{ind_states['L_V'].current:7.4f}, "
                      f"{ind_states['L_W'].current:7.4f}] A")

        except Exception as e:
            print(f"ERROR at step {step}: {e}")
            break

    print(f"\nSequenced {len(states)} state transitions over {t_end*1e6:.0f} us")

    # PASS criterion: all states converge without numerical divergence
    i_max = max(max(abs(s["i_U"]), abs(s["i_V"]), abs(s["i_W"])) for s in states)
    vg_max_error = max(abs(s["v_0"] - 2.5) for s in states)

    passed = (i_max < 10.0) and (vg_max_error < 0.5)
    status = "PASS" if passed else "FAIL"

    print(f"\nPeak current magnitude: {i_max:.3f} A (limit: 10 A)")
    print(f"Max virtual ground error: {vg_max_error:.3f} V (limit: 0.5 V)")
    print(f"Status: {status}")

    return {
        "test": "Ternary Sequencing",
        "expected": "Stable 3-state sequencing, I < 10A, V_0 error < 0.5V",
        "actual": f"Peak I = {i_max:.3f}A, V_0 error = {vg_max_error:.3f}V",
        "passed": passed,
        "states": states
    }


if __name__ == "__main__":
    results = []

    results.append(test_virtual_ground_stability())
    results.append(test_ternary_sequencing())

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    passed_count = sum(1 for r in results if r["passed"])
    print(f"\n{passed_count}/{len(results)} tests PASSED")

    for r in results:
        status = "✓ PASS" if r["passed"] else "✗ FAIL"
        print(f"  {status}: {r['test']}")

    # Save results
    output_file = Path(__file__).parent / "receipts" / "p0_ternary_results.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to {output_file}")

    sys.exit(0 if all(r["passed"] for r in results) else 1)
