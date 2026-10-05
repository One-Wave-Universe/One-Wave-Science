# Resistance/change timing: executed propagation control

Interpretation owner: [E-533](../Nodes/E-533_Superfluid_Transport_Time_Dilation.md).
This receipt tests observables from the existing A-114 recurrence. It does not
equate a packet's carrier phase with the internal clock of a bounded excitation.

Reference main: `a7a1b0bea412600edaed60b374a38d85c2343f4e`.
Authorities read: Book1 Ch16a, A-114, C-309, E-509, E-533, E-528, Book5 Ch6,
AGENTS and General Reference Rules. Existing metadata gates remain unchanged.

## Executed model

Native geometry: one-dimensional periodic nearest-neighbor control, 1024 sites,
unit spacing and unit step; not native 3D FCC or a physical superfluid simulation.
Complex values encode two real copies of the same linear recurrence:

    psi_(n+1) = (2-gamma) psi_n - (1-gamma) psi_(n-1)
                 + beta[(psi_(i+1)+psi_(i-1))/2-psi_i].

The exact characteristic equation is

    z²-[2-gamma+beta(cos k-1)]z+(1-gamma)=0.

For the oscillatory lower-imaginary branch, omega=-arg z,
decay=-log|z| and v_g=d omega/dk. The packet is a Gaussian of width 24 with
carrier k=.5,1,1.5. beta=.5; gamma=0,.05,.1; each run lasts 240 updates.
Initialization uses the root to select a traveling branch; subsequent evolution
executes the nearest-neighbor recurrence in real space. No trajectory is imposed.

Packet position is its density-weighted circular centroid. The code measures
its velocity by regression and samples the complex field at the moving centroid
by spectral interpolation. It also evolves a single carrier independently to
measure frequency, and measures packet norm decay. The moving phase rate is
compared with omega-k v_g, rather than defined as a proper-time rate.

## Run and receipts

    python solvers/time_resistance_probe.py

Requires NumPy. Prints JSON and returns exit 1 if any of five controls fails.
Code: [time_resistance_probe.py](time_resistance_probe.py).
Raw run: [time_resistance_results.json](time_resistance_results.json).
Environment: Python 3.12.14, NumPy 2.3.5 in the isolated execution workspace.
This receipt does not claim the Jetson executed the scientific run.

Five controls pass across nine runs: characteristic residual <1e-12,
carrier frequency error <1e-10, packet speed error <.003, moving phase-rate
error <.003, packet amplitude-decay error <1e-6. Actual packet speed errors
are below 8.56e-5 in the published run. These are numerical controls; passing
them is not a successful physical time-dilation test.

| k | gamma | Carrier omega | Measured speed | Measured moving phase rate |
|---|---|---:|---:|---:|
| .5 | 0 | .24803931 | .48816353 | .00391634 |
| .5 | .1 | .24912675 | .51249989 | -.00720580 |
| 1 | 0 | .48413997 | .45192263 | .03213210 |
| 1 | .1 | .49441396 | .46727217 | .02705062 |
| 1.5 | 0 | .69557664 | .38909276 | .11180415 |
| 1.5 | .1 | .71284296 | .40188856 | .10987281 |

The raw file preserves the intermediate gamma=.05 cases too.

## What the result establishes and rejects

The recurrence has measurable transport, oscillation and damping. Increasing
gamma does not universally slow carrier oscillation: at k=1 the frequency
increases from .48414 to .49441. Thus simply identifying gamma with every form
of transport difficulty, and frequency with all internal change, does not yield
the proposed universal slowing mechanism.

For gamma=0,k=1, the exact normalized moving carrier phase rate is .06645,
whereas sqrt(1-(v_g/c_longwave)²) is .42766 with c_longwave=sqrt(beta/2)=.5.
The square-root comparator is evaluated after the run; it is absent from
the recurrence. This demonstrates failure of *that carrier-clock identification*,
not a failure of a still-unconstructed self-held clock's timing law.

The gamma=.1,k=.5 group speed exceeds the undamped long-wave value .5, while
remaining below the strict nearest-neighbor front bound 1. The Lorentz comparator
using .5 is therefore undefined there and recorded as null rather than clipped
to manufacture a timing result. Group speed in a damped dispersive medium and
signal-front speed are distinct. The moving phase rate can reverse sign; it
cannot then be silently called a positive proper-time rate.

gamma is phenomenological memory damping here. Energy removed by it has no
retained receiving field in this reduced control. Compression, strain, reversible
work, circulation, weave and detector response are not implemented. No closed
superfluid energy budget, mass, bound-clock recurrence, Lorentz recovery or
shared redshift/timing law is established.

## Branch-step consequence

User goal: post and run the resistance/change interpretation.
Exact action: append an explicitly unverified operational interpretation to
E-533 and publish this propagation control, code and raw report on a task branch.
Protected: existing transport equations, node gates, static redshift proposal,
all existing solvers, PR #193 and dirty device checkouts.
Field: test motion, oscillation and decay from the actual recurrence.
Void: require separate packet/carrier/clock observables; prohibit inserted
Lorentz factors, invented difficulty coefficients or timing-derived mass.
Attempt: 1/3, all five numerical controls pass without retuning.
Decision: accepted propagation receipt; PARTIAL on the physical timing mechanism.
Do not scale this into clock, cosmological or detector claims.
Next permitted step: evolve a self-held time-periodic native excitation and
measure internal recurrence under translation and reversible field work, with
energy and perturbation controls. Derive the field-difficulty Xi from those
retained variables before interpreting its effect on timing. Preserve this
carrier/damping failure as a control for that next test.
