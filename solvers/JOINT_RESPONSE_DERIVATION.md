# Joint One-Wave response: executable replacement

Run from the repository root (Python 3, NumPy and SciPy):

```sh
python -m pip install numpy scipy
python solvers/test_joint_boundary_response.py
python solvers/run_joint_response.py > solvers/joint_response_results.json
```

This computes knot K, electrical shell E, Mirror M and weave T together. It replaces unsupported numerical shortcuts with a common operator, an energy ledger, a carried-profile curvature calculation and a complete fixed-window boundary response. It does not assign experimental particle masses to cavity modes.

## What has actually been solved

| Earlier numerical shortcut | Constructive replacement |
|---|---|
| Forced penetration or first crossing assigned 125 GeV | No exterior penetration bonds; coupling and phase response calculated from a passive four-port resolvent |
| Separate guessed mass formulas | Boundary-coordinate inertia from a Schur derivative and spatial carried-profile energy curvature from the same H and W |
| Square-root work calibration | Explicit linear work-unit scaling of fixed-coordinate inertia; dimensionless frequencies unchanged |
| Target-selected resonance | Every sample in the predetermined dimensionless interval 0.01–2 is published, with all eigenfrequency groups |
| Quark labels assigned to fitted inputs | Geometry and declared constitutive inputs produce unlabeled modes; no mass targets occur in the calculation |

The 13-site control gives maximum unitarity error 1.12e-14, lossless power-ledger error 1.34e-15, dissipative ledger error 3.89e-16 and relative energy drift below 9.38e-14 over 500 steps. Boundary inertia agrees with an independent Schur finite difference to relative error 1.22e-9. Removing both cross and phase coupling eliminates off-diagonal port response. Multiplying the common work unit by four multiplies boundary inertia by four and preserves the dimensionless spectrum and scattering.

## 1. Native geometry and joint constitutive candidate

Use D-409's twelve nearest neighbors a/sqrt(2) times (±1,±1,0), (±1,0,±1), (0,±1,±1). The selected finite FCC graph has no exterior bonds. FCC and HCP share this nearest shell; this implementation uses FCC stacking and does not establish longer-range HCP equivalence.

At each site q=(K,E,M,T). These are candidate response coordinates, not a derived microscopic identification of the actual four fields. Let L be the graph Laplacian and R the four-role cycle Laplacian. With cell volume ΔV=a³/sqrt(2), declare

\[
C=\operatorname{diag}(s_K,s_E,s_M,s_T)+cR,\quad
W=w\Delta V I,\quad
H=w\Delta V\left[\frac{L\otimes C}{12a^2}+I\otimes\kappa R\right].
\]

Default inputs are s=(1,0.8,1.2,0.6), c=0.12, κ=0.04, w=1 and port coupling g=0.25. These are explicit dimensionless control choices, not measured or uniquely derived constants. Positive spatial coefficients and nonnegative cross/phase coefficients make H positive semidefinite. The common uniform coordinate remains free; the relative-phase term is not a generic scalar mass gap.

## 2. Exact update and discrete work ledger

The central recurrence is

\[
W(q_{n+1}-2q_n+q_{n-1})/\Delta t^2+Hq_n=0.
\]

For v=(q_n-q_{n-1})/Δt and m=(q_n+q_{n-1})/2,

\[
E_{n-1/2}=\tfrac12 v^T(W-\Delta t^2H/4)v+\tfrac12 m^THm.
\]

Multiplying the recurrence by q[n+1]-q[n-1] proves equality of adjacent energies. Require Δt² λmax(W^-1/2 H W^-1/2)<4; the implementation rejects its endpoint and unstable steps. This is an exact discrete control, not a claim that any arbitrary update conserves continuum energy.

## 3. Coupling, phase response and reflection control

Select four interaction-coordinate ports at one boundary site, B=g sqrt(wΔV) times the selector. For the exp(-iωt) convention,

\[
D=H-\omega^2 W-i\omega(BB^T+\Gamma),\qquad
S=I+2i\omega B^TD^{-1}B.
\]

For incident amplitude a and q=D^-1 Ba,

\[
\|a\|^2-\|Sa\|^2=4\omega^2q^\dagger\Gamma q.
\]

Thus Γ=0 gives unitary coupling; Γ positive semidefinite accounts for loss. Phase and redistributed power come from the same operator. Missing exterior bonds give zero geometric graph flux. These four ports are abstract interaction channels: they do not yet supply an angular scattering distribution, tangential roll-off wave packets or a physical exterior radiation continuum. Those require exterior channel geometry and wave-packet evolution, while retaining the no-penetration rule.

At exact dark-mode frequencies the full resolvent can be singular despite an observable limit. The code rejects warnings, nonfinite solutions and excessive residuals explicitly. It never hides the singularity by adding damping. The fixed-window control has no rejected samples; exact eigenfrequencies have a separate test.

## 4. Boundary inertia without a separate guessed formula

Partition q into four selected boundary coordinates b and all remaining coordinates i. Verify Hii is positive definite, then

\[
T=\begin{bmatrix}I\\-H_{ii}^{-1}H_{ib}\end{bmatrix},\qquad
W_{\rm eff}=T^TWT.
\]

For the undamped mechanical Schur complement of H-zW,

\[
W_{\rm eff}=-\left.\frac{d}{dz}\operatorname{Schur}(H-zW)\right|_{z=0}.
\]

The finite-difference test independently evaluates the full Schur operator. This is inertia of boundary coordinates, not automatically center-of-mass translational inertia.

## 5. Carried-profile resistance and its independent energy check

For a specified profile Q, estimate its native three-dimensional derivatives G_j by nearest-neighbor least squares; reject rank-deficient geometry. Carrying the profile at velocity v changes its velocity by -Gv. The discrete metric Wd=W-Δt²H/4 gives the energy Hessian

\[
\mathcal M=\langle G^TW_dG\rangle_{\rm cycle}.
\]

For a W-normalized cavity eigenmode of eigenvalue λ, the exact discrete frequency is 2 asin(Δt sqrt(λ)/2)/Δt. Its midpoint amplitude supplies sqrt(1-Δt²λ/4), and the cycle average supplies 1/2. The test independently constructs carried pairs at 64 phases, evaluates their actual ledger energy and finite-differences velocity. It agrees with the tensor. Uniform internal phase modes can have nonzero frequencies and zero spatial carried response: a resonance alone is insufficient to establish Mass Effect.

Individual eigenvectors inside degenerate spaces are arbitrary. The report averages tensors over each complete degenerate group, yielding a projector-based invariant. W-normalized profile amplitude changes with w, so its tensor must not be interpreted as a physical work-scale calibration. A fixed actual profile and physical amplitude are needed for physical translational mass.

## 6. Refinement evidence and what must close next

At fixed radius 1.01, spacing 1, 1/2 and 1/3 gives 13, 55 and 177 sites. The first spatial frequency is respectively 0.459660896, 0.632761487 and 0.683984404. These changes are material. The decreasing difference is useful refinement evidence; three meshes do not prove continuum convergence or justify a precise particle prediction. Time-step refinement and positive-energy stability have separate tests.

The next physical closure must derive the constitutive coefficients, obtain a self-held three-vortex profile without imposed cavity walls, specify its amplitude and spatial/temporal units, and map observable scattering channels to independently measured spectra. A 125 GeV comparison must follow an independent energy/time calibration and identified resonance observable. Quark comparison also needs consistent renormalization conventions and independently derived flavor states. None of these may be replaced by tuning until a desired number appears.

## Reference, Field/Void review and verification record

Reference: main 0f005afb9afc8ac15a1ea061c2900cf3f6b0187c; D-409, A-115, C-317, C-318, C-322 and Book 1 Chapters 14–15. Choice: one additive joint response fixture plus replacement of contradictory gate-crossing/validated numerical passages in these paths; preserve legacy solvers and hardware.

Field produced the operator, update, scattering ledger and profile Hessian. Independent Void review allowed the candidate with a repaired singular-frequency guard and explicit restrictions on physical interpretation. Eleven tests cover geometry, conservation, stability, passive/unitary response, coupling ablation, Schur inertia, carried energy curvature, work scaling and singular frequencies. The report includes every fixed-window sample, unresolved samples and refinement outcomes. Status: candidate numerical response control solved and reproducible; physical spectrum closure remains open. A failure of conservation, passivity, anchoring or solve residual is a hard stop, not permission to recalibrate.
