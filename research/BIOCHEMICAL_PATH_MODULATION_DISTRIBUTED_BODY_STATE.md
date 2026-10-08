# Chemical Path Modulation, Distributed Body State, and Biological Recurrence

**Status:** RESEARCH HYPOTHESIS / NOT EXPERIMENTALLY VERIFIED AS ONE-WAVE PHYSICS  
**Scope:** Biological mechanism, candidate equations, discriminating experiments, and downstream CELL_V1 design implications.  
**Source authority:** This file owns this *new* cross-domain hypothesis; established biology and other One-Wave claims retain their own authorities.  
**Related Science:** A-101 (Ground/Zero), A-102 (Displacement), A-104 (Gradient), A-105 (Restoring Response), A-115 (Unified Compression Field), C-319 (Magnetic Lattice Reorganization, analogy only), E-533 (Time-Transport, distinct physical hypothesis), chapters/02_Bio_Energetics_ATP.md, chapters/03_Affective_State_Mapping.md, V1_VERIFICATION_MATRIX.md.  
**Build application:** Builds repo CELL_V1; implementation must follow its own locked hardware/anti-drift rules.

## 1. Core research question
Can spatially localized chemical transport and receptor binding dynamically change electrical network excitability and *effective path accessibility*, yielding distributed sensorimotor coordination and oscillator synchronization beyond what fixed-connectivity models predict?

## 2. Mechanism to investigate
- Chemicals must physically arrive: vesicular release, extracellular diffusion, blood/interstitial circulation, or other transport depending on tissue and messenger.
- Binding at spatially distributed receptors modifies conductance, thresholds, channel kinetics, excitability, and sometimes functional connectivity.
- The resulting electrical activity propagates through neural/cellular networks; the original chemical does **not** generally travel from peripheral receptor to brain with each electrical impulse. Exceptions include long-range endocrine and other chemical signaling; chemical synapses genuinely transmit information locally.
- Local electrical/mechanical consequences feed back to chemical release, transport, uptake, receptor availability, and network state.
- Reuptake, vesicle recycling, calcium resequestration, degradation, and washout are distinct processes. **Reinjection** here is an *analogy for local recirculation/recovery*, not proof of electrical energy gain or a single universal biological loop.
- Biological variability, leakage, delay, receptor promiscuity, and redundancy are explicit model terms, not idealized away.
- Candidate distributed body-state map: locally coupled sensory/motor activity reflects load, stretch, position, balance, and action; this is **not** proof of a literal body-shaped electromagnetic field or replacement of known axonal and synaptic signaling.

## 3. Minimal candidate model (illustrative, not derived from One-Wave lattice)
For nodes i, receptor occupancy r_i, chemical concentration c_i, electrical potential V_i:

dc_i/dt = D_i ∇²c_i + s_i - u_i(c_i,r_i) - d_i(c_i) + transport_i

dr_i/dt = k_on,i c_i(1-r_i) - k_off,i r_i

C_i dV_i/dt = -I_ion,i(V_i,r_i) + Σ_j g_ij(r_i,r_j,V_i,V_j)(V_j-V_i) + I_ext,i

Here g_ij is **effective** electrical coupling/functional transmission, not necessarily a literal newly opened anatomical connection. The derivative with respect to t is an **external mathematical analysis coordinate**, not a commanded hardware clock. For clockless/event-driven implementations use threshold crossings and continuous physical coupling, not forced internal steps.

A candidate observable path-accessibility matrix is K_eff=[g_ij]; compare measured impulse-response transfer, propagation probability, latency, phase, and path recruitment before/after localized receptor perturbation.

Do not identify K_eff with C-319's magnetic lattice tensor K_L without a derived cross-domain mapping.

## 4. Internal timing and perceived time: separate layers
Biological circadian clocks are molecular feedback oscillators coupled by chemical/electrical interactions, entrained by light and other cues; sleep pressure is a separate interacting process. Subjective duration depends on attention, expectation, and memory, and can differ across people during equal external intervals. Neither observation establishes physical relativistic time dilation. E-533's transport-time mechanism remains a separate unverified cosmology hypothesis.

Test whether local receptor perturbation shifts oscillator phase, coupling, and period without assuming a master timed command. For human duration perception, test prospective vs retrospective reports separately.

## 5. Falsifiable experimental sequence
**E1 — local receptor/path modulation:** Compare a calibrated excitable-cell or neural-network model with (a) fixed coupling, (b) receptor-dependent conductance only, (c) receptor-dependent effective path transmission. Use localized pulses, matched total chemical dose, and sham control. Measure spatial voltage maps, phase response, activation routes, latency, energy consumption, and prediction error on held-out perturbations.

**E2 — distribution versus recovery:** Compare local release/reuptake, broader diffusion, uptake blockade, and degradation at matched receptor occupancy where feasible. Measure chemical concentration maps and electrical network responses. A 'more local recycling is always better' claim fails if it reduces coordination, clearance, or robustness.

**E3 — movement/body-state:** Use measured proprioceptive/motor data or established neuromuscular models. Compare the candidate distributed map with standard spinal-reflex, central-pattern-generator, and control models. Predict held-out movement/strain responses, not just a plausible animation.

**E4 — internal timing:** In a coupled-oscillator model, vary receptor state and quantify phase-locking, period, and robustness; compare against conventional circadian/neuronal oscillator baselines. Keep subjective duration experiments independent.

**E5 — physical One-Wave extension (only after E1–E4):** Derive a specific lattice-based prediction with fixed parameters that differs from accepted electrodiffusion/neurophysiology, then preregister a measurement. Without a discriminating prediction, the One-Wave interpretation remains an analogy.

For each experiment record control, parameter units, solver, input data provenance, predefined failure criterion, raw results, and reproducible receipt. Never label the full hypothesis proven because one subtest passes.

## 6. CELL_V1 implications (requirements, not implementation claims)
- Explore local sensor-induced threshold modulation, state-dependent path gating, retained hysteresis, and continuous feedback.
- Distinguish binary nucleus permission/confirmation from differential sensor/motor activity and the *separate* physical reinjection gate.
- Test distributed coupling and noise tolerance; no digital timing required in the proposed analog architecture.
- Measure real reinjected electrical energy, dissipation, and safe switching. Do not equate chemical recycling with power amplification.
- Compare with ordinary analog control and established motor systems. Do not tune a general simulator to validate One-Wave.
- Do not override CELL_V1 canonical geometry or introduce unsupported new windings/gates from biological analogy.

## 7. Candidate first paper
**Working title:** *Local Chemical Receptor Modulation as Dynamic Path Control in Distributed Excitable Networks: A Testable Cross-Scale Hypothesis*

**Abstract draft:** Chemical messengers can alter local receptor states, modifying conductance, excitability, and the effective propagation of electrical activity through coupled biological networks. We formulate a spatially resolved transport–binding–electrical model to test whether local chemical redistribution and recovery predict changes in collective waveform, pathway recruitment, and oscillator coordination beyond fixed-connectivity baselines. The proposed extension to distributed body-state control and One-Wave lattice mechanics is explicitly unverified. We specify matched controls, quantitative observables, and failure conditions for each level of interpretation.

**Paper sections:** biological prior art and alternatives; precise mechanism; transport/binding/network equations; measurable path-accessibility definition; controls and data; model comparisons; motor and timing tests; limitations; One-Wave-specific discriminating prediction; reproducibility and negative results.

**Publication gate:** Do not submit as a validated physical theory until original results, uncertainty estimates, comparisons to existing neuroscience, and a reproducible dataset/code receipt exist. A hypothesis/perspective paper can be drafted sooner if accurately labeled.

## 8. Open questions
- Which receptor families and tissues support meaningful effective path rerouting versus only gain modulation?
- When is chemical recirculation beneficial versus slower clearance or unwanted excitation?
- Can a compact local model reproduce distributed body-state responses without assuming a literal body-shaped field?
- What precise mathematical mapping, if any, links biological K_eff to One-Wave magnetic K_L?
- Which prediction would be impossible or substantially worse under standard electrodiffusion + neural network models?

**Evidence status:** Established biological components; new integrative mapping and One-Wave extension UNVERIFIED. This document proposes tests; it does not report experimental results.
