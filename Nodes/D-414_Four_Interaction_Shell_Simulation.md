---
node_id: "D-414"
canonical_name: "Four-Interaction Shell Simulation (Real Data as Wave Data)"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Reduced Simulation / Four-Interaction Visualization"
claim_gate_detail: "YELLOW (illustrative simulation of the C-318 coupled four-interaction state driven by real experimental data used as wave data; candidate geometry and couplings; does not derive gravity, charge, proton, or Mass Effect)"
metadata_standard: "I-06"
---

# Node D-414: Four-Interaction Shell Simulation

**Assets**
- `Nodes/D-414_Four_Interaction_Shell_Simulation/four_interaction_sim.html` — live interactive simulation
- `Nodes/D-414_Four_Interaction_Shell_Simulation/data/waves_bundle.json` — real datasets as wave data
- `Nodes/D-414_Four_Interaction_Shell_Simulation/graphs/*.png` — rendered data graphs (six_step_cycle, ligo_events, eeg_bands, reactor_isotopes, binding_curve, four_channels)
- `Wiki_Pages/D-414_Wiki_Page.html` — wiki page with embedded live sim + graphs

**Dependencies**
Upstream: C-318 Four-Interaction Mass-Effect Response, C-317 Boundary-Tension Weave, C-311 Electric-Magnetic Duality, C-301 Mirror Gate, C-322 (125 GeV anchor), A-115 Unified Compression Field
Downstream: One_Wave_Bench experiment ledger

## Purpose

D-414 renders the **four interactions** of the C-318 coupled state — **not** the four fundamental forces, but the four channels of **one** bounded wave — and drives each channel with a **real experimental dataset used as wave data** (the actual time series or spectrum fed in as the channel's wave function, not merely a headline constant).

The four interactions:

1. **Z_K — Three-Vortex Knot:** internal braided geometry (the proton drawn as three interwoven strands).
2. **Z_E — Electrical Shell:** pressure/voltage shell and its push-back against compression.
3. **Z_M — Mirror Gate:** compression↔expression reversal boundary (C-301 / C-322, 125 GeV anchor).
4. **Z_T — Boundary-Tension Weave:** surface + volume confinement / gluon-like surface tension (C-317).

## The Six-Step Master Cycle (B-221) — how every dataset is folded

Every real dataset is folded onto the repo's canonical six-step cycle, exactly as it already lives in the repo (`Nodes/B-221_Six_Recursive_Steps.md`):

**BEGIN → MOVE → HOLD → BUILD → BREAK → LOOP**

The fold is:
- **Nested / recursive (B-220):** the same six steps repeat inside every step, five scale layers deep — Micro ⊂ Small ⊂ Medium ⊂ Large ⊂ Macro.
- **Everything doubles + bidirectional (B-224, C-301):** the forward pass is doubled by a mirror-reversed pass; each dataset yields a 48-point bidirectional envelope, forward then mirrored through the center. Mirror M² = −I, M⁴ = I (4π closure).
- **Oscillating at the middle (B-222):** HOLD resolves back toward BEGIN through the oscillation center (A-108); every transition is Compression ← Center → Expression.

Each dataset in `waves_bundle.json` therefore carries a `fold` object: `center_pivot`, `amplitude`, the six `steps{BEGIN..LOOP}` with per-step level/energy, `hold_returns_to_begin_residual`, `break_crossing`, the `bidirectional_envelope`, `nested_scales`, and a `nested_energy_tree` (6 branches at each of 5 levels). The simulation animates the bidirectional envelope; the graphs render the folded steps.

## Real Data as Wave Data (expanded)

| Channel | Real datasets (each used as wave, folded on the six-step cycle) | Source |
|---|---|---|
| Z_M Mirror Gate | **7 LIGO/Virgo events**, 32 s @ 4096 Hz each — GW150914 (BBH, break-crossing), GW151226 (Boxing Day BBH), GW170817 (binary neutron-star, ~2.74 M☉), GW190425 (2nd BNS), GW190521 (massive BH, ~142 M☉), GW190814 (most asymmetric masses, 2.6 M☉ mass-gap secondary), GW200105 (first confident neutron-star–black-hole); **125.11 GeV Higgs** = mirror-gate boundary scale | GWOSC / LIGO-Virgo; ATLAS/CMS |
| Z_E Electric Shell | **8 real EEG records** across 5 subjects (PhysioNet eegmmidb, 160 Hz) — S001R01 eyes-open, S001R02 eyes-closed (real Berger alpha-blocking, highest alpha 0.178), S001R03 motor task, S001R04 motor imagery, S002R01/S003R01/S004R01/S005R01 additional subjects; **antimatter** = same shell with inverted voltage differential (CERN ALPHA 1S–2S) | PhysioNet / CERN ALPHA |
| Z_T Boundary-Tension Weave | **5 reactor isotopes** — point-kinetics neutron-flux transients from measured Keepin six-group delayed-neutron data: U-235 thermal (β=0.0067), Pu-239 thermal (β=0.0022), U-238 fast (β=0.0164), U-233 thermal (β=0.0026), Th-232 fast (β=0.0291, largest); plus the **nuclear binding-energy curve** (peak Ni-62/Fe-56 ~8.79 MeV) | Keepin / NEA / IAEA; Wikipedia binding curve |
| Z_K Three-Vortex Knot | **Full CODATA-2022 anchor set** — proton 938.272 MeV / 0.8409 fm (uud = three braids), neutron 939.565 MeV, electron 0.511 MeV, the complete three-generation quark ladder (up 2.16, down 4.70, strange 93.5, charm 1273, bottom 4183, top 172570 MeV), lepton ladder (muon 105.7, tau 1776.9 MeV), deuteron & alpha-particle masses, radii, g-factors, fine-structure constant; braided phase is candidate geometry | NIST CODATA 2022 / PDG 2024 |

## What the Simulation Shows

- **Proton braids / knot (Z_K):** three interwoven strands with adjustable crossing number — the Three-Vortex geometry drawn explicitly.
- **Toroidal flow (Z_T):** particles circulating around a torus, flow rate modulated by real reactor kinetics — the surface + volume confinement of C-317.
- **Electric shell + push-back (Z_E):** a pulsing shell that displaces inward and pushes back when EEG-driven data compresses it.
- **Mirror-Gate boundary (Z_M):** a crossing ring that flashes when the LIGO strain amplitude passes threshold.
- **Cross-coupling E_×:** live energy panel tracks E_K, E_E, E_M, E_T and the load-bearing cross term, per C-318.
- **Data-drive selector:** choose any single real dataset (each LIGO event, each EEG record, each reactor isotope, the binding curve, or antimatter) or the blended “all real data” mode; the selected dataset's six-step bidirectional envelope drives the live simulation.
- **Scale (micro→macro):** from a single proton-scale knot out to many shells whose retained wake is the Extended-Compression / dark-matter view. Camera/scale never changes the physics.

## Discipline & Honest Limits (D-412)

D-414 is a **YELLOW reduced model**. It separates state from measurement from visualization, declares its native dimension (a bounded field of coupled channels), and its runs can fail. The real datasets **drive** the channels as inputs; the geometry and coupling coefficients are **candidate**, not derived.

D-414 does **not** claim to prove gravity, charge, the proton, or Mass Effect, and does **not** reinterpret the source experiments — LIGO remains gravitational waves, EEG remains cortical voltage, reactor data remains neutron kinetics. They are used strictly as wave inputs to an illustrative one-wave analogy.

## Sources

- LIGO/GWOSC event portal (GW150914, GW170817, GW190521): https://gwosc.org/eventapi/
- PhysioNet EEG Motor Movement/Imagery Database: https://physionet.org/content/eegmmidb/1.0.0/
- Keepin six-group delayed-neutron data (U-235 / Pu-239 / U-238; standard nuclear tables, NEA/IAEA): https://www.sciencedirect.com/topics/engineering/delayed-neutron
- Nuclear binding-energy curve: https://en.wikipedia.org/wiki/Nuclear_binding_energy
- NIST CODATA 2022 constants: https://physics.nist.gov/cuu/Constants/
- Higgs 125.11 GeV: https://atlas.cern and https://cms-results.web.cern.ch
- Six-step cycle & nesting: `Nodes/B-221_Six_Recursive_Steps.md`, `B-220_Scale_Layer`, `B-222_Oscillation_Center`, `B-224_Two_Choices`, `C-301_Mirror`
