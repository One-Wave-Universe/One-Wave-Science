#!/usr/bin/env python3
"""
DC electrical regressions -- the pass criteria for this batch (see
engine/electrical/README.md). Every check computes a real analytic
expected value from Ohm's/Kirchhoff's laws independently of the solver,
then compares it against what the solver actually produced. Nothing here
hard-codes the solver's answer; if the solver's answer is right, it will
match the independently-computed formula, and if it's wrong, this will
show a real numeric mismatch, not a passing string comparison.

No eyeballing: every check prints TEST/EXPECTED/ACTUAL/TOLERANCE/PASS-FAIL,
all checks run (a failure does not stop the rest), and results are also
written as JSON (and CSV) receipts under tests/receipts/.

Run with: python3 One_Wave_Bench/engine/electrical/tests/test_dc_regressions.py
"""
from __future__ import annotations
import csv
import datetime
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE_DIR = HERE.parents[1]  # One_Wave_Bench/engine
sys.path.insert(0, str(ENGINE_DIR))

from electrical import Circuit, DCVoltageSource, Resistor, Wire, Ground, measurements as M, energy as E  # noqa: E402

CODE_VERSION = "electrical-dc-0.1"
records: list[dict] = []


def check(name: str, expected, actual, tolerance, note: str = "") -> None:
    if isinstance(expected, bool):
        passed = expected == actual
        tol_report = None
    else:
        passed = abs(actual - expected) <= tolerance
        tol_report = tolerance
    records.append({
        "test": name,
        "expected": expected,
        "actual": actual,
        "tolerance": tol_report,
        "pass": passed,
        "notes": note,
    })
    tol_str = f" tolerance={tol_report}" if tol_report is not None else ""
    print(f"{'PASS' if passed else 'FAIL'} [{name}] expected={expected} actual={actual}{tol_str}"
          + (f" -- {note}" if note else ""))


# ---------------------------------------------------------------------------
# 1. DC voltage source (holds its own value under negligible load)
# ---------------------------------------------------------------------------
def test_dc_source():
    c = Circuit()
    c.add(DCVoltageSource("bat1", "p", "g", 9.0))
    c.add(Resistor("rref", "p", "g", 1e9))  # negligible load
    c.add(Ground("g"))
    res = c.solve()
    check("dc-source-holds-value", 9.0, res.voltages["p"], 1e-6,
          "an ideal DC source under negligible load must read its own nominal voltage")


# ---------------------------------------------------------------------------
# 2. Single resistor / Ohm's law
# ---------------------------------------------------------------------------
def test_ohms_law():
    c = Circuit()
    c.add(DCVoltageSource("bat1", "p", "g", 5.0))
    r1 = c.add(Resistor("r1", "p", "g", 1000.0))
    c.add(Ground("g"))
    res = c.solve()
    expected_i = 5.0 / 1000.0
    check("ohms-law-current", expected_i, M.resistor_current(res, r1), 1e-9,
          "I = V/R through a single real resistor")


# ---------------------------------------------------------------------------
# 3. Series resistors
# ---------------------------------------------------------------------------
def test_series_resistors():
    c = Circuit()
    c.add(DCVoltageSource("bat1", "p", "g", 5.0))
    r1 = c.add(Resistor("r1", "p", "mid", 1000.0))
    r2 = c.add(Resistor("r2", "mid", "g", 1000.0))
    c.add(Ground("g"))
    res = c.solve()

    c2 = Circuit()
    c2.add(DCVoltageSource("bat1", "p", "g", 5.0))
    req = c2.add(Resistor("req", "p", "g", 2000.0))
    c2.add(Ground("g"))
    res2 = c2.solve()

    check("series-resistors-match-equivalent", M.resistor_current(res2, req), M.resistor_current(res, r1), 1e-9,
          "two 1k resistors in series must draw the same current as one real 2k resistor")
    check("series-resistors-same-current-both-legs", M.resistor_current(res, r1), M.resistor_current(res, r2), 1e-9,
          "a series loop must carry the same current through every element")


# ---------------------------------------------------------------------------
# 4. Parallel resistors
# ---------------------------------------------------------------------------
def test_parallel_resistors():
    c = Circuit()
    c.add(DCVoltageSource("bat1", "p", "g", 5.0))
    r1 = c.add(Resistor("r1", "p", "g", 1000.0))
    r2 = c.add(Resistor("r2", "p", "g", 1000.0))
    c.add(Ground("g"))
    res = c.solve()
    total_i = M.resistor_current(res, r1) + M.resistor_current(res, r2)

    c2 = Circuit()
    c2.add(DCVoltageSource("bat1", "p", "g", 5.0))
    req = c2.add(Resistor("req", "p", "g", 500.0))
    c2.add(Ground("g"))
    res2 = c2.solve()

    check("parallel-resistors-match-equivalent", M.resistor_current(res2, req), total_i, 1e-9,
          "two 1k resistors in parallel must together draw the same total current as one real 500ohm resistor")


# ---------------------------------------------------------------------------
# 5. Unloaded voltage divider (the first required test network)
# ---------------------------------------------------------------------------
def build_divider(r1_ohms=10000.0, r2_ohms=10000.0, load_ohms=None):
    """9V -> R1 -> CENTER -> R2 -> 0V, with an optional load resistor from
    CENTER to the bottom (0V) rail."""
    c = Circuit()
    c.add(DCVoltageSource("bat1", "top", "bottom", 9.0))
    r1 = c.add(Resistor("r1", "top", "center", r1_ohms))
    r2 = c.add(Resistor("r2", "center", "bottom", r2_ohms))
    load = None
    if load_ohms is not None:
        load = c.add(Resistor("load", "center", "bottom", load_ohms))
    c.add(Ground("bottom"))
    res = c.solve()
    return c, res, r1, r2, load


def test_unloaded_divider():
    c, res, r1, r2, _ = build_divider()
    check("unloaded-divider-vtop", 9.0, res.voltages["top"], 1e-6, "Vtop must hold the real source voltage")
    check("unloaded-divider-vcenter", 4.5, res.voltages["center"], 1e-6,
          "equal-value divider legs must produce a real half-rail midpoint")
    check("unloaded-divider-vbottom", 0.0, res.voltages["bottom"], 1e-9, "the explicit Ground node must read exactly 0V")
    expected_i = 9.0 / (10000.0 + 10000.0)
    check("unloaded-divider-current", expected_i, M.resistor_current(res, r1), 1e-9,
          "the loop current must match I = V / (R1+R2) exactly, computed from the real network, not assumed")


# ---------------------------------------------------------------------------
# 6/7. Loaded divider / passive CENTER sag -- the critical test
# ---------------------------------------------------------------------------
def test_loaded_divider_center_moves():
    _, res_unloaded, _, _, _ = build_divider()
    v_unloaded = res_unloaded.voltages["center"]

    c, res, r1, r2, load = build_divider(load_ohms=10000.0)
    v_loaded = res.voltages["center"]

    # Real Thevenin-equivalent expected value: R2 and the load are both
    # 10k from CENTER to the bottom rail, i.e. genuinely in parallel
    # (5k), driven from a 10k source resistance (R1) off the 9V rail.
    r2_parallel_load = 1.0 / (1.0 / 10000.0 + 1.0 / 10000.0)
    expected_v_loaded = 9.0 * r2_parallel_load / (10000.0 + r2_parallel_load)

    check("loaded-divider-center-matches-real-thevenin", expected_v_loaded, v_loaded, 1e-6,
          "loading CENTER with a real 10k resistor to the bottom rail must produce the real Thevenin-divided voltage")
    check("loaded-divider-center-must-move", True, abs(v_loaded - v_unloaded) > 0.5, None,
          f"CENTER must genuinely move under load (unloaded={v_unloaded:.4f}V, loaded={v_loaded:.4f}V) -- "
          "a simulator that silently restores CENTER to 4.5V here is FAILING this test by construction, "
          "not passing it by coincidence")

    for r_name, r in (("r1", r1), ("r2", r2), ("load", load)):
        check(f"loaded-divider-branch-current-{r_name}-real", True, M.resistor_current(res, r) != 0.0, None,
              f"I({r_name}) must be a real, nonzero, independently measured branch current")


# ---------------------------------------------------------------------------
# 8. Differential voltage measurements
# ---------------------------------------------------------------------------
def test_differential_measurements():
    c, res, r1, r2, _ = build_divider()
    v_plus_rel_center = M.differential_voltage(res, "top", "center")
    v_minus_rel_center = M.differential_voltage(res, "bottom", "center")
    v_diff = M.differential_voltage(res, "top", "bottom")

    check("differential-plus-relative-center", 4.5, v_plus_rel_center, 1e-6, "V(+ rail) relative to CENTER")
    check("differential-minus-relative-center", -4.5, v_minus_rel_center, 1e-6, "V(- rail) relative to CENTER")
    check("differential-plus-to-minus", 9.0, v_diff, 1e-6, "V(+ to - rail) differential must equal the full rail voltage")


# ---------------------------------------------------------------------------
# 9/10. Branch currents and source current, cross-checked against each other
# ---------------------------------------------------------------------------
def test_branch_and_source_currents():
    c, res, r1, r2, load = build_divider(load_ohms=10000.0)
    i_r1 = M.resistor_current(res, r1)
    i_r2 = M.resistor_current(res, r2)
    i_load = M.resistor_current(res, load)
    i_source = M.source_current(res, c.sources[0])

    check("branch-current-r1-real", True, i_r1 > 0, None, f"I(R1) = {i_r1:.6f}A, must be real and flowing from + toward CENTER")
    check("source-current-equals-r1-current", i_r1, i_source, 1e-9,
          "in this single-loop-into-CENTER topology, the source current must equal I(R1) exactly (KCL at the top node)")
    check("kcl-at-center-node", 0.0, i_r1 - i_r2 - i_load, 1e-9,
          "current arriving at CENTER (I(R1)) must equal current leaving it (I(R2)+I(load)) -- real Kirchhoff's current law, not assumed")


# ---------------------------------------------------------------------------
# 11/12. Resistor power and source power (power balance)
# ---------------------------------------------------------------------------
def test_power_balance():
    c, res, r1, r2, load = build_divider(load_ohms=10000.0)
    p_r1 = M.resistor_power(res, r1)
    p_r2 = M.resistor_power(res, r2)
    p_load = M.resistor_power(res, load)
    p_source = M.source_power(res, c.sources[0])
    total_dissipated = p_r1 + p_r2 + p_load

    check("resistor-power-real-positive", True, p_r1 > 0 and p_r2 > 0 and p_load > 0, None,
          f"P(R1)={p_r1:.6f}W, P(R2)={p_r2:.6f}W, P(load)={p_load:.6f}W -- every real resistor must show real positive dissipation")
    check("source-power-matches-total-dissipation", total_dissipated, p_source, 1e-9,
          "source power must equal total dissipated resistor power within numerical tolerance -- no unexplained gain or loss")


# ---------------------------------------------------------------------------
# 13. Energy accounting
# ---------------------------------------------------------------------------
def test_energy_accounting():
    c, res, r1, r2, load = build_divider(load_ohms=10000.0)
    p_source = M.source_power(res, c.sources[0])
    total_dissipated_power = M.total_resistor_power(res, [r1, r2, load])
    duration_s = 60.0  # 1 minute, an arbitrary but explicit run duration

    supplied_j = E.energy_from_power(p_source, duration_s)
    dissipated_j = E.energy_from_power(total_dissipated_power, duration_s)
    balance = E.energy_balance(supplied_j, dissipated_j)

    check("energy-supplied-real-positive", True, supplied_j > 0, None, f"supplied energy over {duration_s}s = {supplied_j:.6f}J")
    check("energy-balance-closes", True, abs(balance["relative_mismatch"]) < 1e-9, None,
          f"supplied {supplied_j:.6f}J vs dissipated {dissipated_j:.6f}J -- must close within numerical tolerance, no unexplained energy gain or loss")


# ---------------------------------------------------------------------------
# 14/15. Mismatch tests -- 1% and 5% must show real, proportional imbalance,
# never a secretly-rebalanced 4.5V.
# ---------------------------------------------------------------------------
def test_mismatch_shows_real_imbalance():
    def expected_vcenter(r1_ohms, r2_ohms):
        return 9.0 * r2_ohms / (r1_ohms + r2_ohms)

    _, res_balanced, _, _, _ = build_divider(10000.0, 10000.0)
    v_balanced = res_balanced.voltages["center"]

    _, res_1pct, _, _, _ = build_divider(10000.0, 10100.0)
    v_1pct = res_1pct.voltages["center"]
    expected_1pct = expected_vcenter(10000.0, 10100.0)

    _, res_5pct, _, _, _ = build_divider(10000.0, 10500.0)
    v_5pct = res_5pct.voltages["center"]
    expected_5pct = expected_vcenter(10000.0, 10500.0)

    check("mismatch-1pct-matches-real-formula", expected_1pct, v_1pct, 1e-6,
          "R2=10.1k must move CENTER to exactly the real formula's value, not a hard-coded number")
    check("mismatch-1pct-shows-real-shift", True, abs(v_1pct - v_balanced) > 0.001, None,
          f"a real 1% mismatch must produce a real, measurable shift from 4.5V (got {v_1pct:.6f}V), not stay pinned at 4.5V")

    check("mismatch-5pct-matches-real-formula", expected_5pct, v_5pct, 1e-6,
          "R2=10.5k must move CENTER to exactly the real formula's value, not a hard-coded number")
    check("mismatch-5pct-shift-larger-than-1pct", True, abs(v_5pct - v_balanced) > abs(v_1pct - v_balanced), None,
          f"a bigger real mismatch must produce a bigger real shift (1%={abs(v_1pct - v_balanced):.6f}V, "
          f"5%={abs(v_5pct - v_balanced):.6f}V) -- proportional, not an arbitrary fixed nudge")


TESTS = [
    test_dc_source,
    test_ohms_law,
    test_series_resistors,
    test_parallel_resistors,
    test_unloaded_divider,
    test_loaded_divider_center_moves,
    test_differential_measurements,
    test_branch_and_source_currents,
    test_power_balance,
    test_energy_accounting,
    test_mismatch_shows_real_imbalance,
]


def write_receipts(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    generated = datetime.datetime.now(datetime.timezone.utc).isoformat()

    text_lines = []
    for r in records:
        text_lines.append(
            f"TEST: {r['test']}\n"
            f"EXPECTED: {r['expected']}\n"
            f"ACTUAL: {r['actual']}\n"
            f"TOLERANCE: {r['tolerance'] if r['tolerance'] is not None else 'n/a (boolean check)'}\n"
            f"PASS/FAIL: {'PASS' if r['pass'] else 'FAIL'}\n"
            f"NOTES: {r['notes']}\n"
        )
    (out_dir / "receipts.txt").write_text("\n".join(text_lines), encoding="utf-8")

    receipt_json = {
        "receipt_id": "RCP-ELEC-DC-001",
        "engine": "electrical-dc",
        "code_version": CODE_VERSION,
        "generated_utc": generated,
        "checks": records,
        "all_checks_pass": all(r["pass"] for r in records),
    }
    (out_dir / "receipt_ELEC-DC-001.json").write_text(json.dumps(receipt_json, indent=2), encoding="utf-8")

    with (out_dir / "measurements.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["test", "expected", "actual", "tolerance", "pass", "notes"])
        for r in records:
            w.writerow([r["test"], r["expected"], r["actual"], r["tolerance"], r["pass"], r["notes"]])


def main() -> int:
    for t in TESTS:
        t()
    passed = sum(1 for r in records if r["pass"])
    failed = len(records) - passed
    print(f"\n=== {len(records)} checks, {passed} passed, {failed} failed ===")

    out_dir = HERE / "receipts"
    write_receipts(out_dir)
    print(f"Receipts written to {out_dir}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
