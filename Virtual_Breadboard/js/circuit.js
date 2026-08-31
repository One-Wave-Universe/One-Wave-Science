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

      const batInternal = (c) => '__batint__' + c.id;
      const vgndInternal = (c) => '__vgndint__' + c.id;

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
      });

      const batteries = components.filter((c) => c.type === 'battery');
      const vgnds = components.filter((c) => c.type === 'vgnd');

      let groundRoot = null;
      if (batteries.length) groundRoot = uf.find(batteries[0].b);
      else if (wires.length) groundRoot = uf.find(wires[0].a);
      else if (components.length) groundRoot = uf.find(components[0].a);

      if (groundRoot === null) {
        return { voltages: new Map(), currents: new Map(), warnings: [], hasCircuit: false };
      }

      const roots = new Set();
      const touch = (id) => roots.add(uf.find(id));
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
      });
      roots.add(groundRoot);

      const nodeIndex = new Map();
      let idx = 0;
      for (const r of roots) if (r !== groundRoot) nodeIndex.set(r, idx++);
      const nNodes = idx;
      const nSrc = batteries.length;
      const nVgnd = vgnds.length;
      const size = nNodes + nSrc + nVgnd;

      const gi = (rt) => (rt === groundRoot ? -1 : nodeIndex.get(rt));

      const diodes = components.filter((c) => c.type === 'led' || c.type === 'diode');
      diodes.forEach((d) => {
        if (!this._ledState.has(d.id)) this._ledState.set(d.id, false);
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

        if (!changed) break;
      }

      const currents = new Map();
      const warnings = [];

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
        }
        currents.set(c.id, I);
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

      return { voltages, currents, warnings, uf, groundRoot, hasCircuit: true };
    }
  }

  const api = { Circuit, UnionFind, solveLinear, LED_VF, LED_RON, DIODE_VF, DIODE_RON, BATTERY_RINT, VGND_RINT };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window !== 'undefined') window.CircuitEngine = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
