# Musical Equipment Qualification for Virtual Breadboard

Musical equipment is now a permanent VBB qualification subject because it forces the simulator to handle several kinds of real circuit behavior at once: weak high-impedance sources, long cables, resonant inductive networks, nonlinear clipping, filters, magnetic parts, balanced reference paths, feedback, transient envelopes, and low-impedance loads.

The rule is the same as the rest of the breadboard work:

**reference/control first -> one change -> test -> compare -> name the drift -> only then add complexity.**

Passing a musical test means VBB reproduced the electrical behavior being checked. It does not mean a subjective tone claim was proven.

## Pack A — implemented first

`test/musical-equipment-qualification.test.js`

1. Passive guitar pickup: winding resistance + inductance + cable capacitance + 1 Mohm input.
2. Pickup/cable resonant peak and post-resonance rolloff.
3. Long/high-capacitance guitar cable versus normal cable.
4. 1 Mohm instrument input versus deliberately loading 100 kohm input.
5. Passive guitar tone network: low-frequency preservation versus treble dump.
6. Pedal input coupling capacitor: correctly sized versus intentionally undersized.
7. Symmetric anti-parallel silicon-diode clipping.
8. Asymmetric one-diode/two-diode clipping.
9. Speaker/voice-coil resistance + inductance: rising impedance with frequency.
10. First-order tweeter crossover.
11. Compressor/synth-style diode envelope follower: attack and release.
12. Pedal/amp RC supply-ripple filter.
13. Balanced differential audio line with equal source impedances.
14. Ideal common-mode hum rejection in the symmetric balanced-line control.

These are controls. They use established circuit behavior and should fail when VBB gets the physics or numerics wrong.

## Pack B — magnetic audio hardware

Build after Pack A is green.

- Guitar pickup turns ratio / mutual coupling controls using the toroid model.
- DI-box transformer: source loading, turns ratio, bandwidth, and saturation disclosure.
- Microphone transformer: low source impedance into reflected secondary load.
- Reverb-tank drive transformer and inductive transducer load.
- Dynamic microphone coil: source resistance + inductance + moving-coil electrical interface.
- Tape-head / magnetic-head small-signal inductive load.
- Speaker back-EMF control once a mechanical/electrical coupling model exists.

Do not fake mechanical cone motion or magnetic saturation if the corresponding model is not present. Mark those boundaries explicitly.

## Pack C — active pedals and amplifiers

Use the existing transistor and MOSFET models as controls before expanding device physics.

- BJT clean boost: bias point, gain, clipping onset, source/load dependence.
- Common-emitter distortion stage: DC bias plus AC gain plus transient clipping.
- MOSFET boost: gate loading, bias, gain, clipping, temperature/RDS(on) effects where applicable.
- Fuzz-style transistor pair when the available BJT model is sufficient to make a meaningful control.
- Source-follower / emitter-follower buffer: high input impedance and low output impedance.
- Tone stack after active gain stage.
- Power-rail sag control with finite battery/supply impedance.

Full commercial pedal emulation is not the target. Each circuit should isolate one physical behavior and have an independent expected result.

## Pack D — time-domain music signals

- 82 Hz, 110 Hz, 440 Hz, 1 kHz and multi-tone sources.
- Pick transient / pluck-like PWL waveform through pickup and cable network.
- Square-wave edge through guitar cable to expose ringing and numerical damping.
- Clipped sine harmonic-generation checks once FFT/spectral receipts are added.
- Tremolo control using time-varying gain once VBB has a suitable controlled element.
- Envelope follower attack/release sweeps.
- Power-supply ripple modulation control.

A waveform should never be accepted because it 'looks musical.' Every check needs a measurable voltage, current, frequency, phase, decay time, clipping threshold, or spectrum value.

## Pack E — balanced audio, reference and noise

This is especially useful for the One-Wave reference work because professional audio already depends on explicit reference management.

- Balanced source with matched source impedances.
- Intentional 1%, 5%, and 10% line imbalance and resulting common-mode leakage.
- Shield connected at both ends versus one end as topology experiments; do not treat simplified ground-loop models as bench proof.
- 60 Hz and 120 Hz common-mode interference.
- Differential receiver with finite CMRR once the receiver model exists.
- Phantom-power style symmetric feed as a reference/balance control, with current limits.
- Ground/reference lift faults and missing-reference diagnostics.

## Pack F — loads that punish weak simulators

- 16/32/80/250/600 ohm headphone loads.
- 4/8/16 ohm speaker loads with inductance.
- Long cable plus low-impedance load.
- Transformer plus rectifier plus RC load.
- Multiple pedals in series with realistic source/output impedances.
- Parallel pedal inputs and tuner loading.
- Hot-plug/open-circuit/shorted-output fault cases.
- Reverse polarity and accidental DC-on-audio-output fault cases.

The goal is to make VBB fail loudly on bad circuits rather than produce a pretty waveform.

## Pack G — ngspice parity targets

The existing ngspice gate already covers divider, sweep, RC AC/transient and diode controls. Musical equipment gives the next useful parity ladder:

1. Passive pickup R-L / cable-C / input-R frequency response.
2. Passive tone control sweep.
3. Symmetric diode clipper DC transfer curve.
4. Asymmetric clipper transfer curve.
5. Speaker R-L impedance sweep.
6. Crossover response.
7. Envelope detector transient.
8. BJT boost operating point and small-signal gain.
9. Balanced passive line network.
10. Transformer controls only when VBB and ngspice are using meaningfully comparable magnetic models.

Do not claim parity for VBB's simplified MOSFET/BJT/magnetic models against unrelated full SPICE models. Compare only where the model definitions are meaningfully aligned.

## Pack H — bench receipts

After simulation controls pass, use real musical parts as cheap physical standards:

- known resistor + capacitor tone filter;
- guitar cable capacitance measured with a meter if available;
- passive pickup DC resistance and frequency response;
- real distortion diodes;
- small speaker or headphone impedance trend;
- small transformer turns ratio;
- pedal supply RC filter;
- balanced cable continuity and symmetry.

Simulation PASS is not PHYSICAL PASS. Physical receipts remain separate.
