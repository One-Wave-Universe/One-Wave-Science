# Magnetic, Harmonic, Rabbit and Algorithm Zero integration — test bridge

**Status: TEST DEFINED / UNVERIFIED COUPLING.** This is a reference bridge, not a replacement for the canonical nodes, algorithms, or calibrated physics.

## Canonical dependencies

- [Chapter 09 magnetic prior art and point rotation](09_Transfluxor_Magnetic_Reorganization_and_Point_Rotation.md)
- [C-319 magnetic path reorganization](../Nodes/C-319_Magnetic_Lattice_Reorganization.md)
- [C-320 path-weighted compression](../Nodes/C-320_Magnetic_Compression_Path_Coupling.md)
- [C-325 independent magnetic triangulation](../Nodes/C-325_Transfluxor_Magnetic_Solver_Triangulation.md)
- [G-766 octave emergence](../Nodes/G-766_Discrete_Lattice_Dispersion_and_Octave_Emergence_Proof.md)
- [E-511 chord rotation](../Nodes/E-511_Chord_Rotation.md), and E-510/E-512 as the harmonic-clock and oscillation-window authorities
- [Rabbit Hopping translator hypothesis](../RABBIT_HOPPING_TRANSLATOR_HYPOTHESIS_QUESTIONS.md)
- Algorithm Zero's X/Y/Z/T branches and governed address/choice rules: resolve their current canonical files before implementing any transition. Do not infer the full algorithm from this bridge.
- [Research evidence graph](../RESEARCH_EVIDENCE_CONNECTION_GRAPH.md)

## Three different mathematical operations

**Octave scale**: frequency ratio \(f_2/f_1=2^n\), with signed log residual \(r_2=\log_2(f_2/f_1)-n\). G-766 already owns peak detection, tolerance and null comparisons. Scaling frequency does not by itself scale geometric size, field strength or lattice topology.

**Circle of fifths**: in twelve-tone equal temperament, the perfect fifth corresponds to a seven-semitone shift \(p\mapsto(p+7)\bmod12\). This is a pitch-class permutation, not a law of magnetic flux or spatial rotation. In measured acoustic ratios a pure fifth is 3:2, which differs from equal-tempered \(2^{7/12}\); preserve the tuning system. E-511's signed chord re-centering is a separate operator. If a 12-bin cyclic indexing scheme is used for experimental search, declare it as an addressing heuristic and compare to other permutations.

**Rabbit Hopping**: keep the source identity, signed rank, selected center and both wrapper choices \((N,T,T-1)\), \((N,T,T+1)\), together with branch, polarity, orientation, operation order and inverse-path metadata. Do not mistake this packet for Cartesian (x,y,z) or claim a physical path from arithmetic alone. Follow the complete translator hypothesis and its unresolved coordinate conventions.

## Proposed bridge to magnetic experiments

1. **Measure** multi-aperture flux, B-H, remanence, induced EMF, phase and frequency response under reproducible drive waveforms. Record raw time series, field maps and uncertainty. Keep waveform sampling separate from the clockless hardware architecture.
2. **Spectral analysis**: estimate complex transfer \(H(f)\), magnitude, phase, coherence, resonance peaks and nonlinear harmonic distortion for each aperture, winding polarity, material and drive history.
3. **Octave test**: detect peaks without supplying an octave ladder; calculate G-766 octave residuals; compare with phase-shuffled, frequency-shuffled and ordinary transformer/hysteresis controls.
4. **Fifths test**: separately test whether a fifths-based ordering improves prediction or retrieval of measured mode couplings over chronological, nearest-frequency, random cyclic and other modular permutations. The null is that indexing order has no privileged physical meaning.
5. **Rabbit route**: represent each experimental state and its source/wrapper lineage with reversible packets; test whether route reconstruction recovers source identity and prior measurement after branching and polarity reversal. Compare against ordinary graph-search indexing. A successful memory/address test does not prove a magnetic law.
6. **Algorithm Zero integration**: assign X/Y/Z/T addresses to verified measurements and hypothesis candidates only through canonical mapping; use FIELD to propose and VOID to independently challenge, with M4 evidence gate recording HOLD/PASS/FAIL. Preserve the exact data, not a generated replacement.
7. **Cross-scale coupling**: test whether a single fitted material model predicts frequency/phase/hysteresis changes across geometries and drive scales on holdout data. Only after ordinary Maxwell/material models have been exhausted should C-319/C-320 propose a *numerically distinct* residual with frozen parameters.
8. **Point rotation**: separate magnetic moment precession, flux-path rearrangement, geometric path turning, and measured mechanical angular momentum (G-749/G-769). A cyclic pitch index cannot stand in for physical torque.

## Falsification and validation

A model must predict observed quantities before the holdout experiment, with preregistered uncertainty, numerical convergence, and competing baselines. No tuned frequencies, winding constants, or geometry to make octave/fifths/Rabbit patterns appear. Reject any claimed octave emergence that also appears in null controls; reject any privileged fifths routing that performs no better than generic permutations; mark Algorithm Zero retrieval advantages unproven until independently benchmarked. The ordinary physics simulator remains independent of One-Wave.

## Receipt handoff

Every run should link: science node, exact claim/equation, Builds fixture and commit, raw data hash, solver parameters, measured spectra and uncertainties, octave residual, fifths baseline comparison, Rabbit route/inverse, Algorithm Zero address, VOID challenge and outcome. Fields without verified semantics stay explicitly NULL/UNMODELED.

**Reality is validation through consequence.**
