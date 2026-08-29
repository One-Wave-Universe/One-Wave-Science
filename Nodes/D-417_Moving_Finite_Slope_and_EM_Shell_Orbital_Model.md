---
node_id: "D-417"
canonical_name: "Moving Finite-Slope and EM-Shell Orbital Model"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "SUPERSEDED"
classification: "Resonance, Modal & Dimensional Structure / Planetary-Scale Displacement Lineage"
claim_gate_detail: "YELLOW (locked test architecture; finite-range boundary law and EM-to-shell coupling law not yet derived). Superseded by D-418/D-419's recursive Point-Path-Field completion; retained as the architecture that removed wake memory from D-416."
metadata_standard: "I-06"
---

# Node D-417: Moving Finite-Slope and EM-Shell Orbital Model

## Dependencies

Upstream: D-416, A-104, A-105, A-106, B-216, C-310, C-311, C-317, D-401,
D-413.

Superseded by: D-418, D-419.

Authority and full engineering contract:
`UPDATED_39_MOVING_FINITE_SLOPE_AND_EM_SHELL_ORBITAL_MODEL.md`.

## Definition

D-417 replaces D-416's stored-wake/assimilation memory with an
instantaneous moving network of body-specific finite displacement/slope
regions. Every body moves; every body's active range moves with it and
is recomputed at every timestep from that body's own potential/slope
against the current surrounding reference. No stored wake memory, relay
memory, or universal cutoff radius is assumed.

## Locked rules

1. Every body has its own moving potential/slope profile `Phi_i(r,t)`,
   `S_i(r,t) = |grad Phi_i(r,t)|`.
2. Its active domain `Omega_i(t) = { r : DeltaS_i(r,t) distinguishable
   from S_ref }`, `DeltaS_i = S_i - S_ref`, is an emergent boundary
   `R_i(t)`, not a hand-set AU radius.
3. All active regions recompute every timestep as bodies move; a planet
   speeds or slows because the instantaneous combined slope geometry
   around it changes.
4. Local slope driving body `i`: `S_local,i(t) = SUM_j I(r_i in
   Omega_j(t)) S_j(r_i,t)`; driver `DeltaS_i = S_local,i - S_ref,i`;
   response `a_i(t) = -F(DeltaS_i(t), K_i_eff(t))`.

## EM-shell role

EM is not a direct gravity-like force. It modifies the stability/
stiffness/response of a body's local displacement shell:

`K_i_eff(t) = K_i0 * [1 + eta * C_i(t)]`,
`C_i(t) = G(B_sun(r_i,t), B_i(t), alignment_i(t), shell_geometry_i(t))`.

Mercury gets an extra Sun-Mercury channel, `K_Me_eff = K_Me0 * [1 +
eta*C_Me + eta_SM*C_SM]`, because its intrinsic field sits deep in the
Sun's magnetic environment; its 3:2 spin-orbit resonance stays a
gravitational/tidal control fact. Earth carries `C_E`. Mars and Venus
are global-intrinsic-dipole controls (`C_Mars_global = C_Venus_intrinsic
= 0` on the first pass). Jupiter, Saturn, Uranus, and Neptune carry
nonzero shell state and are the falsification test against "large
magnetic moment implies large orbital correction."

## Falsification requirements

Reject if a single arbitrary cutoff serves all planets, if body ranges
must be tuned independently to force a match, if an EM coefficient needs
independent per-planet tuning, if Jupiter's field produces an unobserved
orbital correction, if Mars/Venus need a fictitious global shell, if
Mercury's coupling is defined only after inspecting its residual, or if
removing absolute coordinates just rewrites ordinary N-body dynamics.

## Disposition

The moving finite-slope/EM-shell separation (`ORBIT = moving finite
slope geometry`, `EM = shell-integrity modifier`) carries forward
unchanged into D-418/D-419. It was extended, not discarded: D-418 places
this slope/shell state inside a recursive Point-Path-Field structure with
explicit internal rotation, and D-419 folds the result into one planetary
displacement state alongside spin, tides, and stability.
