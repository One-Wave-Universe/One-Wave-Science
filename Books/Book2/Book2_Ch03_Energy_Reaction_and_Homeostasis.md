# ONE-WAVE FRAMEWORK
## Book 2 — Small
## Chapter 3: Energy, Reaction, and Homeostasis

**Status:** GRAY reference / YELLOW One-Wave comparison  
**Dependencies:** A-105 Restoring Response, A-108 Local Stability, A-111 Recursion  

---

## Gray

Cells are open thermodynamic systems. They exchange matter and energy with their surroundings, run coupled chemical reactions, and maintain concentrations far from equilibrium. "Balance" in biology does not mean every variable is equal. It means important variables are regulated within viable ranges while energy and material continue to flow.

For a reaction network with concentrations collected in vector $\mathbf c$, a compact model is

$$
\frac{d\mathbf c}{dt}=\mathbf S\,\mathbf v(\mathbf c,t),
$$

where $\mathbf S$ is the stoichiometric matrix and $\mathbf v$ contains reaction rates.

For a simple reversible reaction $A\rightleftharpoons B$,

$$
\frac{d[A]}{dt}=-k_f[A]+k_r[B],
$$

$$
\frac{d[B]}{dt}=k_f[A]-k_r[B].
$$

The total $[A]+[B]$ is conserved if nothing enters or leaves. Real cells add transport, synthesis, degradation, and energy coupling.

## 2D — regulation as state-space motion

Plot two measured cellular variables on perpendicular axes. A viable region is then an area rather than a single magical center point. The state may move continuously while remaining viable.

A simple negative-feedback controller can be written

$$
\tau\frac{dx}{dt}=-(x-x_*)+u(t),
$$

where $x_*$ is a reference state, $u$ is disturbance/input, and $\tau$ sets response time.

This makes a useful correction to careless "everything seeks perfect balance" language: living systems frequently maintain **asymmetric, driven steady states**.

## 3D — nested inventories

A cell contains many compartments. Each compartment can have its own inventory and exchange terms. For compartment $i$,

$$
\frac{dN_i}{dt}=\sum_j F_{j\to i}-\sum_kF_{i\to k}+P_i-C_i,
$$

with inflow $F$, production $P$, and consumption $C$. The whole-cell equation is obtained by summing compartments; internal transfers cancel in pairs.

That cancellation is important for One-Wave bookkeeping: an internal handoff is not external creation.

## Mathematics — free energy and driven state

At constant temperature and pressure, chemical reactions are commonly organized using Gibbs free-energy change:

$$
\Delta G=\Delta G^\circ+RT\ln Q.
$$

A negative $\Delta G$ indicates thermodynamic favorability in the stated direction under those conditions; it does not by itself specify the reaction rate.

A minimal dynamical homeostasis model with feedback is

$$
\dot x=f(x)+b\,u-k(x-x_*).
$$

Linearizing near $x_*$ gives

$$
\delta\dot x\approx\left[f'(x_*)-k\right]\delta x+b\,u.
$$

Local stability requires the effective coefficient to drive small deviations back rather than amplify them.

## One-Wave comparison

A-105 Restoring Response and A-108 Local Stability are structurally relevant to regulation. A-111 Recursion is relevant when state history changes the next response. The candidate mapping is:

- deviation from operating region → differential;
- regulatory response → restoring response;
- stable viable range → local stability;
- adaptation/history dependence → recursion.

This mapping is useful only if it stays measurable. "Homeostasis equals One-Wave balance" is too vague to test.

## Graph requirement

For every proposed regulated variable, show:

- reference/viable band;
- perturbation time;
- measured or simulated response;
- recovery time and overshoot;
- comparison with an ordinary feedback control.

A plot that hides the control comparison does not establish a One-Wave advantage.

## Predictions / tests

1. Perturb one variable and estimate its return rate instead of merely saying it restores.
2. Compare one-state and history-dependent models. Recursion is justified only if history materially improves prediction.
3. Separate stability from equality: test nonzero steady states and asymmetric flows.
4. Check conservation by summing compartment inventories and external fluxes.

## Yellow Audit

- Cellular regulation is established biology; its identification with One-Wave primitives remains interpretive.
- No universal restoring coefficient is derived here.
- Thermodynamic favorability must not be confused with kinetics.
- A stable state need not be zero, symmetric, or static.

## Future Work

Choose one well-measured cellular feedback loop and fit a minimal standard model and a candidate recursive model against the same time-series data.

## Closing Thoughts

A living cell is not a statue at equilibrium. It is a driven system that keeps selected variables inside workable ranges while continuously processing energy and material. Any useful One-Wave account of "balance" has to preserve that fact.
