/*
 * Circuit engine: solves real circuit physics on whatever the user has wired up.
 *
 * Method: Modified Nodal Analysis (MNA) — the same linear-algebra technique
 * real SPICE-class simulators use for the resistive/DC part of a circuit.
 *   - Kirchhoff's Current Law is enforced at every node (sum of currents = 0).
 *   - Ohm's Law (I = V/R) stamps resistors as conductances.
 *   - Ideal voltage sources (batteries) get an extra unknown (branch current).
 *   - LEDs use an iterative ideal-diode-with-threshold model (on/off fixed
 *     point iteration): below Vf they are an open circuit, above Vf they are
 *     a small series resistance plus the forward-voltage drop — the standard
 *     "constant voltage drop" large-signal diode model used in hand circuit
 *     analysis.
 *   - Capacitors use a backward-Euler companion model (conductance C/dt in
 *     parallel with a current source), which reproduces real RC charge/
 *     discharge curves frame to frame.
 *   - Inductors use the dual backward-Euler companion model (an extra
 *     branch-current unknown, same technique as an ideal voltage source),
 *     reproducing real L/R current-rise transients frame to frame.
 *   - AC sources are ideal voltage sources whose value is evaluated at the
 *     simulator's own running clock (accumulated real dt, same clock every
 *     frame draws from) instead of a fixed constant — genuine time-domain
 *     AC, not a single-frequency phasor snapshot.
 *   - The MTJ angle sensor models the electrical interface of a real
 *     magnetic-tunnel-junction angle-sensor IC (e.g. AS5047P/TLE5012-class
 *     parts): two buffered analog outputs, sin(theta) and cos(theta) of a
 *     rotating field, referenced to a shared pin — implemented as a
 *     quadrature pair of ideal sources sharing one clock, 90 degrees apart.
 *   - Ferrite toroids generalize the single inductor to N windings sharing
 *     one magnetic core: real mutual inductance (SPICE-style coupling),
 *     each winding a backward-Euler branch whose equation now also carries
 *     every other winding's discretized current, plus real per-winding DC
 *     winding resistance from wire gauge and core size.
 *   - Discrete MOSFETs conduct drain-source only past a real Vgs threshold
 *     (fixed RDS(on) once on), and their body diode is a genuinely separate
 *     always-live one-way path -- independent on/off fixed-point state, same
 *     technique as the diode/LED model.
 *   - Square-loop memory cores generalize the toroid to a NONLINEAR core: one
 *     shared flux state B (normalized to +/-1) instead of a linear L, with a
 *     real ampere-turns coercive threshold (Hc). Below Hc, B is frozen (real
 *     remanence -- current can wiggle without erasing it); above Hc, B
 *     relaxes toward +/-1 on a real (short but nonzero) switching time
 *     constant via the same backward-Euler technique as a capacitor/inductor,
 *     so a flip produces a genuine multi-frame induced-voltage spike on any
 *     other winding sharing the core (Faraday's law: V = N*dPhi/dt), not an
 *     instant step. Whether a given drive actually flips it, and what any
 *     other winding on the same core reads, is computed by the solver from
 *     real current and never pre-decided.
 *   - The TLV3202 dual comparator is two independent push-pull output
 *     stages sharing one VCC/GND pair: each output is modeled as a small
 *     output-impedance resistor path to whichever rail the real Vin+/Vin-
 *     comparison (offset by a real input offset voltage) currently
 *     decides -- exactly the same on/off fixed-point technique as a
 *     MOSFET's channel decision, just choosing between two conduction
 *     paths (to VCC or to GND) instead of one path being on/off. No
 *     ternary/multi-level decision is hard-coded here: this is a plain
 *     2-level comparator, honestly modeled: whatever multi-level behavior
 *     gets built from it has to come from real wiring around it.
 *   - A tiny leak conductance (gmin) from every node to ground prevents the
 *     matrix from going singular when part of the board isn't wired to
 *     anything yet.
 */
(function (root) {
  'use strict';

  class UnionFind {
    constructor() {
      this.parent = new Map();
    }
    find(x) {
      if (!this.parent.has(x)) this.parent.set(x, x);
      let p = this.parent.get(x);
      if (p === x) return x;
      const r = this.find(p);
      this.parent.set(x, r);
      return r;
    }
    union(a, b) {
      const ra = this.find(a);
      const rb = this.find(b);
      if (ra !== rb) this.parent.set(ra, rb);
    }
  }

  const LED_VF = { red: 1.8, yellow: 2.0, green: 2.1, blue: 3.0, white: 3.0, ir: 1.4 };
  const LED_RON = 12; // ohms, approximate forward dynamic resistance
  const DIODE_VF = 0.7; // volts, generic silicon rectifier (e.g. 1N4001-class)
  const DIODE_RON = 5; // ohms, approximate forward dynamic resistance
  const GMIN = 1e-9;
  const BATTERY_RINT = 1; // ohms, internal resistance of a small supply/battery
  // ohms; a purpose-built low-voltage/precision reference source (a DAC
  // output stage, a precision resistor divider, a low-voltage reference
  // IC) has real output impedance too, but it is NOT the same real part as
  // a battery -- typically a couple hundred ohms rather than a battery's
  // ~1 ohm. Honest order-of-magnitude default; a real design's actual
  // source impedance is set via the diffsource's own optional sourceR.
  const DIFFSOURCE_RINT = 200;

  // deterministic PRNG (mulberry32) + Box-Muller Gaussian sampling, used
  // for real source noise (diffsource's optional noiseRms) -- seeded per
  // component id so a run is reproducible, not re-randomized every call.
  function mulberry32(seed) {
    let s = seed >>> 0;
    return function () {
      s = (s + 0x6d2b79f5) | 0;
      let t = Math.imul(s ^ (s >>> 15), 1 | s);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function hashSeed(str) {
    let h = 2166136261;
    for (let i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return h >>> 0;
  }
  function gaussianSample(rng) {
    const u1 = Math.max(rng(), 1e-12);
    const u2 = rng();
    return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  }
  // farads; at/above this a capacitor is a real polarized electrolytic
  // (matches components.js's drawing threshold -- the same real part,
  // just two different concerns needing the same number)
  const ELECTROLYTIC_THRESHOLD = 1e-6;
  // volts; a real electrolytic's typical absolute-max reverse-voltage
  // rating before the dielectric breaks down -- conservative but real
  const REVERSE_POLARITY_LIMIT = 1.0;

  // A plain Inductor doesn't expose turns/gauge/core the way the Ferrite
  // Toroid does, so it can't compute a winding resistance from first
  // principles the same way -- but a real inductor is never a bare L
  // either. This is an honest order-of-magnitude estimate (DCR ~ sqrt(L),
  // the real trend across a typical small commercial radial-inductor
  // product family: more turns for more inductance, but also thicker
  // wire/larger cores at the high end), not a specific part's datasheet
  // number -- real DCR for a specific inductor varies with its physical
  // size and should be checked against that part's own datasheet.
  function inductorDCR(L) {
    return 0.5 * Math.sqrt(Math.max(L, 1e-9) * 1000);
  }

  // Real capacitors are not pure C: every real part has a real series ESR
  // (dominated by electrolyte/foil resistance for electrolytics, by
  // termination + dielectric loss for ceramics) and a real parallel
  // leakage/self-discharge resistance (dielectric absorption current).
  // Both are genuine, measurable, datasheet-relevant numbers, not
  // decoration -- an electrolytic's ESR is often the single biggest real
  // limit on how fast it can actually deliver current, and its leakage
  // is exactly why a "held" sample doesn't stay held forever even with a
  // perfect external circuit.
  function capacitorESR(c) {
    if (c.value >= ELECTROLYTIC_THRESHOLD) {
      // real small-signal electrolytics commonly run from a few ohms at
      // 1uF-class down to well under 0.1 ohm at 1000uF-class -- an
      // empirical ESR ~ 1/C trend (not exact for any one part number,
      // but the right order of magnitude across the range this
      // simulator's CAPACITOR_VALUES actually offers)
      return Math.max(0.05, 2e-5 / c.value);
    }
    // ceramics: dominated by termination/lead resistance, real but tiny
    return 0.05;
  }
  function capacitorLeakageR(c) {
    if (c.value >= ELECTROLYTIC_THRESHOLD) {
      // real electrolytics self-discharge on the order of tens of
      // minutes to an hour open-circuit -- a real, commonly-cited rule of
      // thumb is a leakage time constant (R_leak * C) around 1800s (30
      // minutes); R_leak = tau / C follows directly from that
      return 1800 / c.value;
    }
    // ceramics: leakage is real but many orders of magnitude smaller --
    // a self-discharge time constant this long is effectively "never" at
    // any timescale this simulator runs, which is the honest real answer
    return 1e11;
  }
  // Real off-the-shelf parts don't hit their nominal value exactly -- these
  // are standard, honest manufacturing tolerance bands for each part
  // class (not tuned per-circuit), used by a Monte Carlo tolerance run
  // (simulate.js's `monteCarlo` mode) to sample each part's real value
  // within its real spread, so a design has to keep working across real
  // part variation instead of one perfect nominal case.
  const COMPONENT_TOLERANCE = {
    resistor: 0.05, // +/-5%, standard through-hole metal-film resistor (E24 series)
    capacitor: 0.10, // +/-10%, typical ceramic/film cap
    battery: 0.02, // +/-2%, typical fresh-cell/regulated-supply voltage spread
    inductor: 0.10, // +/-10%, typical wound-inductor tolerance
  };
  function capacitorToleranceFor(c) {
    // electrolytics ship with a much wider band than ceramics/film --
    // +/-20% is a common real datasheet figure (some are -20%/+80%, but
    // +/-20% is the honest symmetric approximation this simulator uses)
    return c.value >= ELECTROLYTIC_THRESHOLD ? 0.20 : COMPONENT_TOLERANCE.capacitor;
  }
  const VGND_RINT = 2; // ohms, output impedance of a rail-splitter / virtual-ground buffer (e.g. TLE2426-class)
  // amps; a real TLE2426-class rail splitter is only rated to source/sink
  // a real, finite output current (the datasheet's typical continuous
  // rating) before it can no longer hold the midpoint under load -- past
  // that, real load regulation (VGND_RINT) breaks down and the part just
  // can't supply more current, so V(out) sags hard instead of following
  // Ohm's law forever.
  const VGND_MAX_CURRENT = 0.02;
  // volts; once current-limited, a real output stage still physically
  // cannot swing its pin past its own supply rails -- the pass
  // transistors (and/or their substrate/ESD protection diodes) sit
  // between those rails. This is the real saturation/protection headroom
  // beyond a rail before that path clamps, same real-diode-clamp idea as
  // a MOSFET's body diode, not a per-part-number datasheet figure. Used
  // by both the vgnd rail-splitter and the comparator's push-pull output
  // (with its own smaller, rail-to-rail-appropriate headroom below).
  const RAIL_CLAMP_VF = 0.3;
  const RAIL_CLAMP_RON = 5; // ohms, real forward resistance of that clamp path
  const AC_RINT = 1; // ohms, output impedance of an ideal AC/function-generator source
  const MTJ_RINT = 200; // ohms, buffered analog-output impedance of a real MTJ/TMR angle-sensor IC's sin/cos pins

  // Single-coil magnetic latching relay (e.g. Panasonic TQ2-L-5V class):
  // reverse the coil drive polarity to set/reset, the contact state is
  // held by real remanence after the drive pulse disappears. Electrically
  // this is a real coil (resistance + the SAME square-loop magnetic
  // dynamics the memorycore already models -- polarity-sensitive
  // set/reset, real coercive threshold, real finite switching time,
  // genuine incomplete-switching if the drive pulse doesn't supply enough
  // current for long enough) driving a real mechanical contact. Values
  // below are honest order-of-magnitude approximations for this part
  // class from public datasheet figures, not one specific lot's spec.
  const LATCHRELAY_SPEC = {
    coilR: 139, // ohms, 5V-coil-class winding resistance
    hcAmpTurns: 0.02, // amps (turns=1 for a lumped single coil, so this IS the real "must-operate" current) -- comfortably below a nominal 5V/139ohm~=36mA drive, comfortably above real coil leakage, so a weak/marginal drive genuinely fails to switch
    phiSat: 4e-6, // Weber-equivalent, sized for a modest, real-scale induced-voltage kick on switching -- relay datasheets don't publish this directly, approximate
    switchTau: 0.003, // seconds, real small-latching-relay operate/release time
    contactR: 0.05, // ohms, real closed-contact resistance for a small signal relay
    contactOpenR: 1e9, // ohms, effectively open
    armatureThreshold: 0.5, // fraction of full remanence; the mechanical armature is a real snap-action mechanism, not proportional -- it only actually moves once driven this far past center, then holds (hysteretic) until driven the other way
    bounceDuration: 0.005, // seconds, real mechanical contact bounce/settling window after an actual armature transition
    bounceRFrac: 3, // contact resistance during bounce is noisy and elevated by roughly this factor over nominal, real for a bouncing mechanical contact
  };
  function latchRelaySpec(c) {
    return Object.assign({}, LATCHRELAY_SPEC, c && c.spec);
  }

  // Discrete MOSFETs: real parts, real limits. "value" selects between two
  // real part classes rather than a made-up continuous parameter -- the
  // same idea as LED_VF picking a real forward-voltage family by color.
  // RDS(on) here is a fixed on-resistance once the channel is on (a
  // piecewise switch model), not a continuous Vgs-dependent square law --
  // sufficient for "does this switch turn on/off and clamp near its rail",
  // which is what a breadboard-level design needs to get right first.
  // ciss (input capacitance, Cgs+Cgd) is the textbook-typical datasheet
  // figure for each named part class, used as an approximate lumped
  // gate-to-source capacitance for real switching-delay purposes -- it is
  // NOT a full nonlinear Cgs/Cgd/Crss model, just the honest order-of-
  // magnitude real gate charge a driving source actually has to slew
  // through before the channel can respond, instead of an idealized
  // instant-response gate.
  const NMOS_PARTS = {
    1.5: { name: 'AO3400A-class (logic-level)', vth: 1.5, rdsOn: 0.03, vgsMax: 12, vdsMax: 30, ciss: 300e-12 },
    2.1: { name: '2N7000-class', vth: 2.1, rdsOn: 5, vgsMax: 20, vdsMax: 60, ciss: 24e-12 },
  };
  const PMOS_PARTS = {
    1.5: { name: 'AO3401A-class (logic-level)', vth: -1.5, rdsOn: 0.05, vgsMax: 12, vdsMax: 30, ciss: 470e-12 },
    2.1: { name: 'BS250-class', vth: -2.1, rdsOn: 5, vgsMax: 20, vdsMax: 60, ciss: 40e-12 },
  };
  function mosfetSpec(c) {
    const table = c.type === 'pmos' ? PMOS_PARTS : NMOS_PARTS;
    return table[c.value] || table[1.5];
  }

  // Real TLV3202 dual comparator (TI datasheet): rail-to-rail push-pull
  // output (not open-drain -- no pull-up needed), input offset voltage a
  // few mV, and a real minimum operating supply voltage. `outputRon` is a
  // real push-pull output stage's small on-resistance, not an idealized
  // zero-ohm switch -- the same "fixed on-resistance once a decision is
  // made" idea as a MOSFET's RDS(on).
  const COMPARATOR_SPEC = {
    name: 'TLV3202 (dual, rail-to-rail push-pull)',
    outputRon: 40, // ohms, approximate push-pull output impedance
    vosTyp: 0.002, // volts, typical input offset voltage
    vosMax: 0.01, // volts, worst-case input offset voltage (datasheet max)
    vccMin: 2.7, // volts, minimum specified supply voltage
    vccMax: 5.5, // volts, maximum specified supply voltage
    cmRangeOver: 0.2, // volts, how far past either rail the real common-mode range extends
    // seconds; a real fast low-power comparator of this class -- the
    // output does not flip the instant Vin crosses Vos, it flips
    // propDelay later. At this simulator's typical frame dt (ms-scale)
    // this resolves within the same frame almost always (honest: it's
    // genuinely this fast on a real bench too), but it becomes real and
    // testable the moment dt is pushed small enough to matter (a fast
    // headless run, or a tight feedback loop with its own short time
    // constant) -- exactly the regime where an idealized zero-delay
    // comparator could hide a real oscillation or race.
    propDelay: 4e-8,
    // amps; a real small-signal CMOS push-pull output stage's typical
    // rated output current -- beyond this the real part can't swing
    // further, so a hard current-limited output (like the vgnd rail-
    // splitter above) replaces the soft outputRon-only limit.
    outputMaxCurrent: 0.008,
    // volts; a real rail-to-rail output stage saturates much closer to
    // its rails than a generic (non-rail-to-rail) part -- a small,
    // honest headroom, not RAIL_CLAMP_VF's more generic default.
    clampVf: 0.1,
  };

  // Reversible inductive H-bridge driver (DRV8833-class; one component
  // instance is ONE bridge/channel -- a real DRV8833 packages two of
  // these). Real logic-level control inputs (in1/in2) select a real
  // 4-state truth table (coast/forward/reverse/brake), and real body
  // diodes on both outputs (present regardless of FET state, exactly like
  // a real MOSFET's own body diode) provide the real flyback/recirculation
  // path an inductive load needs -- an ideal bridge that could reverse
  // inductor current instantaneously is not physically possible.
  const HBRIDGE_SPEC = {
    name: 'DRV8833-class H-bridge (one channel)',
    ronHS: 0.15, // ohms, real high-side FET RDS(on)
    ronLS: 0.15, // ohms, real low-side FET RDS(on)
    bodyDiodeVf: 0.7, // volts, real body-diode forward drop (silicon)
    bodyDiodeRon: 5, // ohms, real body-diode forward resistance
    // seconds; real logic-to-output propagation delay, INCLUDING this
    // part's real internal shoot-through-prevention dead time -- a
    // datasheet's propagation-delay figure already reflects that the part
    // never has both FETs on the same output conducting at once, so this
    // single delay is an honest simplification of "current can't reverse
    // instantaneously and switching isn't infinitely fast", not a
    // separate two-stage dead-time model.
    propDelay: 3e-7,
    inputThreshold: 1.3, // volts, real logic input threshold (CMOS/TTL-class)
    vmMin: 2.7, // volts, real minimum motor-supply voltage (below this, real undervoltage lockout forces outputs off)
    vmMax: 10.8, // volts, real maximum motor-supply voltage
    currentLimit: 1.5, // amps, real per-channel continuous output current rating
  };
  function hbridgeSpec(c) {
    return Object.assign({}, HBRIDGE_SPEC, c && c.spec);
  }

  // Single Schmitt-trigger inverter (SN74HC14-class, one of its six
  // gates). Real hysteresis: the input has TWO thresholds, not one -- it
  // has to rise past the higher one to register HIGH, then fall past the
  // LOWER one to register LOW again, holding its prior decision anywhere
  // in between. That gap is exactly what a noisy signal near a single
  // fixed threshold needs to avoid chattering; a plain comparator (single
  // threshold plus a fixed offset) cannot provide it. Real HC-family
  // thresholds scale with supply voltage rather than being fixed volts,
  // so they're specified here as fractions of VCC.
  const SCHMITT_SPEC = {
    name: 'SN74HC14 (hex Schmitt-trigger inverter, one gate)',
    vtPlusFrac: 0.58, // fraction of VCC; input must rise above this to register HIGH (real HC-family ~2.9V typ at VCC=5V)
    vtMinusFrac: 0.34, // fraction of VCC; input must fall below this to register LOW again (real HC-family ~1.7V typ at VCC=5V)
    outputRon: 45, // ohms, real push-pull output impedance for this logic family
    propDelay: 15e-9, // seconds, real gate propagation delay
    vccMin: 2, // volts
    vccMax: 6, // volts
    clampVf: 0.3, // volts, real output protection headroom past the rails (not rail-to-rail like the comparator)
  };
  function schmittSpec(c) {
    return Object.assign({}, SCHMITT_SPEC, c && c.spec);
  }

  // shared time-domain waveform used by AC sources and the MTJ sensor's
  // sin/cos channels -- a real sinusoid evaluated at the simulator's own
  // running clock, not a single-frequency phasor snapshot
  function wave(amplitude, freqHz, phaseDeg, t) {
    return amplitude * Math.sin(2 * Math.PI * freqHz * t + (phaseDeg * Math.PI) / 180);
  }

  // LEDs and plain diodes are the same device electrically (one-way
  // conduction past a threshold) — only the threshold/dynamic-resistance and
  // whether it glows differ.
  function forwardVoltage(c) {
    return c.type === 'diode' ? DIODE_VF : LED_VF[c.color] || 1.8;
  }
  function forwardRon(c) {
    return c.type === 'diode' ? DIODE_RON : LED_RON;
  }

  function solveLinear(A, bIn) {
    const n = bIn.length;
    const M = A.map((row, i) => row.concat([bIn[i]]));
    for (let col = 0; col < n; col++) {
      let piv = col;
      let maxAbs = Math.abs(M[col][col]);
      for (let r = col + 1; r < n; r++) {
        if (Math.abs(M[r][col]) > maxAbs) {
          maxAbs = Math.abs(M[r][col]);
          piv = r;
        }
      }
      if (maxAbs < 1e-15) continue;
      if (piv !== col) {
        const tmp = M[col];
        M[col] = M[piv];
        M[piv] = tmp;
      }
      const pivVal = M[col][col];
      for (let r = 0; r < n; r++) {
        if (r === col) continue;
        const factor = M[r][col] / pivVal;
        if (factor === 0) continue;
        for (let c = col; c <= n; c++) {
          M[r][c] -= factor * M[col][c];
        }
      }
    }
    const x = new Array(n).fill(0);
    for (let i = 0; i < n; i++) {
      x[i] = Math.abs(M[i][i]) < 1e-15 ? 0 : M[i][n] / M[i][i];
    }
    return x;
  }

  class Circuit {
    constructor() {
      this.reset();
    }
    reset() {
      this._ledState = new Map(); // component id -> boolean (conducting)
      this._capState = new Map(); // component id -> voltage across it last frame
      this._indState = new Map(); // component id -> current through it last frame
      this._toroidState = new Map(); // toroid id -> array of per-winding currents last frame
      this._fetChannelState = new Map(); // mosfet id -> boolean (channel conducting)
      this._fetDiodeState = new Map(); // mosfet id -> boolean (body diode conducting)
      this._fetGateV = new Map(); // mosfet id -> Vgs last frame (real gate capacitance charge state)
      this._coreState = new Map(); // memory-core id -> normalized remanent flux B in [-1, 1], persists across frames
      this._compState = new Map(); // "<comparatorId>:<channel>" -> boolean (LATCHED output actually driven HIGH toward VCC, after propagation delay)
      this._compDesired = new Map(); // "<comparatorId>:<channel>" -> boolean (what the raw Vin+/Vin- comparison currently says, before delay)
      this._compDesiredSince = new Map(); // "<comparatorId>:<channel>" -> sim-clock time the desired value last changed
      this._compOutLimited = new Map(); // "<comparatorId>:<channel>" -> boolean (output current-limited, real push-pull stage can't swing further)
      this._compOutLimitDir = new Map(); // "<comparatorId>:<channel>" -> +1/-1, which way it was sourcing/sinking when it hit the limit
      this._vgndLimited = new Map(); // vgnd id -> boolean (output current-limited, can't hold the midpoint under this load)
      this._vgndLimitDir = new Map(); // vgnd id -> +1/-1, which way it was sourcing/sinking when it hit the limit
      // real output/protection clamp-diode on/off state, keyed by a
      // descriptive string per clamp path (see the stamping code) --
      // shared by the vgnd rail-splitter's output and the comparator's
      // push-pull outputs, since both need the exact same real "this pin
      // physically cannot swing past its own supply rails" constraint
      this._railClampState = new Map();
      this._diffNoiseRng = new Map(); // diffsource id -> its own seeded PRNG (a real independent noise sequence over time)
      this._diffNoiseSample = new Map(); // diffsource id -> this frame's sampled noise volts (resampled once per new sim-clock tick, not per fixed-point iteration)
      this._diffNoiseAtT = new Map(); // diffsource id -> sim-clock time the cached sample was drawn at
      this._latchContactClosed = new Map(); // latchrelay id -> boolean (real mechanical armature position -- a snap-action mechanism, not proportional to B)
      this._latchLastFlipT = new Map(); // latchrelay id -> sim-clock time the contact last actually moved (drives the real post-transition bounce/unsettled window)
      this._latchBounceRng = new Map(); // latchrelay id -> its own seeded PRNG for real bounce-noise contact resistance
      this._latchBounceSample = new Map(); // latchrelay id -> this frame's sampled bounce noise factor
      this._latchBounceAtT = new Map(); // latchrelay id -> sim-clock time the cached bounce sample was drawn at
      this._hbridgeDesired = new Map(); // hbridge id -> 'coast'|'forward'|'reverse'|'brake', what the real IN1/IN2 comparison currently says
      this._hbridgeDesiredSince = new Map(); // hbridge id -> sim-clock time the desired mode last changed
      this._hbridgeMode = new Map(); // hbridge id -> the LATCHED mode actually driving the outputs, after real propagation delay
      this._hbridgeDiodeState = new Map(); // "<id>:<out1|out2>:<hi|lo>" -> boolean, the real body-diode flyback paths, on/off exactly like a MOSFET's body diode
      this._schmittInputHigh = new Map(); // schmitt id -> boolean, the real hysteretic input-side decision (updates instantly on threshold crossing, no propagation delay -- that's a real internal analog comparator, separate from the output stage)
      this._schmittDesired = new Map(); // schmitt id -> boolean, the INVERTED output value the input-side decision currently implies, before propagation delay
      this._schmittDesiredSince = new Map(); // schmitt id -> sim-clock time the desired output last changed
      this._schmittState = new Map(); // schmitt id -> boolean, the LATCHED output actually driven, after real propagation delay
      this._t = 0; // running sim clock (seconds), shared by every AC/MTJ source
    }

    /**
     * elements = {
     *   wires: [{a, b}],                 // zero-resistance jumper wires
     *   components: [{id, type, a, b, value, color, closed, pos, wiper}]
     * }
     * dt = seconds since last solve (for capacitor transient stepping)
     */
    solve(elements, dt) {
      const wires = elements.wires || [];
      const components = elements.components || [];
      const uf = new UnionFind();
      this._t += dt;
      const t = this._t;

      const batInternal = (c) => '__batint__' + c.id;
      // diffsource: a real EMF of "value" volts referenced to whatever its
      // own b-pin is wired to (its real reference input), through its own
      // real source impedance -- see the `batteries` filter comment below
      // for why it reuses the battery's exact MNA structure.
      const sourceRFor = (c) => (c.type === 'diffsource' ? (c.sourceR != null ? c.sourceR : DIFFSOURCE_RINT) : BATTERY_RINT);
      const diffNoiseSample = (c) => {
        if (!c.noiseRms) return 0;
        // resample once per new sim-clock tick, not per fixed-point
        // iteration -- a real noise source has one value per instant, and
        // resampling mid-iteration would just be numerical jitter, not
        // real noise
        if (this._diffNoiseAtT.get(c.id) !== t) {
          if (!this._diffNoiseRng.has(c.id)) {
            this._diffNoiseRng.set(c.id, mulberry32(hashSeed(String(c.noiseSeed != null ? c.noiseSeed : c.id))));
          }
          const rng = this._diffNoiseRng.get(c.id);
          this._diffNoiseSample.set(c.id, gaussianSample(rng) * c.noiseRms);
          this._diffNoiseAtT.set(c.id, t);
        }
        return this._diffNoiseSample.get(c.id) || 0;
      };
      const effectiveSourceValue = (c) => (c.type === 'diffsource' ? c.value + diffNoiseSample(c) : c.value);

      // real relay contact resistance: nominal closed/open value, except
      // for a real, bounded window right after the armature actually moved
      // (this frame's t vs the last real flip time -- see the armature
      // decision above) where a real mechanical contact bounces, making
      // and breaking intermittently -- modeled honestly here as noisy,
      // elevated resistance rather than simulating literal chatter events.
      // Resampled once per new sim-clock tick, not per fixed-point
      // iteration, for the same reason diffsource's noise is.
      const latchContactResistance = (lr) => {
        const spec = latchRelaySpec(lr);
        const closed = this._latchContactClosed.get(lr.id) || false;
        const base = closed ? spec.contactR : spec.contactOpenR;
        const lastFlip = this._latchLastFlipT.get(lr.id);
        if (lastFlip == null || t - lastFlip >= spec.bounceDuration) return base;
        if (this._latchBounceAtT.get(lr.id) !== t) {
          if (!this._latchBounceRng.has(lr.id)) {
            this._latchBounceRng.set(lr.id, mulberry32(hashSeed(lr.id + ':bounce')));
          }
          const rng = this._latchBounceRng.get(lr.id);
          const factor = 1 + Math.abs(gaussianSample(rng)) * (spec.bounceRFrac - 1);
          this._latchBounceSample.set(lr.id, factor);
          this._latchBounceAtT.set(lr.id, t);
        }
        return base * (this._latchBounceSample.get(lr.id) || 1);
      };
      const vgndInternal = (c) => '__vgndint__' + c.id;
      const acInternal = (c) => '__acint__' + c.id;
      const mtjSinInternal = (c) => '__mtjsin__' + c.id;
      const mtjCosInternal = (c) => '__mtjcos__' + c.id;

      wires.forEach((w) => uf.union(w.a, w.b));
      components.forEach((c) => {
        uf.find(c.a);
        uf.find(c.b);
        if (c.type === 'potentiometer') uf.find(c.wiper);
        if ((c.type === 'switch' || c.type === 'pushbutton') && c.closed) uf.union(c.a, c.b);
        if (c.type === 'battery' || c.type === 'diffsource') uf.find(batInternal(c));
        if (c.type === 'vgnd') {
          uf.find(c.out);
          uf.find(vgndInternal(c));
        }
        if (c.type === 'acsource') uf.find(acInternal(c));
        if (c.type === 'mtjsensor') {
          uf.find(c.sin);
          uf.find(c.cos);
          uf.find(mtjSinInternal(c));
          uf.find(mtjCosInternal(c));
        }
        if (c.type === 'toroid') c.windings.forEach((w) => { uf.find(w.a); uf.find(w.b); });
        if (c.type === 'nmos' || c.type === 'pmos') { uf.find(c.gate); uf.find(c.drain); uf.find(c.source); }
        if (c.type === 'memorycore' || c.type === 'latchrelay') c.windings.forEach((w) => { uf.find(w.a); uf.find(w.b); });
        if (c.type === 'latchrelay') { uf.find(c.contactA); uf.find(c.contactB); }
        if (c.type === 'comparator') {
          uf.find(c.in1p); uf.find(c.in1m); uf.find(c.out1);
          uf.find(c.in2p); uf.find(c.in2m); uf.find(c.out2);
          uf.find(c.vcc); uf.find(c.gnd);
        }
        if (c.type === 'hbridge') {
          uf.find(c.in1); uf.find(c.in2); uf.find(c.vm); uf.find(c.gnd);
          uf.find(c.out1); uf.find(c.out2);
        }
        if (c.type === 'schmitt') {
          uf.find(c.in); uf.find(c.out); uf.find(c.vcc); uf.find(c.gnd);
        }
      });

      // diffsource shares the exact same ideal-EMF-plus-series-resistance
      // MNA structure as a battery (extra branch-current unknown via
      // rowBat) -- it is a real 2-terminal source too, just one whose EMF
      // is specified as "value volts relative to whatever node b is
      // wired to" (its real reference pin) instead of an absolute rail,
      // and with its own real (smaller, precision-source-typical) output
      // impedance instead of a battery's. Grouping them together reuses
      // all of the existing extra-unknown row bookkeeping below with no
      // change to any other row offset.
      const batteries = components.filter((c) => c.type === 'battery' || c.type === 'diffsource');
      const vgnds = components.filter((c) => c.type === 'vgnd');
      const inductors = components.filter((c) => c.type === 'inductor');
      const acsources = components.filter((c) => c.type === 'acsource');
      const mtjsensors = components.filter((c) => c.type === 'mtjsensor');
      const toroids = components.filter((c) => c.type === 'toroid');
      const mosfets = components.filter((c) => c.type === 'nmos' || c.type === 'pmos');
      // a latchrelay's coil is, electrically, exactly a one-winding
      // memorycore (real winding resistance + the same square-loop
      // magnetic dynamics) -- folding it into the same array reuses all
      // of that already-proven extra-unknown-row machinery unmodified.
      // Its separate mechanical contact is stamped independently below,
      // as an ordinary resistor whose value depends on the persisted B.
      const memoryCores = components.filter((c) => c.type === 'memorycore' || c.type === 'latchrelay');
      const comparators = components.filter((c) => c.type === 'comparator');
      const hbridges = components.filter((c) => c.type === 'hbridge');
      const schmitts = components.filter((c) => c.type === 'schmitt');

      let groundRoot = null;
      if (batteries.length) groundRoot = uf.find(batteries[0].b);
      else if (wires.length) groundRoot = uf.find(wires[0].a);
      else if (components.length) groundRoot = uf.find(components[0].a);

      if (groundRoot === null) {
        return { voltages: new Map(), currents: new Map(), warnings: [], hasCircuit: false };
      }

      const roots = new Set();
      // touchCount: how many distinct pins (wires + component terminals)
      // land on each electrical node -- used to detect a MOSFET gate that
      // isn't wired to anything at all (a node touched exactly once, by
      // its own gate pin and nothing else: no wire, no other component).
      const touchCount = new Map();
      const touch = (id) => {
        const r = uf.find(id);
        roots.add(r);
        touchCount.set(r, (touchCount.get(r) || 0) + 1);
      };
      wires.forEach((w) => {
        touch(w.a);
        touch(w.b);
      });
      components.forEach((c) => {
        touch(c.a);
        touch(c.b);
        if (c.type === 'potentiometer') touch(c.wiper);
        if (c.type === 'battery' || c.type === 'diffsource') touch(batInternal(c));
        if (c.type === 'vgnd') {
          touch(c.out);
          touch(vgndInternal(c));
        }
        if (c.type === 'acsource') touch(acInternal(c));
        if (c.type === 'mtjsensor') {
          touch(c.sin);
          touch(c.cos);
          touch(mtjSinInternal(c));
          touch(mtjCosInternal(c));
        }
        if (c.type === 'toroid') c.windings.forEach((w) => { touch(w.a); touch(w.b); });
        if (c.type === 'nmos' || c.type === 'pmos') { touch(c.gate); touch(c.drain); touch(c.source); }
        if (c.type === 'memorycore' || c.type === 'latchrelay') c.windings.forEach((w) => { touch(w.a); touch(w.b); });
        if (c.type === 'latchrelay') { touch(c.contactA); touch(c.contactB); }
        if (c.type === 'comparator') {
          touch(c.in1p); touch(c.in1m); touch(c.out1);
          touch(c.in2p); touch(c.in2m); touch(c.out2);
          touch(c.vcc); touch(c.gnd);
        }
        if (c.type === 'hbridge') {
          touch(c.in1); touch(c.in2); touch(c.vm); touch(c.gnd);
          touch(c.out1); touch(c.out2);
        }
        if (c.type === 'schmitt') {
          touch(c.in); touch(c.out); touch(c.vcc); touch(c.gnd);
        }
      });
      roots.add(groundRoot);

      const nodeIndex = new Map();
      let idx = 0;
      for (const r of roots) if (r !== groundRoot) nodeIndex.set(r, idx++);
      const nNodes = idx;
      const nSrc = batteries.length;
      const nVgnd = vgnds.length;
      const nInd = inductors.length;
      const nAc = acsources.length;
      const nMtj = mtjsensors.length;
      const nToroidRows = toroids.reduce((s, tor) => s + tor.windings.length, 0);
      // extra-unknown row offsets, in stamping order: batteries, vgnds,
      // inductors, ac sources, 2 rows (sin, cos) per MTJ sensor, then one
      // row per toroid winding (windings of the same toroid stay adjacent)
      const rowBat = (k) => nNodes + k;
      const rowVgnd = (k) => nNodes + nSrc + k;
      const rowInd = (k) => nNodes + nSrc + nVgnd + k;
      const rowAc = (k) => nNodes + nSrc + nVgnd + nInd + k;
      const rowMtjSin = (k) => nNodes + nSrc + nVgnd + nInd + nAc + k * 2;
      const rowMtjCos = (k) => nNodes + nSrc + nVgnd + nInd + nAc + k * 2 + 1;
      const toroidRowBase = nNodes + nSrc + nVgnd + nInd + nAc + nMtj * 2;
      const toroidRowOffsets = [];
      {
        let off = toroidRowBase;
        toroids.forEach((tor) => {
          toroidRowOffsets.push(off);
          off += tor.windings.length;
        });
      }
      const rowToroid = (torK, windingIdx) => toroidRowOffsets[torK] + windingIdx;
      const nMemCoreRows = memoryCores.reduce((s, mc) => s + mc.windings.length, 0);
      const memCoreRowBase = toroidRowBase + nToroidRows;
      const memCoreRowOffsets = [];
      {
        let off = memCoreRowBase;
        memoryCores.forEach((mc) => {
          memCoreRowOffsets.push(off);
          off += mc.windings.length;
        });
      }
      const rowMemCore = (mcK, windingIdx) => memCoreRowOffsets[mcK] + windingIdx;
      const size = memCoreRowBase + nMemCoreRows;

      const gi = (rt) => (rt === groundRoot ? -1 : nodeIndex.get(rt));

      const diodes = components.filter((c) => c.type === 'led' || c.type === 'diode');
      diodes.forEach((d) => {
        if (!this._ledState.has(d.id)) this._ledState.set(d.id, false);
      });
      mosfets.forEach((f) => {
        // a fresh MOSFET (just placed, or a fresh reset -- power just
        // started) always begins fully off, same reasoning as the diode/LED
        // on/off state: don't presume a decision before ever solving
        if (!this._fetChannelState.has(f.id)) this._fetChannelState.set(f.id, false);
        if (!this._fetDiodeState.has(f.id)) this._fetDiodeState.set(f.id, false);
        if (!this._fetGateV.has(f.id)) this._fetGateV.set(f.id, 0);
      });
      memoryCores.forEach((mc) => {
        // a fresh core (just placed, or a fresh reset) starts demagnetized --
        // no history to presume a remanence from
        if (!this._coreState.has(mc.id)) this._coreState.set(mc.id, 0);
      });
      comparators.forEach((cp) => {
        // a fresh comparator (just placed, or a fresh reset) starts with
        // both outputs LOW -- same "don't presume a decision" reasoning as
        // the diode/MOSFET on/off state above
        ['1', '2'].forEach((ch) => {
          const key = cp.id + ':' + ch;
          if (!this._compState.has(key)) this._compState.set(key, false);
          if (!this._compDesired.has(key)) this._compDesired.set(key, false);
          // "since t-dt" (the START of this step), not "since t" (its end) --
          // a desired-state change detected mid-step is conservatively
          // treated as having held for this whole step's dt already, so a
          // real propDelay far smaller than dt (the normal case) resolves
          // within the SAME step instead of always costing one whole extra
          // step no matter how small propDelay actually is
          if (!this._compDesiredSince.has(key)) this._compDesiredSince.set(key, t - dt);
          if (!this._compOutLimited.has(key)) this._compOutLimited.set(key, false);
          if (!this._compOutLimitDir.has(key)) this._compOutLimitDir.set(key, 1);
        });
      });
      vgnds.forEach((v) => {
        // a fresh rail splitter starts un-limited -- no load history yet
        if (!this._vgndLimited.has(v.id)) this._vgndLimited.set(v.id, false);
        if (!this._vgndLimitDir.has(v.id)) this._vgndLimitDir.set(v.id, 1);
      });
      hbridges.forEach((hb) => {
        // a fresh bridge starts coasting -- same "don't presume a decision"
        // reasoning as every other on/off state above
        if (!this._hbridgeDesired.has(hb.id)) this._hbridgeDesired.set(hb.id, 'coast');
        if (!this._hbridgeDesiredSince.has(hb.id)) this._hbridgeDesiredSince.set(hb.id, t - dt);
        if (!this._hbridgeMode.has(hb.id)) this._hbridgeMode.set(hb.id, 'coast');
      });
      schmitts.forEach((sg) => {
        // a fresh gate starts with input LOW (a real gate at power-up has
        // no history to presume from) -- so its inverted output starts HIGH
        if (!this._schmittInputHigh.has(sg.id)) this._schmittInputHigh.set(sg.id, false);
        if (!this._schmittDesired.has(sg.id)) this._schmittDesired.set(sg.id, true);
        if (!this._schmittDesiredSince.has(sg.id)) this._schmittDesiredSince.set(sg.id, t - dt);
        if (!this._schmittState.has(sg.id)) this._schmittState.set(sg.id, true);
      });
      // per-frame working state for the square-loop cores: coreBStart is
      // fixed for the whole frame (this is the real physical B the core had
      // at the start of this dt, exactly like a capacitor's/inductor's
      // "previous" state) and is what dB/dt is measured against; coreB is
      // the fixed-point loop's current best guess of B at the END of this
      // same dt, refined each inner iteration exactly like a diode's on/off
      // guess -- it never accumulates across iterations, it's recomputed
      // from coreBStart every time using this frame's real dt, so iterating
      // to convergence here finds the self-consistent (current, B) pair for
      // ONE real time step, not several.
      const coreBStart = new Map();
      const coreB = new Map();
      memoryCores.forEach((mc) => {
        const b0 = this._coreState.get(mc.id);
        coreBStart.set(mc.id, b0);
        coreB.set(mc.id, b0);
      });

      // real mechanical armature: a snap-action mechanism, not proportional
      // to B -- it only actually moves once driven a real distance past
      // center, then HOLDS there (hysteretic) regardless of small wiggles
      // in B, exactly like a real relay's spring-loaded armature. Decided
      // once per frame from bStart (fixed for the whole solve() call), same
      // reasoning as a mechanical part that cannot move within zero time.
      const latchrelays = components.filter((c) => c.type === 'latchrelay');
      latchrelays.forEach((lr) => {
        const spec = latchRelaySpec(lr);
        const bStart = coreBStart.get(lr.id) || 0;
        const wasClosed = this._latchContactClosed.get(lr.id) || false;
        let nowClosed = wasClosed;
        if (!wasClosed && bStart > spec.armatureThreshold) nowClosed = true;
        else if (wasClosed && bStart < -spec.armatureThreshold) nowClosed = false;
        if (nowClosed !== wasClosed) {
          this._latchContactClosed.set(lr.id, nowClosed);
          this._latchLastFlipT.set(lr.id, t);
        }
      });

      let voltages = new Map();
      let xSol = new Array(size).fill(0);

      const iterations = size === 0 ? 0 : 30;
      for (let iter = 0; iter < Math.max(iterations, 1); iter++) {
        const A = Array.from({ length: size }, () => new Array(size).fill(0));
        const b = new Array(size).fill(0);
        const stampG = (i, j, val) => {
          if (i >= 0 && j >= 0) A[i][j] += val;
        };
        const stampI = (i, val) => {
          if (i >= 0) b[i] += val;
        };
        // real output/protection clamp diode: same on/off ideal-diode
        // stamp as the LED/rectifier and MOSFET body-diode models above,
        // just reused here for "this pin cannot swing past its own supply
        // rail" instead of a discrete part's own two leads.
        const stampClampDiode = (anode, cathode, on, vf, ron) => {
          if (!on) return;
          const g = 1 / ron;
          stampG(anode, anode, g);
          stampG(cathode, cathode, g);
          stampG(anode, cathode, -g);
          stampG(cathode, anode, -g);
          const Ieq = g * vf;
          stampI(anode, Ieq);
          stampI(cathode, -Ieq);
        };

        for (const r of roots) {
          if (r === groundRoot) continue;
          const i = gi(r);
          stampG(i, i, GMIN);
        }

        components.forEach((c) => {
          if (c.type === 'resistor') {
            const g = 1 / Math.max(c.value, 1e-6);
            const i = gi(uf.find(c.a));
            const j = gi(uf.find(c.b));
            stampG(i, i, g);
            stampG(j, j, g);
            stampG(i, j, -g);
            stampG(j, i, -g);
          } else if (c.type === 'latchrelay') {
            // the real mechanical contact: an ordinary resistor whose real
            // value depends on the armature position decided once per
            // frame above -- this is NOT the coil (the coil's own
            // resistance + magnetic dynamics are stamped by the shared
            // memoryCores extra-unknown-row block, since a latchrelay's
            // coil electrically IS a one-winding memorycore).
            const g = 1 / latchContactResistance(c);
            const i = gi(uf.find(c.contactA));
            const j = gi(uf.find(c.contactB));
            stampG(i, i, g);
            stampG(j, j, g);
            stampG(i, j, -g);
            stampG(j, i, -g);
          } else if (c.type === 'potentiometer') {
            const total = Math.max(c.value, 1);
            const pos = Math.min(Math.max(c.pos ?? 0.5, 0), 1);
            const r1 = Math.max(total * pos, 1);
            const r2 = Math.max(total * (1 - pos), 1);
            const ia = gi(uf.find(c.a));
            const iw = gi(uf.find(c.wiper));
            const ib = gi(uf.find(c.b));
            const g1 = 1 / r1;
            const g2 = 1 / r2;
            stampG(ia, ia, g1);
            stampG(iw, iw, g1);
            stampG(ia, iw, -g1);
            stampG(iw, ia, -g1);
            stampG(ib, ib, g2);
            stampG(iw, iw, g2);
            stampG(ib, iw, -g2);
            stampG(iw, ib, -g2);
          } else if (c.type === 'capacitor') {
            // real series ESR folds straight into the backward-Euler
            // companion resistance (Rs + dt/C in series is still just one
            // resistance), so this is the SAME Norton-source technique as
            // an ideal cap, just with a real Rs added before inverting --
            // vPrev here is the voltage across the ideal-C portion alone
            // (see the state-update comment below for why that matters).
            const esr = capacitorESR(c);
            const gC = 1 / (esr + Math.max(dt, 1e-6) / c.value);
            const vPrev = this._capState.get(c.id) || 0;
            const i = gi(uf.find(c.a));
            const j = gi(uf.find(c.b));
            stampG(i, i, gC);
            stampG(j, j, gC);
            stampG(i, j, -gC);
            stampG(j, i, -gC);
            const Ieq = gC * vPrev;
            stampI(i, Ieq);
            stampI(j, -Ieq);
            // real parallel leakage/self-discharge path, straight across
            // the external leads (the standard simplified real-capacitor
            // leakage model) -- independent of the ESR+C branch above
            const gLeak = 1 / capacitorLeakageR(c);
            stampG(i, i, gLeak);
            stampG(j, j, gLeak);
            stampG(i, j, -gLeak);
            stampG(j, i, -gLeak);
          } else if (c.type === 'led' || c.type === 'diode') {
            if (this._ledState.get(c.id)) {
              const vf = forwardVoltage(c);
              const g = 1 / forwardRon(c);
              const i = gi(uf.find(c.a));
              const j = gi(uf.find(c.b));
              stampG(i, i, g);
              stampG(j, j, g);
              stampG(i, j, -g);
              stampG(j, i, -g);
              const Ieq = g * vf;
              stampI(i, Ieq);
              stampI(j, -Ieq);
            }
          } else if (c.type === 'nmos' || c.type === 'pmos') {
            // a real discrete MOSFET: a channel (RDS(on) resistor between
            // drain and source, only while gate-source crosses the real
            // threshold) IN PARALLEL WITH a real body diode (silicon-
            // rectifier-class one-way conduction, oriented per channel
            // type). Both are independently on/off -- exactly like the
            // physical part, where the body diode conducts even with the
            // gate held off.
            const spec = mosfetSpec(c);
            const d = gi(uf.find(c.drain));
            const s = gi(uf.find(c.source));
            const g_ = gi(uf.find(c.gate));
            // real gate input capacitance (Ciss, gate to source): the same
            // backward-Euler companion-source technique as an ideal
            // capacitor, with no series ESR of its own -- whatever real
            // impedance is driving the gate (a comparator's outputRon, a
            // resistor, etc.) already supplies the series resistance that
            // sets the real RC charge time, exactly like a real gate driver
            // circuit. This is what turns an idealized instant Vgs flip
            // into a real switching delay when the driving impedance and
            // dt are both small enough for it to show up.
            const gGate = 1 / (Math.max(dt, 1e-6) / spec.ciss);
            const vgPrev = this._fetGateV.get(c.id) || 0;
            stampG(g_, g_, gGate);
            stampG(s, s, gGate);
            stampG(g_, s, -gGate);
            stampG(s, g_, -gGate);
            const IeqGate = gGate * vgPrev;
            stampI(g_, IeqGate);
            stampI(s, -IeqGate);
            if (this._fetChannelState.get(c.id)) {
              const g = 1 / spec.rdsOn;
              stampG(d, d, g);
              stampG(s, s, g);
              stampG(d, s, -g);
              stampG(s, d, -g);
            }
            if (this._fetDiodeState.get(c.id)) {
              // NMOS body diode: anode at source, cathode at drain (blocks
              // drain->source, conducts source->drain past Vf). PMOS is the
              // complementary orientation: anode at drain, cathode at source.
              const anode = c.type === 'nmos' ? s : d;
              const cathode = c.type === 'nmos' ? d : s;
              const g = 1 / DIODE_RON;
              stampG(anode, anode, g);
              stampG(cathode, cathode, g);
              stampG(anode, cathode, -g);
              stampG(cathode, anode, -g);
              const Ieq = g * DIODE_VF;
              stampI(anode, Ieq);
              stampI(cathode, -Ieq);
            }
          } else if (c.type === 'comparator') {
            // a real push-pull output stage is just two small-Ron paths,
            // one to each rail, with exactly one active at a time -- stamp
            // whichever one this channel's fixed-point decision currently
            // holds, same "resistor path selected by a decision" idea as
            // the MOSFET channel above, just choosing between two rails
            // instead of one path being on/off. Below outputMaxCurrent this
            // stays a stiff outputRon path; at the real part's output
            // current rating it switches to a fixed-current-source stamp
            // instead, the same "which real regime are we in" fixed-point
            // choice used for the vgnd rail-splitter above.
            const g = 1 / COMPARATOR_SPEC.outputRon;
            const vccIdx = gi(uf.find(c.vcc));
            const gndIdx = gi(uf.find(c.gnd));
            [['1', c.out1], ['2', c.out2]].forEach(([ch, outPin]) => {
              const o = gi(uf.find(outPin));
              const key = c.id + ':' + ch;
              const target = this._compState.get(key) ? vccIdx : gndIdx;
              if (this._compOutLimited.get(key)) {
                const dir = this._compOutLimitDir.get(key) || 1;
                stampI(o, dir * COMPARATOR_SPEC.outputMaxCurrent);
                stampI(target, -dir * COMPARATOR_SPEC.outputMaxCurrent);
              } else {
                stampG(o, o, g);
                stampG(target, target, g);
                stampG(o, target, -g);
                stampG(target, o, -g);
              }
              // real output-pin protection, same reasoning as the vgnd
              // rail-splitter's clamp above: a rail-to-rail push-pull
              // output still physically cannot swing past VCC/GND by
              // more than its own real (small) saturation headroom, no
              // matter what the current-limited path above would
              // otherwise imply into a weak external load.
              stampClampDiode(o, vccIdx, this._railClampState.get(key + ':hi') || false, COMPARATOR_SPEC.clampVf, RAIL_CLAMP_RON);
              stampClampDiode(gndIdx, o, this._railClampState.get(key + ':lo') || false, COMPARATOR_SPEC.clampVf, RAIL_CLAMP_RON);
            });
          } else if (c.type === 'hbridge') {
            // real reversible drive: each output gets whichever real FET
            // path (high-side to VM, low-side to GND) the LATCHED mode
            // currently calls for, exactly the same "resistor path
            // selected by a decision" idea as the comparator/MOSFET above.
            // Real body diodes on BOTH outputs to BOTH rails are stamped
            // UNCONDITIONALLY (a real body diode exists whether or not its
            // FET is on) -- this is what gives an inductive load (the
            // latching relay coil) a real path to recirculate current
            // through instead of an impossible instantaneous reversal,
            // and what makes "coast" a real Hi-Z-except-for-flyback state
            // rather than a true open circuit.
            const spec = hbridgeSpec(c);
            const vmIdx = gi(uf.find(c.vm));
            const gndIdx = gi(uf.find(c.gnd));
            // (UVLO is folded into the tracked mode decision itself, below
            // -- not read fresh here, since this stamp runs BEFORE this
            // iteration's own solve and would only see stale/empty
            // voltages on a fixed point loop's first pass, with no
            // "changed" signal to force a retry once real voltages exist)
            const mode = this._hbridgeMode.get(c.id) || 'coast';
            [['out1', c.out1, 1], ['out2', c.out2, 2]].forEach(([tag, outPin, outNum]) => {
              const o = gi(uf.find(outPin));
              const highOn = (mode === 'forward' && outNum === 1) || (mode === 'reverse' && outNum === 2);
              const lowOn = (mode === 'forward' && outNum === 2) || (mode === 'reverse' && outNum === 1) || mode === 'brake';
              if (highOn) {
                const g = 1 / spec.ronHS;
                stampG(o, o, g);
                stampG(vmIdx, vmIdx, g);
                stampG(o, vmIdx, -g);
                stampG(vmIdx, o, -g);
              }
              if (lowOn) {
                const g = 1 / spec.ronLS;
                stampG(o, o, g);
                stampG(gndIdx, gndIdx, g);
                stampG(o, gndIdx, -g);
                stampG(gndIdx, o, -g);
              }
              const hiKey = c.id + ':' + tag + ':hi';
              const loKey = c.id + ':' + tag + ':lo';
              stampClampDiode(o, vmIdx, this._hbridgeDiodeState.get(hiKey) || false, spec.bodyDiodeVf, spec.bodyDiodeRon);
              stampClampDiode(gndIdx, o, this._hbridgeDiodeState.get(loKey) || false, spec.bodyDiodeVf, spec.bodyDiodeRon);
            });
          } else if (c.type === 'schmitt') {
            // a real push-pull output stage to whichever rail the LATCHED
            // (propagation-delayed) decision holds -- same "resistor path
            // selected by a decision" idea as the comparator's output.
            const spec = schmittSpec(c);
            const g = 1 / spec.outputRon;
            const o = gi(uf.find(c.out));
            const vccIdx = gi(uf.find(c.vcc));
            const gndIdx = gi(uf.find(c.gnd));
            const target = this._schmittState.get(c.id) ? vccIdx : gndIdx;
            stampG(o, o, g);
            stampG(target, target, g);
            stampG(o, target, -g);
            stampG(target, o, -g);
            stampClampDiode(o, vccIdx, this._railClampState.get(c.id + ':hi') || false, spec.clampVf, RAIL_CLAMP_RON);
            stampClampDiode(gndIdx, o, this._railClampState.get(c.id + ':lo') || false, spec.clampVf, RAIL_CLAMP_RON);
          } else if (c.type === 'battery' || c.type === 'diffsource') {
            const g = 1 / sourceRFor(c);
            const i = gi(uf.find(batInternal(c)));
            const j = gi(uf.find(c.a));
            stampG(i, i, g);
            stampG(j, j, g);
            stampG(i, j, -g);
            stampG(j, i, -g);
          } else if (c.type === 'vgnd') {
            // real load regulation up to a real output current limit: below
            // the limit this is a stiff low-impedance buffer (VGND_RINT);
            // at/beyond it, the real part just can't supply more current,
            // so it stamps as a fixed current source instead -- the same
            // "which real regime are we in" fixed-point decision as a
            // diode/MOSFET on/off state, just choosing between a resistor
            // and a current source instead of on/off.
            const i = gi(uf.find(vgndInternal(c)));
            const j = gi(uf.find(c.out));
            if (this._vgndLimited.get(c.id)) {
              const dir = this._vgndLimitDir.get(c.id) || 1;
              stampI(j, dir * VGND_MAX_CURRENT);
              stampI(i, -dir * VGND_MAX_CURRENT);
            } else {
              const g = 1 / VGND_RINT;
              stampG(i, i, g);
              stampG(j, j, g);
              stampG(i, j, -g);
              stampG(j, i, -g);
            }
            // real output-pin protection: "out" physically cannot swing
            // past its own supply rails by more than a real clamp-diode
            // drop, no matter what the current-limited path above would
            // otherwise imply into a weak external load. A rail splitter's
            // two supply pins have a fixed real role -- "a" is always the
            // higher/positive rail, "b" the lower/ground rail (exactly
            // like this component is wired everywhere in this codebase,
            // matching a real part's labeled V+/GND pins) -- so only 2
            // directional clamps are needed, not 4: out can't rise above
            // "a", and can't fall below "b". Under normal (non-limited)
            // operation, out sits between the rails and neither conducts;
            // they only matter once something is pushing "out" toward or
            // past a rail.
            {
              const ia = gi(uf.find(c.a));
              const ib = gi(uf.find(c.b));
              const key = c.id;
              stampClampDiode(j, ia, this._railClampState.get(key + ':hi') || false, RAIL_CLAMP_VF, RAIL_CLAMP_RON);
              stampClampDiode(ib, j, this._railClampState.get(key + ':lo') || false, RAIL_CLAMP_VF, RAIL_CLAMP_RON);
            }
          } else if (c.type === 'acsource') {
            const g = 1 / AC_RINT;
            const i = gi(uf.find(acInternal(c)));
            const j = gi(uf.find(c.a));
            stampG(i, i, g);
            stampG(j, j, g);
            stampG(i, j, -g);
            stampG(j, i, -g);
          } else if (c.type === 'mtjsensor') {
            const g = 1 / MTJ_RINT;
            const iS = gi(uf.find(mtjSinInternal(c)));
            const jS = gi(uf.find(c.sin));
            stampG(iS, iS, g);
            stampG(jS, jS, g);
            stampG(iS, jS, -g);
            stampG(jS, iS, -g);
            const iC = gi(uf.find(mtjCosInternal(c)));
            const jC = gi(uf.find(c.cos));
            stampG(iC, iC, g);
            stampG(jC, jC, g);
            stampG(iC, jC, -g);
            stampG(jC, iC, -g);
          }
        });

        batteries.forEach((bat, k) => {
          const row = nNodes + k;
          const p = gi(uf.find(batInternal(bat)));
          const m = gi(uf.find(bat.b));
          if (p >= 0) {
            A[p][row] += 1;
            A[row][p] += 1;
          }
          if (m >= 0) {
            A[m][row] -= 1;
            A[row][m] -= 1;
          }
          b[row] += effectiveSourceValue(bat);
        });

        // rail-splitter constraint: V(internal) = 0.5*(V(a) + V(b)), an
        // ideal buffer forcing its own node to the midpoint of the two
        // rails it reads — same extra-unknown technique as a battery, just
        // a different equation on the source row.
        vgnds.forEach((v, k) => {
          const row = nNodes + nSrc + k;
          const iInt = gi(uf.find(vgndInternal(v)));
          const iA = gi(uf.find(v.a));
          const iB = gi(uf.find(v.b));
          if (iInt >= 0) {
            A[iInt][row] += 1;
            A[row][iInt] += 1;
          }
          if (iA >= 0) {
            A[iA][row] -= 0.5;
            A[row][iA] -= 0.5;
          }
          if (iB >= 0) {
            A[iB][row] -= 0.5;
            A[row][iB] -= 0.5;
          }
        });

        // inductor: dual of the capacitor's backward-Euler model. Its own
        // current is a state variable (can't be read off node voltages
        // alone), so it gets an extra branch-current unknown like an ideal
        // source: V(a) - V(b) - R*iL - (L/dt)*iL = -(L/dt)*iL_prev. The
        // real winding DCR just adds straight into that same coefficient
        // -- an inductor's coil is a resistor and an inductor in series,
        // and backward-Euler already treats L as a resistance (L/dt) plus
        // a series source, so R and L/dt simply add.
        inductors.forEach((ind, k) => {
          const row = rowInd(k);
          const Ldt = Math.max(ind.value, 1e-9) / Math.max(dt, 1e-6);
          const dcr = inductorDCR(ind.value);
          const iPrev = this._indState.get(ind.id) || 0;
          const ia = gi(uf.find(ind.a));
          const ib = gi(uf.find(ind.b));
          if (ia >= 0) {
            A[ia][row] += 1;
            A[row][ia] += 1;
          }
          if (ib >= 0) {
            A[ib][row] -= 1;
            A[row][ib] -= 1;
          }
          A[row][row] -= (Ldt + dcr);
          b[row] += -Ldt * iPrev;
        });

        // Ferrite toroid: N windings sharing one core. Each winding is a
        // backward-Euler branch like a plain inductor, but its equation now
        // includes every OTHER winding's discretized current too (mutual
        // inductance -- the standard SPICE "K" coupling generalized to
        // transient), plus its own real DC winding resistance:
        //   V(a_i)-V(b_i) - R_i*i_i - sum_j(L_ij/dt)*i_j = -sum_j(L_ij/dt)*iPrev_j
        // L_ii is the winding's own self-inductance; L_ij (i != j) is the
        // mutual inductance k*sqrt(L_i*L_j) from sharing the same core.
        toroids.forEach((tor, tk) => {
          const n = tor.windings.length;
          const dtSafe = Math.max(dt, 1e-6);
          const prev = this._toroidState.get(tor.id) || new Array(n).fill(0);
          const k = tor.coupling || 0;
          const Lself = tor.windings.map((w) => Math.max(w.L, 1e-12));
          for (let i = 0; i < n; i++) {
            const row = rowToroid(tk, i);
            const w = tor.windings[i];
            const ia = gi(uf.find(w.a));
            const ib = gi(uf.find(w.b));
            if (ia >= 0) {
              A[ia][row] += 1;
              A[row][ia] += 1;
            }
            if (ib >= 0) {
              A[ib][row] -= 1;
              A[row][ib] -= 1;
            }
            A[row][row] -= w.R || 0;
            let rhs = 0;
            for (let j = 0; j < n; j++) {
              const Lij = i === j ? Lself[i] : k * Math.sqrt(Lself[i] * Lself[j]);
              const Ldt2 = Lij / dtSafe;
              A[row][rowToroid(tk, j)] -= Ldt2;
              rhs += -Ldt2 * (prev[j] || 0);
            }
            b[row] += rhs;
          }
        });

        // Square-loop memory core: like a toroid winding (own DC resistance,
        // extra branch-current unknown), but the induced voltage comes from
        // the CORE's changing magnetization (Faraday's law, V = N*dPhi/dt)
        // instead of from this winding's own dI/dt -- every winding on the
        // core sees the SAME dB/dt, scaled by its own turns, because they
        // share one physical flux. dB/dt here is measured against this
        // frame's fixed starting B (coreBStart), using the fixed-point
        // loop's current best guess of where B will end up (coreB) -- see
        // the coreB/coreBStart setup above for why that's correctly one
        // real dt of physics, not several.
        memoryCores.forEach((mc, mck) => {
          const dtSafe = Math.max(dt, 1e-6);
          const bStart = coreBStart.get(mc.id);
          const bNow = coreB.get(mc.id);
          const dBdt = (bNow - bStart) / dtSafe;
          mc.windings.forEach((w, wi) => {
            const row = rowMemCore(mck, wi);
            const ia = gi(uf.find(w.a));
            const ib = gi(uf.find(w.b));
            if (ia >= 0) {
              A[ia][row] += 1;
              A[row][ia] += 1;
            }
            if (ib >= 0) {
              A[ib][row] -= 1;
              A[row][ib] -= 1;
            }
            A[row][row] -= w.R || 0;
            const Vind = (w.N || 0) * (mc.phiSat || 0) * dBdt;
            b[row] += Vind;
          });
        });

        // AC source: an ideal source like a battery, but its target value is
        // the shared sim clock's sinusoid instead of a constant.
        acsources.forEach((ac, k) => {
          const row = rowAc(k);
          const p = gi(uf.find(acInternal(ac)));
          const m = gi(uf.find(ac.b));
          if (p >= 0) {
            A[p][row] += 1;
            A[row][p] += 1;
          }
          if (m >= 0) {
            A[m][row] -= 1;
            A[row][m] -= 1;
          }
          b[row] += wave(ac.value, ac.freq || 1, ac.phase || 0, t);
        });

        // MTJ angle sensor: two ideal sources sharing one rotating clock,
        // 90 degrees apart, both referenced to the sensor's "ref" pin --
        // the sin(theta)/cos(theta) quadrature pair a real MTJ/TMR
        // angle-sensor IC's analog outputs present.
        mtjsensors.forEach((sensor, k) => {
          const rowS = rowMtjSin(k);
          const rowC = rowMtjCos(k);
          const ref = gi(uf.find(sensor.ref));
          const pS = gi(uf.find(mtjSinInternal(sensor)));
          const pC = gi(uf.find(mtjCosInternal(sensor)));
          if (pS >= 0) {
            A[pS][rowS] += 1;
            A[rowS][pS] += 1;
          }
          if (ref >= 0) {
            A[ref][rowS] -= 1;
            A[rowS][ref] -= 1;
          }
          b[rowS] += wave(sensor.value, sensor.freq || 1, sensor.phase || 0, t);

          if (pC >= 0) {
            A[pC][rowC] += 1;
            A[rowC][pC] += 1;
          }
          if (ref >= 0) {
            A[ref][rowC] -= 1;
            A[rowC][ref] -= 1;
          }
          b[rowC] += wave(sensor.value, sensor.freq || 1, (sensor.phase || 0) + 90, t);
        });

        xSol = size ? solveLinear(A, b) : [];
        voltages = new Map();
        for (const r of roots) voltages.set(r, r === groundRoot ? 0 : xSol[nodeIndex.get(r)]);

        let changed = false;
        // same on/off ideal-diode fixed-point decision as the LED/diode
        // and MOSFET body-diode blocks below, reused for the vgnd/
        // comparator rail-clamp paths: turn on once the real forward
        // voltage is exceeded, turn off once the clamp's own computed
        // current would go negative (load eased, rail no longer pinned).
        const updateClampDiode = (key, anodeV, cathodeV, vf, ron) => {
          const vd = (anodeV || 0) - (cathodeV || 0);
          const wasOn = this._railClampState.get(key) || false;
          if (!wasOn && vd > vf) {
            this._railClampState.set(key, true);
            changed = true;
          } else if (wasOn) {
            const i = (vd - vf) / ron;
            if (i < 0) {
              this._railClampState.set(key, false);
              changed = true;
            }
          }
        };
        diodes.forEach((d) => {
          const va = voltages.get(uf.find(d.a));
          const vb = voltages.get(uf.find(d.b));
          const vd = va - vb;
          const vf = forwardVoltage(d);
          const wasOn = this._ledState.get(d.id);
          if (!wasOn && vd > vf) {
            this._ledState.set(d.id, true);
            changed = true;
          } else if (wasOn) {
            const i = (vd - vf) / forwardRon(d);
            if (i < 0) {
              this._ledState.set(d.id, false);
              changed = true;
            }
          }
        });

        mosfets.forEach((f) => {
          const spec = mosfetSpec(f);
          const vg = voltages.get(uf.find(f.gate));
          const vs = voltages.get(uf.find(f.source));
          const vd = voltages.get(uf.find(f.drain));
          const vgs = vg - vs;
          const channelShouldBeOn = f.type === 'nmos' ? vgs > spec.vth : vgs < spec.vth;
          if (channelShouldBeOn !== this._fetChannelState.get(f.id)) {
            this._fetChannelState.set(f.id, channelShouldBeOn);
            changed = true;
          }

          // body diode: same on/off fixed-point iteration as the LED/diode
          // model above, just with the anode/cathode assignment swapped per
          // channel type (see the stamping comment above).
          const anodeV = f.type === 'nmos' ? vs : vd;
          const cathodeV = f.type === 'nmos' ? vd : vs;
          const vDiode = anodeV - cathodeV;
          const wasOn = this._fetDiodeState.get(f.id);
          if (!wasOn && vDiode > DIODE_VF) {
            this._fetDiodeState.set(f.id, true);
            changed = true;
          } else if (wasOn) {
            const i = (vDiode - DIODE_VF) / DIODE_RON;
            if (i < 0) {
              this._fetDiodeState.set(f.id, false);
              changed = true;
            }
          }
        });

        comparators.forEach((cp) => {
          // output current limit first, using the LATCHED state exactly as
          // it was stamped for the solve we just ran -- same on/off-style
          // fixed-point decision as the vgnd rail above: while un-limited,
          // check whether the low-impedance outputRon path this iteration
          // just solved would actually demand more current than the real
          // push-pull stage can source/sink; while limited, check whether
          // the load has eased enough that outputRon would stay within the
          // rating. This must run BEFORE the propagation-delay block below
          // changes _compState for next iteration -- checking against a
          // target that doesn't match what was actually stamped this solve
          // would compare an old vOut to a new rail and read a huge fake
          // overcurrent that was never really demanded of the part.
          [['1', cp.out1], ['2', cp.out2]].forEach(([ch, outPin]) => {
            const key = cp.id + ':' + ch;
            const vccV = voltages.get(uf.find(cp.vcc));
            const gndV = voltages.get(uf.find(cp.gnd));
            const vOut = voltages.get(uf.find(outPin));
            const targetV = this._compState.get(key) ? (vccV || 0) : (gndV || 0);
            const iIfNormal = (targetV - (vOut || 0)) / COMPARATOR_SPEC.outputRon;
            const limited = this._compOutLimited.get(key);
            if (!limited && Math.abs(iIfNormal) > COMPARATOR_SPEC.outputMaxCurrent) {
              this._compOutLimited.set(key, true);
              this._compOutLimitDir.set(key, iIfNormal >= 0 ? 1 : -1);
              changed = true;
            } else if (limited && Math.abs(iIfNormal) <= COMPARATOR_SPEC.outputMaxCurrent) {
              this._compOutLimited.set(key, false);
              changed = true;
            }
            updateClampDiode(key + ':hi', vOut, vccV, COMPARATOR_SPEC.clampVf, RAIL_CLAMP_RON);
            updateClampDiode(key + ':lo', gndV, vOut, COMPARATOR_SPEC.clampVf, RAIL_CLAMP_RON);
          });

          // real input offset voltage: the decision is Vin+ - Vin- > Vos,
          // not a perfectly ideal zero-offset comparison -- a real part
          // with a few mV of built-in imbalance, same honesty as the
          // MOSFET's real Vth instead of an ideal zero-threshold switch.
          [['1', cp.in1p, cp.in1m], ['2', cp.in2p, cp.in2m]].forEach(([ch, inP, inM]) => {
            const vp = voltages.get(uf.find(inP));
            const vm = voltages.get(uf.find(inM));
            const shouldBeHigh = (vp || 0) - (vm || 0) > COMPARATOR_SPEC.vosTyp;
            const key = cp.id + ':' + ch;
            if (shouldBeHigh !== this._compDesired.get(key)) {
              this._compDesired.set(key, shouldBeHigh);
              // see the fresh-init comment above: "since t-dt", not "since
              // t" -- otherwise a change detected mid-step would always
              // read 0 elapsed time against itself in this same solve()
              // call and cost a whole extra step no matter how small the
              // real propDelay is relative to dt
              this._compDesiredSince.set(key, t - dt);
            }
            // the real output only actually flips propDelay after the
            // real input comparison changed -- at typical frame dt this
            // resolves within the same frame (t doesn't advance again
            // until the next solve()), but a small enough dt genuinely
            // spans multiple frames before the output catches up, exactly
            // like a real bench measurement would show.
            const since = this._compDesiredSince.get(key) ?? t;
            if (shouldBeHigh !== this._compState.get(key) && t - since >= COMPARATOR_SPEC.propDelay) {
              this._compState.set(key, shouldBeHigh);
              changed = true;
            }
          });
        });

        hbridges.forEach((hb) => {
          const spec = hbridgeSpec(hb);
          // real logic-level input decision (a comparison against a real
          // threshold, not an idealized digital 0/1) selects the real
          // 4-state truth table this part class actually implements.
          const v1 = voltages.get(uf.find(hb.in1));
          const v2 = voltages.get(uf.find(hb.in2));
          const in1High = (v1 || 0) > spec.inputThreshold;
          const in2High = (v2 || 0) > spec.inputThreshold;
          // real undervoltage lockout: below its minimum motor supply, the
          // part genuinely cannot drive its outputs -- folded into the
          // same tracked, "changed"-participating decision as the mode
          // itself (not a raw same-iteration voltage read at stamp time,
          // which would see stale/empty voltages on a fixed-point loop's
          // first pass with no way to signal a retry once real ones exist)
          const vmNow = voltages.get(uf.find(hb.vm));
          const belowUvlo = (vmNow || 0) < spec.vmMin;
          const desired = belowUvlo ? 'coast' : in1High && in2High ? 'brake' : in1High ? 'forward' : in2High ? 'reverse' : 'coast';
          if (desired !== this._hbridgeDesired.get(hb.id)) {
            this._hbridgeDesired.set(hb.id, desired);
            // "since t-dt", not "since t" -- same reasoning as the
            // comparator's propagation-delay fix above
            this._hbridgeDesiredSince.set(hb.id, t - dt);
          }
          const since = this._hbridgeDesiredSince.get(hb.id) ?? t;
          if (desired !== this._hbridgeMode.get(hb.id) && t - since >= spec.propDelay) {
            this._hbridgeMode.set(hb.id, desired);
            changed = true;
          }

          // real body-diode flyback paths: same on/off ideal-diode
          // fixed-point decision as a MOSFET's body diode, independent of
          // whatever the FET-path decision above is doing, since a real
          // diode conducts whenever it's forward biased regardless of
          // gate state.
          const vmV = voltages.get(uf.find(hb.vm));
          const gndV = voltages.get(uf.find(hb.gnd));
          [['out1', hb.out1], ['out2', hb.out2]].forEach(([tag, outPin]) => {
            const vOut = voltages.get(uf.find(outPin));
            updateClampDiode(hb.id + ':' + tag + ':hi', vOut, vmV, spec.bodyDiodeVf, spec.bodyDiodeRon);
            updateClampDiode(hb.id + ':' + tag + ':lo', gndV, vOut, spec.bodyDiodeVf, spec.bodyDiodeRon);
          });
        });

        schmitts.forEach((sg) => {
          const spec = schmittSpec(sg);
          const vcc = voltages.get(uf.find(sg.vcc)) || 0;
          const vIn = voltages.get(uf.find(sg.in));
          const vtPlus = spec.vtPlusFrac * vcc;
          const vtMinus = spec.vtMinusFrac * vcc;
          // the real hysteretic input-side decision -- an internal analog
          // comparator with two thresholds, not delayed itself (the delay
          // belongs to the OUTPUT stage below); holds its prior decision
          // anywhere between the two thresholds, exactly what gives a
          // noisy signal real chatter immunity.
          let inputHigh = this._schmittInputHigh.get(sg.id) || false;
          if ((vIn || 0) > vtPlus) inputHigh = true;
          else if ((vIn || 0) < vtMinus) inputHigh = false;
          if (inputHigh !== this._schmittInputHigh.get(sg.id)) {
            this._schmittInputHigh.set(sg.id, inputHigh);
            changed = true;
          }
          const desiredOutHigh = !inputHigh; // inverter
          if (desiredOutHigh !== this._schmittDesired.get(sg.id)) {
            this._schmittDesired.set(sg.id, desiredOutHigh);
            this._schmittDesiredSince.set(sg.id, t - dt);
          }
          const since = this._schmittDesiredSince.get(sg.id) ?? t;
          if (desiredOutHigh !== this._schmittState.get(sg.id) && t - since >= spec.propDelay) {
            this._schmittState.set(sg.id, desiredOutHigh);
            changed = true;
          }
          const vOut = voltages.get(uf.find(sg.out));
          const gndV = voltages.get(uf.find(sg.gnd));
          updateClampDiode(sg.id + ':hi', vOut, vcc, spec.clampVf, RAIL_CLAMP_RON);
          updateClampDiode(sg.id + ':lo', gndV, vOut, spec.clampVf, RAIL_CLAMP_RON);
        });

        vgnds.forEach((v) => {
          // same on/off-style fixed-point decision as a diode: while
          // un-limited, check whether the low-impedance path this
          // iteration just solved would actually demand more current than
          // the real part can supply; while limited, check whether the
          // load has lightened enough that the low-impedance path would
          // now stay within the real rating.
          const vInt = voltages.get(uf.find(vgndInternal(v)));
          const vOut = voltages.get(uf.find(v.out));
          const iIfNormal = ((vInt || 0) - (vOut || 0)) / VGND_RINT;
          const limited = this._vgndLimited.get(v.id);
          if (!limited && Math.abs(iIfNormal) > VGND_MAX_CURRENT) {
            this._vgndLimited.set(v.id, true);
            this._vgndLimitDir.set(v.id, iIfNormal >= 0 ? 1 : -1);
            changed = true;
          } else if (limited && Math.abs(iIfNormal) <= VGND_MAX_CURRENT) {
            this._vgndLimited.set(v.id, false);
            changed = true;
          }
          const vA = voltages.get(uf.find(v.a));
          const vB = voltages.get(uf.find(v.b));
          updateClampDiode(v.id + ':hi', vOut, vA, RAIL_CLAMP_VF, RAIL_CLAMP_RON);
          updateClampDiode(v.id + ':lo', vB, vOut, RAIL_CLAMP_VF, RAIL_CLAMP_RON);
        });

        memoryCores.forEach((mc, mck) => {
          // net ampere-turns driving this core: every winding contributes
          // turns*current, exactly like a real multi-winding core (this is
          // also the ENTIRE mechanism behind group memory and toward/away
          // neighbor coupling -- there is no separate scripted logic for
          // those; they are just more windings, wired by the user, adding
          // their own real ampere-turns to this same sum)
          let netAT = 0;
          mc.windings.forEach((w, wi) => {
            netAT += (w.N || 0) * (xSol[rowMemCore(mck, wi)] || 0);
          });
          const bStart = coreBStart.get(mc.id);
          const hc = mc.hcAmpTurns > 0 ? mc.hcAmpTurns : 1;
          let target;
          if (netAT > hc) target = 1;
          else if (netAT < -hc) target = -1;
          // below the coercive threshold the core is not being driven at
          // all -- real remanence means it stays exactly where it was,
          // not "spring back toward zero"
          else target = bStart;
          const tau = mc.switchTau > 0 ? mc.switchTau : 1e-3;
          const k = Math.max(dt, 1e-6) / tau;
          let bTarget = (bStart + k * target) / (1 + k);
          bTarget = Math.max(-1, Math.min(1, bTarget));
          // under-relaxed update: a real, fast flip induces a real back-EMF
          // (Lenz's law) that fights the very current causing the flip --
          // jumping straight to bTarget each inner iteration lets that
          // feedback oscillate forever (drive current flips B -> induced
          // back-EMF chokes the drive current -> B un-flips -> back-EMF
          // vanishes -> drive current returns -> repeat) instead of settling
          // on the correct self-consistent answer for this one real dt. Move
          // only partway toward bTarget per iteration -- same technique
          // SPICE-class solvers use for damped Newton convergence -- so the
          // fixed point this converges to is unchanged (at true convergence
          // bTarget already equals the current guess, damping or not), it
          // just gets there without ringing.
          const bOld = coreB.get(mc.id);
          const bNew = bOld + 0.25 * (bTarget - bOld);
          if (Math.abs(bNew - bOld) > 1e-7) {
            coreB.set(mc.id, bNew);
            changed = true;
          }
        });

        if (!changed) break;
      }

      const currents = new Map();
      const warnings = [];

      const indCurrent = new Map();
      inductors.forEach((ind, k) => {
        const I = xSol[rowInd(k)] || 0;
        indCurrent.set(ind.id, I);
        this._indState.set(ind.id, I);
      });
      const acCurrent = new Map();
      acsources.forEach((ac, k) => acCurrent.set(ac.id, -(xSol[rowAc(k)] || 0)));

      // toroid windings: report each winding's own current under
      // "<toroidId>:<windingIndex>" (voltages need no special handling --
      // winding terminals are ordinary cellIds already in the voltages map)
      const toroidCurrent = new Map();
      toroids.forEach((tor, tk) => {
        const arr = tor.windings.map((w, wi) => xSol[rowToroid(tk, wi)] || 0);
        this._toroidState.set(tor.id, arr);
        arr.forEach((I, wi) => toroidCurrent.set(tor.id + ':' + wi, I));
        toroidCurrent.set(tor.id, arr[0] || 0);
      });

      // memory-core windings: report each winding's own current, same
      // "<coreId>:<windingIndex>" convention as the toroid, and commit this
      // frame's converged B back into persisted state -- this IS the DC
      // memory: nothing clears it except an explicit circuit reset (a fresh
      // board), never the fixed-point iteration or the windings' current
      // going to zero.
      const memCoreCurrent = new Map();
      memoryCores.forEach((mc, mck) => {
        const arr = mc.windings.map((w, wi) => xSol[rowMemCore(mck, wi)] || 0);
        arr.forEach((I, wi) => memCoreCurrent.set(mc.id + ':' + wi, I));
        memCoreCurrent.set(mc.id, arr[0] || 0);
        this._coreState.set(mc.id, coreB.get(mc.id));
      });

      components.forEach((c) => {
        const va = voltages.get(uf.find(c.a));
        const vb = voltages.get(uf.find(c.b));
        let I = 0;
        if (c.type === 'resistor') {
          I = (va - vb) / c.value;
          const p = I * I * c.value;
          if (p > 0.25) warnings.push(`Resistor ${c.label || c.id}: ${p.toFixed(2)} W — exceeds a typical 1/4W resistor's rating`);
        } else if (c.type === 'led' || c.type === 'diode') {
          const on = this._ledState.get(c.id);
          I = on ? (va - vb - forwardVoltage(c)) / forwardRon(c) : 0;
          if (c.type === 'led' && I > 0.03) warnings.push(`LED ${c.label || c.id}: ${(I * 1000).toFixed(0)} mA — add a current-limiting resistor`);
          if (c.type === 'diode' && I > 1.0) warnings.push(`Diode ${c.label || c.id}: ${I.toFixed(2)} A — exceeds a typical small rectifier's rating`);
        } else if (c.type === 'capacitor') {
          // vPrev is the ideal-C-only voltage from last frame (see the
          // stamping comment above); the branch current is whatever the
          // solved terminal voltage and that companion source imply...
          const esr = capacitorESR(c);
          const gC = 1 / (esr + Math.max(dt, 1e-6) / c.value);
          const gLeak = 1 / capacitorLeakageR(c);
          const vPrev = this._capState.get(c.id) || 0;
          const capBranchI = gC * ((va - vb) - vPrev);
          const leakI = gLeak * (va - vb);
          I = capBranchI + leakI; // total current the part draws, ESR branch + leakage, same convention as every other component's a->b current
          // ...and THAT current is what actually charges the ideal C this
          // frame (real ESR drops some of (va-vb) across itself first;
          // only the current through the ideal-C branch moves its charge)
          this._capState.set(c.id, vPrev + (capBranchI * Math.max(dt, 1e-6)) / c.value);
          // an electrolytic (value >= ELECTROLYTIC_THRESHOLD) is a real
          // polarized part -- terminals[0]/"a" is the "+" lead by the same
          // convention as the LED/diode anode. Real electrolytics tolerate
          // only a small reverse voltage before the dielectric breaks down
          // (vents, sometimes violently); a ceramic disc below the
          // threshold has no polarity at all and never warns.
          if (c.value >= ELECTROLYTIC_THRESHOLD && va - vb < -REVERSE_POLARITY_LIMIT) {
            warnings.push(`Electrolytic capacitor ${c.label || c.id}: reverse-biased by ${(vb - va).toFixed(2)}V -- exceeds a typical electrolytic's reverse-voltage rating and can vent or fail`);
          }
          // real ESR self-heating: a small ESR times a real ripple/charge
          // current is genuine dissipated power, exactly the mechanism
          // that limits how much current a real electrolytic can actually
          // deliver (this is why Cal F/G/H-style low-impedance writes into
          // a hold cap are a real design tradeoff, not a free lunch)
          const capP = capBranchI * capBranchI * esr;
          if (capP > 0.1) {
            warnings.push(`Capacitor ${c.label || c.id}: ${capP.toFixed(2)} W in its own ESR (${(esr * 1000).toFixed(1)}mΩ) -- real self-heating, check the part's ripple-current rating`);
          }
        } else if (c.type === 'potentiometer') {
          I = 0;
        } else if (c.type === 'switch' || c.type === 'pushbutton') {
          I = 0;
        } else if (c.type === 'vgnd') {
          // the real output current the buffer is actually sourcing/
          // sinking into "out" -- exactly VGND_MAX_CURRENT once real load
          // regulation has broken down, not whatever Ohm's law over
          // VGND_RINT would otherwise imply
          const vInt = voltages.get(uf.find(vgndInternal(c)));
          const vOut = voltages.get(uf.find(c.out));
          I = this._vgndLimited.get(c.id)
            ? (this._vgndLimitDir.get(c.id) || 1) * VGND_MAX_CURRENT
            : ((vInt || 0) - (vOut || 0)) / VGND_RINT;
          if (this._vgndLimited.get(c.id)) {
            warnings.push(`Virtual Ground ${c.label || c.id}: current-limited at ${(VGND_MAX_CURRENT * 1000).toFixed(0)}mA -- can no longer hold V0 under this load, a real load-regulation limit`);
          }
        } else if (c.type === 'inductor') {
          I = indCurrent.get(c.id) || 0;
          const dcrP = I * I * inductorDCR(c.value);
          if (dcrP > 0.25) warnings.push(`Inductor ${c.label || c.id}: ${dcrP.toFixed(2)} W in its real winding resistance -- exceeds a typical small inductor's rating`);
        } else if (c.type === 'acsource') {
          I = acCurrent.get(c.id) || 0;
        } else if (c.type === 'mtjsensor') {
          I = 0;
        } else if (c.type === 'toroid') {
          I = toroidCurrent.get(c.id) || 0;
        } else if (c.type === 'nmos' || c.type === 'pmos') {
          const spec = mosfetSpec(c);
          const vg = voltages.get(uf.find(c.gate));
          const vs = voltages.get(uf.find(c.source));
          const vd = voltages.get(uf.find(c.drain));
          // total conventional current from drain to source: the channel
          // (when on) and the body diode (when on) are two parallel paths
          // between the same two nodes, so their currents just add.
          I = this._fetChannelState.get(c.id) ? (vd - vs) / spec.rdsOn : 0;
          if (this._fetDiodeState.get(c.id)) {
            const anodeV = c.type === 'nmos' ? vs : vd;
            const cathodeV = c.type === 'nmos' ? vd : vs;
            const diodeI = (anodeV - cathodeV - DIODE_VF) / DIODE_RON; // anode->cathode
            I += c.type === 'nmos' ? -diodeI : diodeI; // convert to the drain->source convention
          }
          const vgs = vg - vs;
          const vds = vd - vs;
          // commit this frame's converged gate charge (no ESR here, so the
          // ideal-C voltage is just the solved terminal Vgs directly, no
          // branch-current back-out needed like the real capacitor's ESR
          // case above)
          this._fetGateV.set(c.id, vgs);
          if (Math.abs(vgs) > spec.vgsMax) {
            warnings.push(`${c.type.toUpperCase()} ${c.label || c.id}: |Vgs|=${Math.abs(vgs).toFixed(2)}V exceeds its ${spec.vgsMax}V gate rating`);
          }
          if (Math.abs(vds) > spec.vdsMax) {
            warnings.push(`${c.type.toUpperCase()} ${c.label || c.id}: |Vds|=${Math.abs(vds).toFixed(2)}V exceeds its ${spec.vdsMax}V drain-source rating`);
          }
          if ((touchCount.get(uf.find(c.gate)) || 0) <= 1) {
            warnings.push(`${c.type.toUpperCase()} ${c.label || c.id}: gate is not wired to anything -- a floating gate picks up noise and can turn the switch on/off unpredictably`);
          }
        } else if (c.type === 'memorycore') {
          I = memCoreCurrent.get(c.id) || 0;
        } else if (c.type === 'latchrelay') {
          // the coil's own current (its magnetic dynamics are stamped by
          // the shared memoryCores block) is reported separately from the
          // real mechanical contact's current, since they're electrically
          // two entirely different circuits joined only by the armature
          currents.set(c.id + ':coil', memCoreCurrent.get(c.id) || 0);
          const vA = voltages.get(uf.find(c.contactA));
          const vB = voltages.get(uf.find(c.contactB));
          I = ((vA || 0) - (vB || 0)) / latchContactResistance(c);
          const spec = latchRelaySpec(c);
          const contactP = I * I * latchContactResistance(c);
          if (contactP > 0.1) warnings.push(`${c.label || c.id} (latching relay): contact dissipating ${contactP.toFixed(2)} W -- exceeds a typical small signal relay's real contact rating`);
          const coilI = memCoreCurrent.get(c.id) || 0;
          const coilP = coilI * coilI * (spec.coilR || 0);
          if (coilP > 0.5) warnings.push(`${c.label || c.id} (latching relay): coil dissipating ${coilP.toFixed(2)} W -- real continuous coil heating exceeds a typical small relay's rating`);
        } else if (c.type === 'comparator') {
          // real limits, checked against the actual solved node voltages,
          // not assumed constants -- exactly like the MOSFET Vgs/Vds
          // warnings above. va/vb are meaningless for this component (it
          // has no plain a/b pins), so I is left at 0 and reported per
          // output channel below instead.
          const vVcc = voltages.get(uf.find(c.vcc));
          const vGnd = voltages.get(uf.find(c.gnd));
          const supplyV = (vVcc || 0) - (vGnd || 0);
          if ((touchCount.get(uf.find(c.vcc)) || 0) <= 1 || (touchCount.get(uf.find(c.gnd)) || 0) <= 1) {
            warnings.push(`${c.label || c.id} (TLV3202): VCC or GND is not wired to anything -- an unpowered comparator can't drive a real output`);
          } else if (supplyV < COMPARATOR_SPEC.vccMin) {
            warnings.push(`${c.label || c.id} (TLV3202): supply is ${supplyV.toFixed(2)}V -- below its ${COMPARATOR_SPEC.vccMin}V minimum operating voltage`);
          } else if (supplyV > COMPARATOR_SPEC.vccMax) {
            warnings.push(`${c.label || c.id} (TLV3202): supply is ${supplyV.toFixed(2)}V -- exceeds its ${COMPARATOR_SPEC.vccMax}V maximum rating`);
          }
          [['1', c.in1p, c.in1m], ['2', c.in2p, c.in2m]].forEach(([ch, inP, inM]) => {
            [['+', inP], ['-', inM]].forEach(([sign, pin]) => {
              const v = voltages.get(uf.find(pin));
              if (v == null) return;
              if (v > (vVcc || 0) + COMPARATOR_SPEC.cmRangeOver || v < (vGnd || 0) - COMPARATOR_SPEC.cmRangeOver) {
                warnings.push(`${c.label || c.id} (TLV3202) ch${ch} IN${sign}: ${v.toFixed(2)}V is outside the real common-mode input range -- the comparator's decision is not guaranteed valid here`);
              }
            });
          });
          // per-channel output current, "<id>:1"/"<id>:2" -- same convention
          // as the toroid/memory-core per-winding currents above
          [['1', c.out1], ['2', c.out2]].forEach(([ch, outPin]) => {
            const key = c.id + ':' + ch;
            const vOut = voltages.get(uf.find(outPin));
            const high = this._compState.get(key);
            const railV = high ? vVcc : vGnd;
            let Iout;
            if (this._compOutLimited.get(key)) {
              const dir = this._compOutLimitDir.get(key) || 1;
              Iout = -dir * COMPARATOR_SPEC.outputMaxCurrent;
              warnings.push(`${c.label || c.id} (TLV3202) ch${ch} OUT: output current-limited at its ${(COMPARATOR_SPEC.outputMaxCurrent * 1000).toFixed(1)}mA rating -- the real push-pull stage can't drive this load any harder`);
            } else {
              Iout = ((vOut || 0) - (railV || 0)) / COMPARATOR_SPEC.outputRon;
            }
            currents.set(key, Iout);
          });
        } else if (c.type === 'hbridge') {
          const spec = hbridgeSpec(c);
          const vmV = voltages.get(uf.find(c.vm)) || 0;
          const gndV = voltages.get(uf.find(c.gnd)) || 0;
          const supplyV = vmV - gndV;
          if ((touchCount.get(uf.find(c.vm)) || 0) <= 1 || (touchCount.get(uf.find(c.gnd)) || 0) <= 1) {
            warnings.push(`${c.label || c.id} (H-bridge): VM or GND is not wired to anything -- an unpowered bridge can't drive a real load`);
          } else if (supplyV < spec.vmMin) {
            warnings.push(`${c.label || c.id} (H-bridge): VM is ${supplyV.toFixed(2)}V -- below its ${spec.vmMin}V undervoltage lockout, outputs are forced to coast`);
          } else if (supplyV > spec.vmMax) {
            warnings.push(`${c.label || c.id} (H-bridge): VM is ${supplyV.toFixed(2)}V -- exceeds its ${spec.vmMax}V maximum rating`);
          }
          // per-output current, "<id>:out1"/"<id>:out2" -- the current
          // actually flowing INTO the load from each output pin (through
          // whichever real path, FET or flyback diode, is conducting)
          [['out1', c.out1], ['out2', c.out2]].forEach(([tag, outPin]) => {
            const vOut = voltages.get(uf.find(outPin)) || 0;
            const key = c.id + ':' + tag;
            const iToVm = (vmV - vOut) / spec.ronHS;
            const iToGnd = (vOut - gndV) / spec.ronLS;
            // whichever real path is actually the active one dominates;
            // report the FET-path current when that FET is on, otherwise
            // whatever the flyback diode is carrying
            const mode = this._hbridgeMode.get(c.id);
            const outNum = tag === 'out1' ? 1 : 2;
            const highOn = (mode === 'forward' && outNum === 1) || (mode === 'reverse' && outNum === 2);
            const lowOn = (mode === 'forward' && outNum === 2) || (mode === 'reverse' && outNum === 1) || mode === 'brake';
            const Iout = highOn ? iToVm : lowOn ? -iToGnd : (this._hbridgeDiodeState.get(key + ':hi') ? iToVm : this._hbridgeDiodeState.get(key + ':lo') ? -iToGnd : 0);
            if (Math.abs(Iout) > spec.currentLimit) {
              warnings.push(`${c.label || c.id} (H-bridge) ${tag}: ${(Iout * 1000).toFixed(0)}mA -- exceeds its ${(spec.currentLimit * 1000).toFixed(0)}mA real continuous current rating`);
            }
            currents.set(key, Iout);
          });
        } else if (c.type === 'schmitt') {
          const spec = schmittSpec(c);
          const vcc = voltages.get(uf.find(c.vcc));
          const gnd = voltages.get(uf.find(c.gnd));
          const supplyV = (vcc || 0) - (gnd || 0);
          if ((touchCount.get(uf.find(c.vcc)) || 0) <= 1 || (touchCount.get(uf.find(c.gnd)) || 0) <= 1) {
            warnings.push(`${c.label || c.id} (SN74HC14): VCC or GND is not wired to anything -- an unpowered gate can't drive a real output`);
          } else if (supplyV < spec.vccMin) {
            warnings.push(`${c.label || c.id} (SN74HC14): supply is ${supplyV.toFixed(2)}V -- below its ${spec.vccMin}V minimum operating voltage`);
          } else if (supplyV > spec.vccMax) {
            warnings.push(`${c.label || c.id} (SN74HC14): supply is ${supplyV.toFixed(2)}V -- exceeds its ${spec.vccMax}V maximum rating`);
          }
          const vOut = voltages.get(uf.find(c.out));
          const high = this._schmittState.get(c.id);
          const railV = high ? vcc : gnd;
          I = ((vOut || 0) - (railV || 0)) / spec.outputRon;
        }
        currents.set(c.id, I);
      });
      toroidCurrent.forEach((I, key) => currents.set(key, I));
      memCoreCurrent.forEach((I, key) => currents.set(key, I));
      // memCoreCurrent's generic pass above just overwrote each
      // latchrelay's plain id with its COIL current (since a latchrelay's
      // coil is folded into the same memoryCores bookkeeping) -- restore
      // the real mechanical contact current there instead; the coil's own
      // current stays separately available under "<id>:coil".
      latchrelays.forEach((lr) => {
        const vA = voltages.get(uf.find(lr.contactA));
        const vB = voltages.get(uf.find(lr.contactB));
        currents.set(lr.id, ((vA || 0) - (vB || 0)) / latchContactResistance(lr));
      });

      batteries.forEach((bat, k) => {
        // MNA's branch-current unknown is defined flowing p->m through the
        // source; negate so a positive value reads as "current the battery
        // is discharging into the external circuit", matching the a->b
        // convention used for every other component's current.
        const Isrc = -(xSol[nNodes + k] || 0);
        currents.set(bat.id, Isrc);
        if (Math.abs(Isrc) > 1.0) {
          warnings.push(`Short circuit at ${bat.label || bat.id}: ${Isrc.toFixed(2)} A — check your wiring`);
        }
      });

      // Two ideal-ish voltage sources wired directly across the same node
      // pair don't settle at a safe "averaged" voltage on a real bench --
      // they fight each other through whatever tiny internal resistance
      // each one has, and the loser sinks a large real current backward.
      // The solver above already reflects that real physics (a real,
      // non-singular MNA system, not a bug), but presenting the resulting
      // number without comment risks reading as a normal, safe operating
      // point. Call it out explicitly and specifically here, distinct from
      // the generic overcurrent warning above.
      for (let bi = 0; bi < batteries.length; bi++) {
        for (let bj = bi + 1; bj < batteries.length; bj++) {
          const b1 = batteries[bi];
          const b2 = batteries[bj];
          const a1 = uf.find(b1.a);
          const g1 = uf.find(b1.b);
          const a2 = uf.find(b2.a);
          const g2 = uf.find(b2.b);
          const sameOrientation = a1 === a2 && g1 === g2;
          const reversedOrientation = a1 === g2 && g1 === a2;
          if ((sameOrientation && b1.value !== b2.value) || reversedOrientation) {
            warnings.push(`Conflicting power supplies: ${b1.label || b1.id} (${b1.value}V) and ${b2.label || b2.id} (${b2.value}V) are wired directly across the same two nodes -- rejected as a valid operating point. A real bench would show these fighting each other (large circulating current, neither supply's voltage), not a safe averaged voltage. Add series resistance or remove one supply.`);
          }
        }
      }

      acsources.forEach((ac) => {
        const I = acCurrent.get(ac.id) || 0;
        if (Math.abs(I) > 1.0) {
          warnings.push(`Overload at ${ac.label || ac.id}: ${I.toFixed(2)} A — check your wiring`);
        }
      });

      // expose each MOSFET's actual on/off decisions directly, so the
      // Inspector (or a test) doesn't have to re-derive "is the channel on"
      // from raw currents/voltages itself -- these are read off the real
      // Vgs/Vth comparison and body-diode conduction computed above, not a
      // separately invented state
      const mosfetStates = new Map();
      mosfets.forEach((f) => mosfetStates.set(f.id, {
        channelOn: this._fetChannelState.get(f.id),
        bodyDiodeOn: this._fetDiodeState.get(f.id),
      }));

      // expose each memory core's actual remanent flux directly (the real
      // number the solver computed, in [-1, 1]) -- any Left/Right/Hold label
      // shown anywhere is derived FROM this after the fact, never the other
      // way around
      const coreStates = new Map();
      memoryCores.forEach((mc) => coreStates.set(mc.id, this._coreState.get(mc.id)));

      // a real flux probe reads real flux (Weber), not just the normalized
      // -1..1 remanence figure -- coreStates already IS a direct readout of
      // the solver's real internal state (never inferred from a terminal
      // voltage); this just also reports it in the physical unit its own
      // phiSat is specified in, since B_normalized * phiSat is real flux.
      const coreFlux = new Map();
      memoryCores.forEach((mc) => coreFlux.set(mc.id, this._coreState.get(mc.id) * (mc.phiSat || 0)));

      // command must never be silently equated with a successful physical
      // transition: requestedState is only "what the coil current says
      // right now", actualState is the real persisted remanence, and
      // transitioning/fault are both derived honestly from that real
      // state, never from whether a command was merely issued.
      const latchStates = new Map();
      latchrelays.forEach((lr) => {
        const spec = latchRelaySpec(lr);
        const coilI = memCoreCurrent.get(lr.id) || 0;
        const actual = this._coreState.get(lr.id) || 0;
        const driveThresh = spec.hcAmpTurns * 0.1;
        const requestedState = coilI > driveThresh ? 'set' : coilI < -driveThresh ? 'reset' : 'none';
        const transitioning = Math.abs(actual) < 0.95;
        latchStates.set(lr.id, {
          requestedState,
          actualState: actual >= 0 ? 'field' : 'void',
          actualB: actual,
          contactClosed: this._latchContactClosed.get(lr.id) || false,
          transitioning,
          // a real fault: still mid-transition with no drive present to
          // finish the job -- the pulse that was applied didn't carry
          // enough current/duration to complete the switch
          fault: transitioning && requestedState === 'none',
        });
      });

      // expose each comparator channel's actual HIGH/LOW decision directly
      // -- the real Vin+/Vin-/Vos comparison computed above, never a
      // separately invented state
      const comparatorStates = new Map();
      comparators.forEach((cp) => comparatorStates.set(cp.id, {
        out1High: this._compState.get(cp.id + ':1'),
        out2High: this._compState.get(cp.id + ':2'),
      }));

      // expose the real committed drive mode directly -- never inferred
      // from the IN1/IN2 command alone, since real propagation delay
      // means the outputs haven't necessarily caught up yet
      const hbridgeStates = new Map();
      hbridges.forEach((hb) => hbridgeStates.set(hb.id, { mode: this._hbridgeMode.get(hb.id) || 'coast' }));

      // expose the real latched (propagation-delayed) output decision
      // directly, plus the raw hysteretic input-side state for diagnosing
      // whether a noisy input is actually being held by hysteresis
      const schmittStates = new Map();
      schmitts.forEach((sg) => schmittStates.set(sg.id, {
        outHigh: this._schmittState.get(sg.id),
        inputHigh: this._schmittInputHigh.get(sg.id),
      }));

      return { voltages, currents, warnings, mosfetStates, coreStates, coreFlux, comparatorStates, latchStates, hbridgeStates, schmittStates, uf, groundRoot, hasCircuit: true };
    }
  }

  const api = {
    Circuit, UnionFind, solveLinear, LED_VF, LED_RON, DIODE_VF, DIODE_RON, BATTERY_RINT, VGND_RINT,
    AC_RINT, MTJ_RINT, NMOS_PARTS, PMOS_PARTS, mosfetSpec, COMPARATOR_SPEC,
    ELECTROLYTIC_THRESHOLD, REVERSE_POLARITY_LIMIT, capacitorESR, capacitorLeakageR, inductorDCR,
    COMPONENT_TOLERANCE, capacitorToleranceFor,
    LATCHRELAY_SPEC, latchRelaySpec,
    HBRIDGE_SPEC, hbridgeSpec,
    SCHMITT_SPEC, schmittSpec,
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window !== 'undefined') window.CircuitEngine = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
