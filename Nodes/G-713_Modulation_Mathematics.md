---
node_id: "G-713"
canonical_name: "Modulation Mathematics"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Resolution / Formalization Node"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node G-713: Modulation Mathematics

Dependencies:
Upstream: G-703 Modulation, G-712 Evaluation Mathematics,
B-216 Threshold Mathematics
Downstream: G-714 Decision Mathematics, G-716 One-Wave Conversion Grammar

## State and Candidate Controls

Let

```text
Theta_n = [q_n,a_n,p_n]^T
```

and let each available action `r` provide a bounded candidate command

```text
u^(r) = [u_q^(r),u_a^(r),u_p^(r)]^T.
```

Example action templates:

```text
Hold:      [0, 0, 0]
Increase:  [0, +delta_a, 0]
Decrease:  [0, -delta_a, 0]
Redirect:  [0, 0, -k_p(p_n-p*_n)]
Stabilize: -K(Theta_n-Theta*_n)
Reject:    [-delta_q, 0, 0] with gate closure metadata
Admit:     [+delta_q, 0, 0] with gate opening metadata
```

`Reject` and `Admit` must still obey G-720: they modify one's own access and
participation, not another independent system's internal state.

## Predicted Next State

For action `r`:

```text
Theta_hat^(r) = Pi_Omega(Theta_n + B u^(r)).
```

## Cost Function

Choose the action minimizing

```text
J(r) =
  (Theta_hat^(r)-Theta*_n)^T W (Theta_hat^(r)-Theta*_n)
  + rho ||u^(r)||^2
  + lambda_D D(Theta_hat^(r))
  + lambda_S S(r).
```

where:

- `W` weights integrity, activation, and polarity errors,
- `rho` penalizes unnecessary control effort,
- `D` penalizes danger states,
- `S` penalizes actions that violate scale-specific safety or access constraints.

A candidate danger penalty is

```text
D(Theta) = [a-a_danger]_+^2 + [q_break-q]_+^2.
```

The selected action is

```text
r_n = argmin_r J(r).
```

This replaces the earlier undefined `argmax utility` placeholder with an
explicit bounded optimization rule.

## Continuous Control Form

When actions are allowed to blend rather than remain discrete, use

```text
u_n = argmin_u
      (Theta_n + Bu - Theta*)^T W (Theta_n + Bu - Theta*)
      + rho u^T u
```

subject to

```text
u_min <= u <= u_max.
```

Without active bounds and with `B=I`, the minimizer is

```text
u_n = -(W + rho I)^(-1) W (Theta_n-Theta*).
```

Every eigenvalue of `(W + rho I)^(-1)W` lies in `[0,1)`, so the command moves
toward the reference without an unbounded one-step overshoot in the ideal
noise-free case.

## Down-Modulation Result

If activation exceeds its reference, `a_n > a*_n`, the continuous solution has

```text
u_a < 0.
```

Therefore Decrease is selected mathematically when it lowers state error and
danger cost more than its control effort. Lowering energy is not a special
failure path; it follows from the same optimization rule as increasing it.

## Internal Tests Completed

1. The action set spans hold, amplitude change, polarity change, access change,
   and restoration.
2. The cost function penalizes overload and broken integrity separately.
3. The continuous minimizer is finite for `rho > 0`.
4. Independent axis weights allow activation and polarity to be controlled
   separately.
5. A bounded command set prevents the optimizer from demanding impossible
   movement.

## Yellow Audit

- `W`, `rho`, `lambda_D`, and `lambda_S` require scale-specific calibration.
- The access-safety penalty must be instantiated for hardware, individuals, and
  groups separately under I-04.
- Bronze requires executing this selection rule across representative
  trajectories and recording successes and failures.
