# Zer0 first cycle — what is proved vs not

Home: Science. Iron stays in Builds. Pipes stay in Bridge-Comand.

## Claim class

This is a **grammar proof**, not a physics proof and not a CELL proof.

Builds `algorithms/IMPLEMENTATION_STATUS.md` already said the implementation gap is one shared event through X,Y,Z,T with HOLD, resolve, and a bounded next reference that depends on the last cycle.

The file `simulations/zer0_first_cycle.py` is that harness. It passed locally 2026-09-28:

- bounded rebase (same-sign flood never leaves `[-1,1]`)
- HOLD is a real third outcome inside the dead band
- next reference depends on the prior resolved cycle
- XYZ disagreement is HOLD, not a hidden arbiter

## Math (one branch)

Let reference \(r_t \in [-1,1]\), input \(u_t\).

\[
\delta_t = u_t - r_t
\]

\[
c_t =
\begin{cases}
+ & \delta_t > d \\
- & \delta_t < -d \\
0 & |\delta_t| \le d
\end{cases}
\]

\(d\) is the HOLD dead band (sim uses \(0.05\)).

Move is \(m_t \in \{-1,0,+1\}\) from \(c_t\).
Consequence \(\kappa_t = m_t\,|\delta_t|\) (zero on HOLD).

Shared resolve: two-of-three on \(\{c^X,c^Y,c^Z\}\). T does not vote. Split vote \(\to 0\).

Rebase:

\[
r_{t+1} =
\begin{cases}
r_t & c=0 \\
\mathrm{clip}\big((1-\alpha)r_t + \alpha\,\mathrm{sign}(c)\,|\bar\kappa|\big) & c\neq 0
\end{cases}
\]

\(\alpha=0.25\) in the sim. Clip is to \([-1,1]\).

That is the **moving zero**: new baseline referenced to the last resolved consequence. Nothing discarded except by clip, which is the bounded-loss rule.

## What this does not prove

- Helmholtz gap fields
- transfluxor remanence
- nested scalar\(\subset\)differential\(\subset\)vector\(\subset\)tensor\(\subset\)stratum\(\subset\)harmonic as physics
- that software memory is CELL memory (it is not)
- Rabbit Hopping addressing (separate arithmetic artifact)

## Next proofs, in order

1. Same harness with *unequal* branch weights / delayed T closure.
2. Map \(\delta\) onto a toy opposed-pair (two numbers, opposite sign, shared mid) — still software.
3. Helmholtz / mutual-inductance numeric in Science `simulations/`, parameters from Builds `cell-v1` only.
4. Physical history test on a real core. That result goes to Builds, not here.

## How to run

```bash
python3 simulations/zer0_first_cycle.py
```

Expect `PASS`.
