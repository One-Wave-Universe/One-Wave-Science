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
  const VGND_RINT = 2; // ohms, output impedance of a rail-splitter / virtual-ground buffer (e.g. TLE2426-class)
  const AC_RINT = 1; // ohms, output impedance of an ideal AC/function-generator source
  const MTJ_RINT = 200; // ohms, buffered analog-output impedance of a real MTJ/TMR angle-sensor IC's sin/cos pins
  // LEGACY: the Ternary Cell is a higher-level macro (comparator + MOSFET
  // pair collapsed into one part with a built-in Hold/Pos/Neg state
  // machine). Keep it working for existing builds, but new example circuits
  // should use the discrete nmos/pmos parts below instead -- real switching
  // built from real transistors, not a pre-decided abstraction.
  const TERNARY_ON_R = 1; // ohms, a MOSFET switch pair's RDS(on) driving the active state (e.g. AO3400A-class)
  const TERNARY_HOLD_R = 100000; // ohms, ties the output back to the reference when neither path conducts (e.g. AO3400A-class)
  const TERNARY_DELTA_DEFAULT = 0.02; // volts, default +/- state displacement from the reference (matches a 20mV first-proof margin)
  const TERNARY_HYSTERESIS_FRAC = 0.15; // fraction of delta -- a real window comparator's hysteresis, sized so ordinary sensing noise can't repeatedly flip the decision right at a threshold

  // Discrete MOSFETs: real parts, real limits. "value" selects between two
  // real part classes rather than a made-up continuous parameter -- the
  // same idea as LED_VF picking a real forward-voltage family by color.
  // RDS(on) here is a fixed on-resistance once the channel is on (a
  // piecewise switch model), not a continuous Vgs-dependent square law --
  // sufficient for "does this switch turn on/off and clamp near its rail",
  // which is what a breadboard-level design needs to get right first.
  const NMOS_PARTS = {
    1.5: { name: 'AO3400A-class (logic-level)', vth: 1.5, rdsOn: 0.03, vgsMax: 12, vdsMax: 30 },
    2.1: { name: '2N7000-class', vth: 2.1, rdsOn: 5, vgsMax: 20, vdsMax: 60 },
  };
  const PMOS_PARTS = {
    1.5: { name: 'AO3401A-class (logic-level)', vth: -1.5, rdsOn: 0.05, vgsMax: 12, vdsMax: 30 },
    2.1: { name: 'BS250-class', vth: -2.1, rdsOn: 5, vgsMax: 20, vdsMax: 60 },
  };
  function mosfetSpec(c) {
    const table = c.type === 'pmos' ? PMOS_PARTS : NMOS_PARTS;
    return table[c.value] || table[1.5];
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
      this._ternaryState = new Map(); // ternary-cell id -> 'hold' | 'pos' | 'neg', persists across frames
      this._fetChannelState = new Map(); // mosfet id -> boolean (channel conducting)
      this._fetDiodeState = new Map(); // mosfet id -> boolean (body diode conducting)
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
        if (c.type === 'battery') uf.find(batInternal(c));
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
        if (c.type === 'ternarycell') { uf.find(c.ref); uf.find(c.sense); uf.find(c.out); }
        if (c.type === 'nmos' || c.type === 'pmos') { uf.find(c.gate); uf.find(c.drain); uf.find(c.source); }
      });

      const batteries = components.filter((c) => c.type === 'battery');
      const vgnds = components.filter((c) => c.type === 'vgnd');
      const inductors = components.filter((c) => c.type === 'inductor');
      const acsources = components.filter((c) => c.type === 'acsource');
      const mtjsensors = components.filter((c) => c.type === 'mtjsensor');
      const toroids = components.filter((c) => c.type === 'toroid');
      const ternaryCells = components.filter((c) => c.type === 'ternarycell');
      const mosfets = components.filter((c) => c.type === 'nmos' || c.type === 'pmos');

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
        if (c.type === 'battery') touch(batInternal(c));
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
        if (c.type === 'ternarycell') { touch(c.ref); touch(c.sense); touch(c.out); }
        if (c.type === 'nmos' || c.type === 'pmos') { touch(c.gate); touch(c.drain); touch(c.source); }
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
      const size = toroidRowBase + nToroidRows;

      const gi = (rt) => (rt === groundRoot ? -1 : nodeIndex.get(rt));

      const diodes = components.filter((c) => c.type === 'led' || c.type === 'diode');
      diodes.forEach((d) => {
        if (!this._ledState.has(d.id)) this._ledState.set(d.id, false);
      });
      ternaryCells.forEach((tc) => {
        // a cell with no prior history (just placed, or a fresh reset --
        // power just started) always begins in Hold, never mid-decision
        if (!this._ternaryState.has(tc.id)) this._ternaryState.set(tc.id, 'hold');
      });
      mosfets.forEach((f) => {
        // a fresh MOSFET (just placed, or a fresh reset -- power just
        // started) always begins fully off, same reasoning as the diode/LED
        // on/off state: don't presume a decision before ever solving
        if (!this._fetChannelState.has(f.id)) this._fetChannelState.set(f.id, false);
        if (!this._fetDiodeState.has(f.id)) this._fetDiodeState.set(f.id, false);
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
            const gC = c.value / Math.max(dt, 1e-6);
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
          } else if (c.type === 'ternarycell') {
            // a real window-comparator-driven MOSFET switch pair: exactly
            // one of {hold, +, -} is ever true at a time (it's one state
            // variable, not two independently-closeable switches), which by
            // construction makes the positive and negative paths mutually
            // exclusive -- there is no shoot-through state to reach.
            const state = this._ternaryState.get(c.id);
            const i = gi(uf.find(c.out));
            const j = gi(uf.find(c.ref));
            if (state === 'hold') {
              const g = 1 / TERNARY_HOLD_R;
              stampG(i, i, g);
              stampG(j, j, g);
              stampG(i, j, -g);
              stampG(j, i, -g);
            } else {
              const g = 1 / TERNARY_ON_R;
              const delta = c.value > 0 ? c.value : TERNARY_DELTA_DEFAULT;
              const sign = state === 'pos' ? 1 : -1;
              stampG(i, i, g);
              stampG(j, j, g);
              stampG(i, j, -g);
              stampG(j, i, -g);
              const Ieq = g * sign * delta;
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
          } else if (c.type === 'battery') {
            const g = 1 / BATTERY_RINT;
            const i = gi(uf.find(batInternal(c)));
            const j = gi(uf.find(c.a));
            stampG(i, i, g);
            stampG(j, j, g);
            stampG(i, j, -g);
            stampG(j, i, -g);
          } else if (c.type === 'vgnd') {
            const g = 1 / VGND_RINT;
            const i = gi(uf.find(vgndInternal(c)));
            const j = gi(uf.find(c.out));
            stampG(i, i, g);
            stampG(j, j, g);
            stampG(i, j, -g);
            stampG(j, i, -g);
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
          b[row] += bat.value;
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
        // source: V(a) - V(b) - (L/dt)*iL = -(L/dt)*iL_prev.
        inductors.forEach((ind, k) => {
          const row = rowInd(k);
          const Ldt = Math.max(ind.value, 1e-9) / Math.max(dt, 1e-6);
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
          A[row][row] -= Ldt;
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

        ternaryCells.forEach((tc) => {
          const vref = voltages.get(uf.find(tc.ref));
          const vsense = voltages.get(uf.find(tc.sense));
          const vd = vsense - vref;
          const delta = tc.value > 0 ? tc.value : TERNARY_DELTA_DEFAULT;
          const hyst = delta * TERNARY_HYSTERESIS_FRAC;
          const prev = this._ternaryState.get(tc.id);
          // a real window comparator's hysteresis: the crossing that ENTERS
          // a state sits at the nominal threshold, but the crossing that
          // LEAVES it is offset further out -- so a signal sitting exactly
          // at the boundary (sensing noise, most commonly) can't repeatedly
          // re-trigger the decision every iteration/frame
          let next = prev;
          if (prev === 'pos') {
            if (vd < delta - hyst) next = vd < -(delta - hyst) ? 'neg' : 'hold';
          } else if (prev === 'neg') {
            if (vd > -(delta - hyst)) next = vd > delta - hyst ? 'pos' : 'hold';
          } else {
            if (vd > delta) next = 'pos';
            else if (vd < -delta) next = 'neg';
          }
          if (next !== prev) {
            this._ternaryState.set(tc.id, next);
            changed = true;
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
          const vPrev = this._capState.get(c.id) || 0;
          I = (c.value * ((va - vb) - vPrev)) / Math.max(dt, 1e-6);
          this._capState.set(c.id, va - vb);
        } else if (c.type === 'potentiometer') {
          I = 0;
        } else if (c.type === 'switch' || c.type === 'pushbutton') {
          I = 0;
        } else if (c.type === 'inductor') {
          I = indCurrent.get(c.id) || 0;
        } else if (c.type === 'acsource') {
          I = acCurrent.get(c.id) || 0;
        } else if (c.type === 'mtjsensor') {
          I = 0;
        } else if (c.type === 'toroid') {
          I = toroidCurrent.get(c.id) || 0;
        } else if (c.type === 'ternarycell') {
          const vout = voltages.get(uf.find(c.out));
          const vref = voltages.get(uf.find(c.ref));
          const state = this._ternaryState.get(c.id);
          const r = state === 'hold' ? TERNARY_HOLD_R : TERNARY_ON_R;
          I = (vout - vref) / r;
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
          if (Math.abs(vgs) > spec.vgsMax) {
            warnings.push(`${c.type.toUpperCase()} ${c.label || c.id}: |Vgs|=${Math.abs(vgs).toFixed(2)}V exceeds its ${spec.vgsMax}V gate rating`);
          }
          if (Math.abs(vds) > spec.vdsMax) {
            warnings.push(`${c.type.toUpperCase()} ${c.label || c.id}: |Vds|=${Math.abs(vds).toFixed(2)}V exceeds its ${spec.vdsMax}V drain-source rating`);
          }
          if ((touchCount.get(uf.find(c.gate)) || 0) <= 1) {
            warnings.push(`${c.type.toUpperCase()} ${c.label || c.id}: gate is not wired to anything -- a floating gate picks up noise and can turn the switch on/off unpredictably`);
          }
        }
        currents.set(c.id, I);
      });
      toroidCurrent.forEach((I, key) => currents.set(key, I));

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

      acsources.forEach((ac) => {
        const I = acCurrent.get(ac.id) || 0;
        if (Math.abs(I) > 1.0) {
          warnings.push(`Overload at ${ac.label || ac.id}: ${I.toFixed(2)} A — check your wiring`);
        }
      });

      // the discrete decision itself ('hold'/'pos'/'neg'), not just the
      // millivolt-scale voltage it produces -- lets a nerve-loop/supervisory
      // layer read the actual state directly instead of re-deriving it from
      // out/ref voltages every time
      const ternaryStates = new Map();
      ternaryCells.forEach((tc) => ternaryStates.set(tc.id, this._ternaryState.get(tc.id)));

      // same idea as ternaryStates: expose the MOSFET's actual on/off
      // decisions directly, so the Inspector (or a test) doesn't have to
      // re-derive "is the channel on" from raw currents/voltages itself
      const mosfetStates = new Map();
      mosfets.forEach((f) => mosfetStates.set(f.id, {
        channelOn: this._fetChannelState.get(f.id),
        bodyDiodeOn: this._fetDiodeState.get(f.id),
      }));

      return { voltages, currents, warnings, ternaryStates, mosfetStates, uf, groundRoot, hasCircuit: true };
    }
  }

  const api = {
    Circuit, UnionFind, solveLinear, LED_VF, LED_RON, DIODE_VF, DIODE_RON, BATTERY_RINT, VGND_RINT,
    AC_RINT, MTJ_RINT, NMOS_PARTS, PMOS_PARTS, mosfetSpec,
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window !== 'undefined') window.CircuitEngine = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
