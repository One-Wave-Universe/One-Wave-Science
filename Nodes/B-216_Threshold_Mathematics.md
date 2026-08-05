---
node_id: "B-216"
canonical_name: "Threshold Mathematics"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Resolution / Formalization Node"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node B-216: Threshold Mathematics

Dependencies:
Upstream: B-207 Threshold State, B-208 Threshold Windows, G-712 Evaluation Mathematics
Downstream: B-209 Break Condition, B-210 Return, G-713 Modulation Mathematics,
G-714 Decision Mathematics

## State

Define the normalized threshold state

```text
Theta_n = [q_n, a_n, p_n]^T
```

with domain

```text
Omega = [0,1] x [0,1] x [-1,1].
```

Let the desired or currently selected reference state be

```text
Theta*_n = [q*_n, a*_n, p*_n]^T.
```

The evaluation error is

```text
e_n = Theta_n - Theta*_n.
```

## Controlled Update

The minimal discrete update is

```text
Theta_(n+1) = Pi_Omega(Theta_n + B u_n + w_n)
```

where:

- `u_n = [u_q, u_a, u_p]^T` is the modulation command,
- `B` maps each command into the state variables,
- `w_n` is measured disturbance or modeling error,
- `Pi_Omega` clips the result to the valid state domain.

For the simplest internally testable case, take `B = I` and use proportional
restoration:

```text
u_n = -K e_n
K = diag(k_q, k_a, k_p).
```

Ignoring clipping and disturbance for the local stability calculation:

```text
e_(n+1) = (I - K)e_n.
```

The reference state is asymptotically stable when every gain satisfies

```text
0 < k_q < 2
0 < k_a < 2
0 < k_p < 2.
```

Reason: each scalar error evolves as

```text
e_(j,n+1) = (1-k_j)e_(j,n),
```

and therefore decays exactly when

```text
|1-k_j| < 1.
```

This is an internal mathematical result, not an experimental calibration.

## Separate-Axis Consequence

Because `a` and `p` are separate coordinates, the controller can reduce
activation without changing polarity:

```text
u_a < 0,  u_p = 0.
```

It can redirect polarity without raising activation:

```text
u_a = 0,  u_p != 0.
```

This formally establishes the earlier verbal correction that healthy
energy reduction is not the same operation as compression or retreat.

## Integrity Update from Mismatch

For two coupled participants or subsystems with local states

```text
s_1 = [a_1,p_1]^T
s_2 = [a_2,p_2]^T,
```

define normalized mismatch

```text
d_n = min(1, sqrt(w_a(a_1-a_2)^2 + w_p(p_1-p_2)^2)).
```

A candidate integrity update is

```text
q_(n+1) = clip(q_n + eta(1-d_n) - mu d_n - xi O_n, 0, 1)
```

where:

- `eta >= 0` is restoration strength,
- `mu >= 0` is mismatch cost,
- `O_n >= 0` is overload exposure,
- `xi >= 0` is overload damage weight.

One candidate overload exposure is

```text
O_n = [a_n - a_danger]_+,
[x]_+ = max(x,0).
```

This makes high activation harmful only when it exceeds a chosen danger boundary;
low activation does not directly reduce integrity.

## Return and Break Conditions

Define parameters

```text
0 <= q_break < q_return <= 1.
```

Then:

```text
Break candidate:  q_n <= q_break
Return candidate: q_(n+1) >= q_n AND q_(n+1) >= q_return
Hold:             |q_(n+1)-q_n| <= epsilon_q
```

A hysteresis gap `q_return > q_break` prevents rapid flip-flopping at one
boundary.

## Reset Condition

Let `N_danger` count consecutive steps for which

```text
a_n >= a_danger AND q_(n+1) < q_n.
```

A reset candidate occurs when

```text
N_danger >= N_reset.
```

This distinguishes a brief peak from sustained overload.

## Internal Consistency Checks Completed

1. **Boundedness:** projection keeps all state variables in their declared domains.
2. **Axis independence:** activation and polarity can change independently.
3. **Rest is not break:** `a -> 0` does not force `q -> 0`.
4. **Hysteresis:** separate break and return boundaries prevent one-step chatter.
5. **Local stability:** proportional control converges for gains in `(0,2)`.
6. **Overload duration:** reset depends on sustained exposure, not one high sample.

These checks satisfy the Green-to-Yellow requirement for an explicit,
internally testable mathematical model.

## Yellow Audit

- The integrity law is a candidate model; `eta`, `mu`, `xi`, and the mismatch
  weights require calibration.
- Scale-specific measurements for `a`, `p`, and `q` must be defined.
- Noise response and delayed feedback remain unresolved.
- Bronze requires a reproducible simulation with metadata and recorded failures.
