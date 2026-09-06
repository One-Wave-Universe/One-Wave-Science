---
id: G-745
title: Zone-Edge 125 GeV Lattice-Constant Hypothesis
status: yellow-hypothesis
tier: yellow
claim_boundary: unit conversion plus named assumptions; not a first-principles derivation of a_0; does not change C-322 or Mass Effect
---

# G-745 — Zone-Edge 125 GeV to a_0 (Yellow, not derived)

**Brick:** Yellow
**Does not override:** C-322, C-318, Updated 24/26, A-114, G-728 E1–E5 / F5
**Source of the claim:** conversational draft that asserted 125 GeV is a lattice-mode ceiling, group-velocity stagnation at the Brillouin zone edge plus condensate break defines a_0, and that a_0 is then a frozen input to a Hoyle / carbon solver.

## Canonical 125 GeV (unchanged)

C-322 keeps approximately 125 GeV as the measured Mirror-Gate boundary-response work to the first mirrored-basin crossing. That is an empirical anchor. It is not the lattice constant, and it is not Mass Effect by itself.

Mass Effect still requires all four interactions together. Propagation speed, zone-edge flattening, or group-velocity stall must not be rewritten as mass.

## The missing equation, written as assumptions

A draft said "the lattice constant resolves to" and then omitted the formula. The only equation that draft could have meant, in the high-frequency acoustic / first-zone-edge family, is the unit conversion

\[
a_0^{(\mathrm{edge})}
=
\frac{\pi\,\hbar\,c_{\mathrm{eff}}}{E_{125}}
\qquad\text{under assumptions A1–A4.}
\]

Gray control uses \(c_{\mathrm{eff}}=c\).

### Named assumptions (not outputs)

- **A1.** \(E_{125}\approx 125\,\mathrm{GeV}\) is identified with a zone-edge mode energy, not merely with Mirror-Gate work.
- **A2.** The edge is the first Brillouin boundary \(k_{\max}=\pi/a_0\) of a 1-D-like acoustic branch.
- **A3.** Group velocity vanishes there, \(dE/dk=0\), and that stall is the same event as a condensate yield / break.
- **A4.** An effective speed \(c_{\mathrm{eff}}\) exists and is already known from vacuum density and compressibility.

If any of A1–A4 is false, \(a_0^{(\mathrm{edge})}\) is not a physical lattice constant. Removing any one assumption must not be papered over by changing the words to "first principles."

## Gray-control number

Using \(\hbar c \approx 197.327\,\mathrm{MeV\,fm}\) and \(E_{125}=1.25\times 10^5\,\mathrm{MeV}\):

\[
\frac{\hbar c}{E_{125}}\approx 1.579\times 10^{-3}\,\mathrm{fm}
= 1.579\times 10^{-18}\,\mathrm{m}.
\]

Times \(\pi\):

\[
a_0^{(\mathrm{edge})}(c_{\mathrm{eff}}=c)\approx 4.96\times 10^{-18}\,\mathrm{m}.
\]

A nucleon / alpha spatial scale is order \(1\,\mathrm{fm}=10^{-15}\,\mathrm{m}\). The Gray-control edge length is about **three orders of magnitude smaller**. To force \(a_0\sim 1\,\mathrm{fm}\) one must take

\[
\frac{c_{\mathrm{eff}}}{c}\sim 2\times 10^{-3}.
\]

That ratio is an extra input. It is not derived in this node.

## Hoyle / carbon solver rule

Do **not** feed \(a_0^{(\mathrm{edge})}\) into a hyperradial / Jacobi carbon test as a non-negotiable constant and call the test blind.

A blind nuclear test may not inherit 125 GeV through a hidden \(c_{\mathrm{eff}}\). If a carbon script needs a length, declare it as a separate Gray nuclear scale or as an explicit Yellow parameter sweep. 7.654 MeV is not allowed to "confirm" an \(a_0\) that was already built from 125 GeV.

## What would promote this off Yellow

G-728 items still required before any Green language:

- E1 exact damped roots of A-114 without small-\(k\) cheat
- E3 numerical dispersion on a declared stencil
- E4 preferred-frame / Lorentz honesty for the damped Field equation
- E5 error bounds on any emergent invariant limit
- F5 absolute scale from the four-interaction work metric, not from this conversion

Condensate-break, phase inversion, and "soliton drop-out into alpha floors" remain story until those exist.

## Executable receipt

`One_Wave_Bench/logic_core/zone_edge_a0.py` and `test_zone_edge_a0.py` compute the conversion and refuse to label it derived.
