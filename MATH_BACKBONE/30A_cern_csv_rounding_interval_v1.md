# MATH BACKBONE 30A — CERN CSV ROUNDING INTERVAL v1

Status: **GREEN AS REPRESENTATION-ERROR CHECK / NOT DETECTOR UNCERTAINTY**

Depends on: `30_cern_fourvector_to_wave_transform_v1.md`

CORE-RULES-PRE:
- The first live CERN transform produced a maximum center-value pair-mass difference of 0.0170164498 GeV while the source four-vector columns were printed to finite decimal precision.
- Do not widen a tolerance merely to make the test pass.
- Derive the comparison interval from the displayed numerical precision instead.

## 1. Why a fixed 10 MeV tolerance was rejected

Suppose the source CSV prints a component as

\[
x_0=9.6987.
\]

If the final printed digit is the rounded representation, the represented value lies within

\[
 x \in [x_0-0.00005,\;x_0+0.00005].
\]

The half-width is therefore determined by the displayed decimal quantum, not selected after looking at the invariant-mass error.

This is a **representation rounding interval**. It is not a statement about CMS detector resolution or experimental systematic uncertainty.

## 2. Component intervals

For each printed four-vector component \(x\), define its half-resolution \(\delta x\) as one half of the least displayed decimal unit.

For a pair of objects,

\[
E=E_1+E_2,
\quad
p_x=p_{x1}+p_{x2},
\quad
p_y=p_{y1}+p_{y2},
\quad
p_z=p_{z1}+p_{z2}.
\]

The conservative summed half-widths are

\[
\delta E=\delta E_1+\delta E_2,
\]

and likewise for each momentum component.

## 3. Squared interval

For a scalar interval

\[
x\in[x_0-\delta x,\;x_0+\delta x],
\]

define

\[
S_{max}(x)=\max[(x_0-\delta x)^2,(x_0+\delta x)^2].
\]

If the interval crosses zero,

\[
S_{min}(x)=0.
\]

Otherwise

\[
S_{min}(x)=\min[(x_0-\delta x)^2,(x_0+\delta x)^2].
\]

## 4. Conservative invariant-mass interval

The invariant relation is

\[
M^2=E^2-p_x^2-p_y^2-p_z^2.
\]

A conservative lower bound is

\[
M^2_{min}=S_{min}(E)-S_{max}(p_x)-S_{max}(p_y)-S_{max}(p_z),
\]

and an upper bound is

\[
M^2_{max}=S_{max}(E)-S_{min}(p_x)-S_{min}(p_y)-S_{min}(p_z).
\]

Therefore

\[
\boxed{M_{min}=\sqrt{\max(M^2_{min},0)}}
\]

and

\[
\boxed{M_{max}=\sqrt{\max(M^2_{max},0)}}.
\]

The printed source `M` value gets its own interval from its displayed precision:

\[
M_{src}\in[M_0-\delta M,\;M_0+\delta M].
\]

## 5. Pass/fail rule

Define the gap between the two intervals:

\[
g=0
\]

when the reconstructed rounding interval and the source-mass rounding interval overlap.

Otherwise \(g\) is the positive distance between the nearest interval endpoints.

The representation-consistency test is

\[
\boxed{g=0\;\Rightarrow\;\text{PASS WITHIN DISPLAYED ROUNDING}}
\]

and

\[
\boxed{g>0\;\Rightarrow\;\text{INVESTIGATE}}
\]

No arbitrary MeV tolerance is inserted.

## 6. First-run receipt

Before this rule was added, 5,000 CMS dimuon events / 10,000 muon objects were transformed successfully.

Observed center-value diagnostics from that run:

- objects transformed: 10,000;
- maximum absolute source-vs-recomputed pair-mass center difference: 0.017016449838837655 GeV;
- individual four-vectors with negative \(E^2-p^2\) after printed-value rounding: 52;
- beta-above-one warnings beyond the declared tolerance: 0;
- standard-derived frequency range: approximately \(6.69\times10^{23}\) to \(1.02\times10^{26}\) Hz;
- de Broglie wavelength range: approximately \(2.95\times10^{-18}\) to \(4.48\times10^{-16}\) m.

The 17 MeV center difference is preserved as an audit receipt. It is not deleted after introducing the more appropriate precision-derived interval test.

## 7. Kill condition

This rounding model is rejected for a record if the source documentation states that the printed decimal places do not represent ordinary rounding/quantization of the supplied four-vector values, or if \(g>0\) persists systematically.

CORE-RULES-POST:
- Failed fixed-tolerance test preserved.
- No tolerance was reverse-fit.
- New test is derived from source representation precision.
- Detector/systematic uncertainty is explicitly kept separate from CSV display precision.
- Drift detected: no.
