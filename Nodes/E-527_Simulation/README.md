# E-527 Simulation Artifacts

These files are the canonical Bronze validation artifacts for node
E-527.

Run:

```bash
python simulate_e527.py
```

The script regenerates all CSV, PNG, and JSON outputs and executes
assertions for the three tested regimes.

## Cases

1. `case_1_constant_supply_plateau.*`
   Tests the rejected product-only cycle claim under constant supply.

2. `case_2_finite_substrate_single_pulse.*`
   Shows that one finite reservoir creates one pulse, not a repeating
   oscillator.

3. `case_3_hybrid_relaxation_cycle.*`
   Tests the corrected recharge/depletion/hysteresis model.

4. `parameter_sweep.*`
   Maps the analytic inequalities over settled synchronization and
   depletion strength.

`simulation_metadata.json` records software versions, parameters,
script hash, numerical results, assertions, and scope limits.
