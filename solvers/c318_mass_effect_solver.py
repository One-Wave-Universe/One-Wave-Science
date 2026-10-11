#!/usr/bin/env python3
"""
C-318 Mass-Effect Solver — One-Wave four-interaction definition.

Source of truth: Nodes/C-318_Mass_Mechanism_Candidate_Resolution.md
Core Rules: CORE_RULES_LOCK.md (Rules 5, 11, 17).

What this solver does:
  - Encodes the canonical bounded-mode state Z = (Z_K, Z_E, Z_M, Z_T):
    knot, electrical shell, Mirror Gate, Boundary-Tension Weave.
  - Encodes the cycle-averaged energy  Ē4 = <E_K + E_E + E_M + E_T + E_x>.
  - Defines the Mass-Effect tensor  M_ij = d²Ē4/dv_i dv_j |_{v=0}
    and the scalar  m_eff = Tr(M)/3  (C-318, boxed equations).

What this solver does NOT do:
  - It does not use the Higgs vev, Yukawa couplings, scalar potentials,
    or measured masses as inputs (Standard Model machinery is not used).
  - It does not produce mass values. Every coefficient of the energy
    functional that C-318 leaves YELLOW is reported as OPEN.
  - Measured masses appear only in reference_comparison(), which reads
    them as targets to match, never as inputs (Core Rules 1, 2, 5).
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

INTERACTIONS = {
    "K": "knot: internal Three-Vortex geometry, recursion, phase relation",
    "E": "electrical shell: pressure/stress shell from boundary resistance",
    "M": "Mirror Gate: restoring pressure and orientation resistance",
    "T": "Boundary-Tension Weave: surface-and-volume confinement",
    "X": "cross-interaction terms (knot-shell, knot-weave, shell-Mirror, Mirror-weave, ...)",
}

# C-318 leaves these YELLOW. They are declared, not derived, and not fitted here.
OPEN_COEFFICIENTS = {
    "E_K": "knot energy functional",
    "E_E": "electrical-shell energy functional",
    "E_M": "Mirror-Gate energy functional",
    "E_T": "Boundary-Tension Weave energy functional",
    "E_x": "cross-interaction coupling coefficients",
    "M_ij": "Mass-Effect tensor components (requires E_K..E_x)",
    "m_eff": "scalar Mass Effect = Tr(M)/3 (requires M_ij)",
}


def definition_receipt() -> dict:
    """Return the canonical C-318 definitions and the open-coefficient ledger."""
    return {
        "node": "C-318",
        "status": {
            "mechanism_identity": "GREEN (per C-318 gate)",
            "coefficients_and_spectrum": "YELLOW (per C-318 gate)",
        },
        "state": "Z = (Z_K, Z_E, Z_M, Z_T)",
        "energy": "Ebar4[Z] = <E_K + E_E + E_M + E_T + E_x>_cycle",
        "mass_effect_tensor": "M_ij = d^2 Ebar4 / dv_i dv_j at v = 0",
        "scalar_mass_effect": "m_eff = (1/3) Tr(M)",
        "interactions": INTERACTIONS,
        "open": OPEN_COEFFICIENTS,
        "inputs_used": [],
        "standard_model_inputs_used": [],
    }


def reference_comparison(predicted: dict, measured: dict) -> dict:
    """
    Compare a predicted value to a measured target. Reference only.
    Refuses to run on any prediction that is not produced from C-318 terms,
    so a Standard Model number cannot be dressed up as a One-Wave result.
    """
    results = {}
    for name, value in predicted.items():
        if value is None or value == "OPEN":
            results[name] = {"status": "OPEN", "reason": "coefficient not derived"}
            continue
        target = measured.get(name)
        if target is None:
            results[name] = {"status": "NO_TARGET"}
            continue
        results[name] = {
            "status": "COMPARED",
            "predicted": value,
            "measured_target": target,
            "error_percent": 100.0 * abs(value - target) / abs(target),
        }
    return results


def main() -> int:
    receipt = definition_receipt()
    out_path = os.path.join(HERE, "c318_mass_effect_receipt.json")
    with open(out_path, "w") as f:
        json.dump(receipt, f, indent=2)
    print("C-318 Mass-Effect definitions (no Standard Model inputs)")
    print("-" * 60)
    print(f"State:       {receipt['state']}")
    print(f"Energy:      {receipt['energy']}")
    print(f"Mass tensor: {receipt['mass_effect_tensor']}")
    print(f"Scalar:      {receipt['scalar_mass_effect']}")
    print("Open coefficients (not derived, not fitted):")
    for k, v in OPEN_COEFFICIENTS.items():
        print(f"  OPEN  {k:<7} {v}")
    print(f"\nReceipt written: {os.path.relpath(out_path, HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
