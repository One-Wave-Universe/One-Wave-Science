from pathlib import Path
p=Path('Virtual_Breadboard/SPICE_PARITY.md')
s=p.read_text()
old='14. Piecewise-linear and pulse sources for repeatable transient tests.'
new="14. **Piecewise-linear and pulse sources for repeatable transient tests** — IMPLEMENTED in the generic time-domain source path. `pwl` sources accept `[time, voltage]` breakpoints, linearly interpolate between points, and hold endpoint values outside the declared range. `pulse` sources implement SPICE-style V1/V2, delay, rise, width, fall, and optional repetition period, including ideal zero-time edges and one-shot behavior when no positive period is supplied. Both reuse the existing function-generator MNA branch and 1-ohm source impedance, so voltage droop and source current are solved rather than scripted. Permanent qualification checks exact waveform timing/interpolation plus a loaded-circuit Ohm's-law reference."
if old not in s: raise SystemExit('roadmap anchor missing')
p.write_text(s.replace(old,new,1))
