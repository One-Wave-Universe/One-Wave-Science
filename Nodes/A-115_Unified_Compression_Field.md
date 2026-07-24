---
node_id: "A-115"
canonical_name: "Unified Compression Field"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Foundation Extension / Load-Bearing Cross-Scale Node"
claim_gate_detail: "YELLOW (field decomposition and static-loop equations) / GREEN (physical identity claims and coefficients)"
metadata_standard: "I-06"
---

# Node A-115: Unified Compression Field

**Dependencies**
Upstream: A-101 Ground / Zero, A-102 Displacement, A-104 Gradient, A-105 Restoring Response, A-106 Pressure Response, A-109 Inertial Memory, A-112 Persistent Mode, A-116 Three-Dimensional Spherical Default, C-309 Friction Limit
Downstream: Book 1 Ch12 Gravity, Book 1 Ch14 Mass Effect, Book 1 Ch15 Higgs, Book 5 Ch1 Galaxies and Dark Matter, C-301 Mirror Gate, C-322 Mirror-Gate 125 GeV Boundary Response, E-528 Static Redshift Transport, E-529 Low-Coupling Return Mode, E-530 White Energy Recirculation, Book 5 Ch4 Black Holes and Quasars

## Purpose

This node gives one load-bearing home to a central One-Wave claim:

> Gravity, dark-matter behavior, local Mass Effect, and the Mirror-Gate boundary response are measurement views of one displaced, compressed, restoring field.

The same field has an outward return channel called **White Energy**. White Energy means quasar/white-hole-scale ejection and reinjection. It does not mean expansion of space.

## 1. Field Variables

Let

\[
\mathbf u(\mathbf x,t)
\]

be displacement of the One-Wave field away from Ground / Zero. Define scalar compression

\[
\chi(\mathbf x,t)=-\nabla\cdot\mathbf u.
\]

- \(\chi>0\): compression,
- \(\chi<0\): expression/release,
- \(\chi=0\): no local volumetric displacement.

Use the minimal energy density

\[
\mathcal E_{\rm OW}
=
\frac{\rho_u}{2}|\partial_t\mathbf u|^2
+
\frac{K_\chi}{2}\chi^2
+
\frac{S_u}{2}|\nabla\mathbf u|^2
+
V_b(\mathbf u).
\]

A damped sourced field equation is

\[
\rho_u\partial_t^2\mathbf u
+
\mu_u\partial_t\mathbf u
-
K_\chi\nabla(\nabla\cdot\mathbf u)
-
S_u\nabla^2\mathbf u
+
\frac{\partial V_b}{\partial\mathbf u}
=
\mathbf J_{\rm source}.
\]

The coefficients remain uncalibrated.

## 2. Gravity / Compression-Gradient View

Define

\[
\Phi_{\rm OW}=\alpha_g\chi,
\qquad
\mathbf g_{\rm OW}=-\nabla\Phi_{\rm OW}=-\alpha_g\nabla\chi.
\]

The Newtonian exterior limit is recovered only if the derived source solution gives

\[
\Phi_{\rm OW}(r)\rightarrow-\frac{G M_{\rm eff}}{r},
\qquad
|\mathbf g_{\rm OW}(r)|\rightarrow\frac{G M_{\rm eff}}{r^2}.
\]

Here \(M_{\rm eff}\) is the measured **Mass Effect** assigned to the bounded source, not an independently defined substance.

## 3. Extended Compression / Dark-Matter View

For bookkeeping,

\[
\mathbf g_{\rm OW}=\mathbf g_{\rm local}+\mathbf g_{\rm wake}.
\]

This does not introduce a second substance. It separates near-source response from retained or wake-like compression.

For circular motion,

\[
\frac{v_c^2(r)}{r}=|\mathbf g_{\rm local}(r)+\mathbf g_{\rm wake}(r)|.
\]

A conventional analysis would infer

\[
\rho_{\rm DM,eff}
=-\frac{1}{4\pi G_{\rm eff}}\nabla\cdot\mathbf g_{\rm wake}.
\]

In One-Wave this is the **Extended Compression Effect**, not unseen particulate matter.

## 4. Local Mass Effect and Mirror-Gate Boundary View

The local bounded state is not reduced to a single scalar coordinate. C-318 groups the accepted architecture into one coupled four-interaction state

\[
\mathbf Z=(\mathbf Z_K,\mathbf Z_E,\mathbf Z_M,\mathbf Z_T),
\]

representing the internal knot, electrical shell, Mirror relation, and Boundary-Tension Weave.

Its cycle-averaged energy is

\[
\overline E_4
=
\left\langle E_K+E_E+E_M+E_T+E_\times\right\rangle_{\rm cycle}.
\]

The cross-interaction term is required because the four interactions stabilize one bounded recurrence together.

Two different measurements come from this same architecture.

### Local carried-pattern response

For center velocity \(\mathbf v\), C-318 defines

\[
\mathcal M_{ij}
=
\left.
\frac{\partial^2\overline E_4}
{\partial v_i\partial v_j}
\right|_{\mathbf v=0}.
\]

For an isotropic lowest mode,

\[
m_{\rm eff}=\frac13\operatorname{Tr}\mathcal M.
\]

C-318 reduces this to the discrete carried-profile form

\[
\mathcal M_{jk}
=
\sum_i\Delta V\,
(D_j\mathbf Z_{0,i})^{\mathsf T}\mathsf W_i(D_k\mathbf Z_{0,i}),
\]

where \(\mathsf W_i\) is the still-unclosed work metric that converts A-109 memory and the four interaction responses into physical energy.

This is the Mass Effect: the resistance produced when the entire coupled recurrence must be carried and rebuilt relative to Ground.

### Finite Mirror-Gate response

For an allowed boundary-deformation path from stable hold \(\mathbf q_0\) to the first Mirror threshold \(\mathbf q_G\), C-322 defines

\[
E_{\rm MG}
=
\overline E_4(\mathbf q_G)-\overline E_4(\mathbf q_0)
=
\int_{\Gamma_{0\to G}}
\nabla_{\mathbf q}\overline E_4\cdot d\mathbf q.
\]

The empirical anchor is

\[
E_{\rm MG}\approx125\ {\rm GeV}.
\]

The Mass Effect and the Mirror-Gate energy are therefore related through the same four-interaction field architecture but are not interchangeable:

\[
m_{\rm eff}\neq E_{\rm MG}/c^2
\]

as a causal derivation.

## 5. Static Cosmic Energy Accounting

One-Wave uses no scale factor and no expansion of space. Redshift is handled by E-528 as propagation-energy transfer through a static background.

Let \(u_\gamma,u_\chi,u_\nu,u_C,u_W\) be energy densities in propagating light, the compression field, Low-Coupling Return Modes, compact compressed reservoirs, and outward White Energy. A minimal local accounting chain is

\[
\partial_tu_\gamma+\nabla\cdot\mathbf J_\gamma=-Q_{\gamma\to\chi},
\]

\[
\partial_tu_\chi+\nabla\cdot\mathbf J_\chi
=Q_{\gamma\to\chi}+Q_{W\to\chi}-Q_{\chi\to\nu}-Q_{\rm capture},
\]

\[
\partial_tu_\nu+\nabla\cdot\mathbf J_\nu
=Q_{\chi\to\nu}-Q_{\nu\to C},
\]

\[
\partial_tu_C+\nabla\cdot\mathbf J_C
=Q_{\rm capture}+Q_{\nu\to C}-Q_{C\to W},
\]

\[
\partial_tu_W+\nabla\cdot\mathbf J_W
=Q_{C\to W}-Q_{W\to\chi}.
\]

The White Energy channel is therefore an explicit carrier of released energy, not a source term that appears and disappears between equations.

For a closed static One-Wave domain,

\[
\frac{d}{dt}\int_\Omega
(u_\gamma+u_\chi+u_\nu+u_C+u_W)\,dV
=
-\oint_{\partial\Omega}
(\mathbf J_\gamma+\mathbf J_\chi+\mathbf J_\nu+\mathbf J_C+\mathbf J_W)\cdot d\mathbf A.
\]

For a closed boundary the right-hand side is zero. A stationary circulation additionally requires the long-time transfer equalities

\[
\langle Q_{\chi\to\nu}\rangle=\langle Q_{\nu\to C}\rangle,
\qquad
\langle Q_{C\to W}\rangle=\langle Q_{W\to\chi}\rangle,
\]

with the field-storage balance

\[
\langle Q_{\gamma\to\chi}+Q_{W\to\chi}\rangle
=
\langle Q_{\chi\to\nu}+Q_{\rm capture}\rangle.
\]

This is circulation and replacement, not expansion.

## 6. Unified Loop

```text
Mass Effect / displacement
-> gravity-compression gradient
-> light propagation loss and redshift
-> field transfer
-> low-coupling neutrino return
-> compact compression reservoir
-> Mirror-Gate threshold
-> White Energy ejection
-> field reinjection
-> new Mass Effect / structure
```

## 7. Promotion Requirements

### Yellow completion

- derive \(\chi(r)\) from sources,
- recover or replace the inverse-square limit,
- derive the extended wake profile without fitting it by hand,
- derive the four-interaction work metric, the actual gate-crossing path, the scale-free gate-to-mass ratio, and one explicit energy calibration route,
- derive the E-528 propagation coefficient from field variables,
- derive the E-529 neutrino-transfer coefficients,
- close the E-530 static energy budget.

### Bronze

- one fixed field law reproduces chosen gravity/rotation/lensing datasets,
- one four-interaction boundary model produces a pressure-work threshold near 125 GeV,
- a static transport simulation conserves total energy through photon loss, neutrino return, capture, and White Energy ejection,
- code, parameters, raw outputs, and failed regimes are published.

## Direct Failure Conditions

This version fails if one coefficient set cannot connect the claimed views, if redshift requires hidden expansion terms, if the energy lost by light cannot be accounted for, if the neutrino return channel has no derivable coupling, or if White Energy ejection creates energy rather than returning stored compression.

## Status Statement

A-115 is load-bearing because it states the identity and accounting rules being tested. It does not claim established experimental proof.
