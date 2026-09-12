from pathlib import Path

p = Path('Virtual_Breadboard/js/circuit.js')
s = p.read_text()

def rep(old, new, name):
    global s
    if old not in s:
        raise SystemExit(name + ' anchor not found')
    s = s.replace(old, new, 1)

rep(
'''      let voltages = new Map();
      let xSol = new Array(size).fill(0);
      let previousVoltages = new Map();''',
'''      let voltages = new Map();
      let xSol = new Array(size).fill(0);
      let previousVoltages = new Map();
      let previousSolution = null;
      let previousPrecisionCurrents = new Map();
      const reltol = solverOptions && Number.isFinite(solverOptions.reltol) ? Math.max(0, solverOptions.reltol) : 1e-3;
      const vntol = solverOptions && Number.isFinite(solverOptions.vntol) ? Math.max(0, solverOptions.vntol) : 1e-6;
      const abstol = solverOptions && Number.isFinite(solverOptions.abstol) ? Math.max(0, solverOptions.abstol) : 1e-12;
      const precisionConvergenceActive = !!(solverOptions && (solverOptions.diodeModel === 'newton' || solverOptions.mosfetModel === 'continuous'));
      let voltageDeltaConverged = !precisionConvergenceActive;
      let currentDeltaConverged = !precisionConvergenceActive;
      let maxVoltageDelta = 0;
      let maxVoltageTolerance = vntol;
      let maxCurrentDelta = 0;
      let maxCurrentTolerance = abstol;''',
'convergence state')

rep(
'''        if (solverOptions && solverOptions.diodeModel === 'newton') {
          let diodeDelta = 0;
          diodes.forEach((d) => {
            if (d.type !== 'diode') return;
            const va = voltages.get(uf.find(d.a)) || 0;
            const vb = voltages.get(uf.find(d.b)) || 0;
            const pva = previousVoltages.get(uf.find(d.a)) || 0;
            const pvb = previousVoltages.get(uf.find(d.b)) || 0;
            diodeDelta = Math.max(diodeDelta, Math.abs((va - vb) - (pva - pvb)));
          });
          if (diodeDelta > 1e-9) changed = true;
        }''',
'''        // Precision-device convergence is checked generically below with
        // RELTOL/VNTOL/ABSTOL rather than hard-coded per-device voltage deltas.''',
'diode hard tolerance')

rep(
'''          const continuousMosfet = solverOptions && solverOptions.mosfetModel === 'continuous';
          if (continuousMosfet) {
            const pvg = previousVoltages.get(uf.find(f.gate)) || 0;
            const pvs = previousVoltages.get(uf.find(f.source)) || 0;
            const pvd = previousVoltages.get(uf.find(f.drain)) || 0;
            const delta = Math.max(Math.abs(vg - pvg), Math.abs(vs - pvs), Math.abs(vd - pvd));
            if (delta > 1e-8) changed = true;
          } else {
            const channelShouldBeOn = f.type === 'nmos' ? vgs > spec.vth : vgs < spec.vth;
            if (channelShouldBeOn !== this._fetChannelState.get(f.id)) {
              this._fetChannelState.set(f.id, channelShouldBeOn);
              changed = true;
            }
          }''',
'''          const continuousMosfet = solverOptions && solverOptions.mosfetModel === 'continuous';
          if (!continuousMosfet) {
            const channelShouldBeOn = f.type === 'nmos' ? vgs > spec.vth : vgs < spec.vth;
            if (channelShouldBeOn !== this._fetChannelState.get(f.id)) {
              this._fetChannelState.set(f.id, channelShouldBeOn);
              changed = true;
            }
          }''',
'MOSFET hard tolerance')

rep(
'''        if (!changed) {
          stateStable = true;
          break;
        }
      }''',
'''        if (precisionConvergenceActive) {
          voltageDeltaConverged = previousSolution !== null;
          currentDeltaConverged = previousSolution !== null;
          maxVoltageDelta = 0;
          maxVoltageTolerance = vntol;
          maxCurrentDelta = 0;
          maxCurrentTolerance = abstol;

          if (previousSolution !== null) {
            for (let vi = 0; vi < nNodes; vi++) {
              const now = xSol[vi] || 0;
              const prev = previousSolution[vi] || 0;
              const delta = Math.abs(now - prev);
              const tol = vntol + reltol * Math.max(Math.abs(now), Math.abs(prev));
              maxVoltageDelta = Math.max(maxVoltageDelta, delta);
              maxVoltageTolerance = Math.max(maxVoltageTolerance, tol);
              if (delta > tol) voltageDeltaConverged = false;
            }

            const precisionCurrents = new Map();
            if (solverOptions && solverOptions.diodeModel === 'newton') {
              diodes.forEach((d) => {
                if (d.type !== 'diode') return;
                const va = voltages.get(uf.find(d.a)) || 0;
                const vb = voltages.get(uf.find(d.b)) || 0;
                const vt = THERMAL_VOLTAGE_25C * ((tempOf(d.id) + 273.15) / 298.15);
                const nvt = DIODE_N * vt;
                const vj = Math.max(-5, Math.min(0.8, va - vb));
                precisionCurrents.set('diode:' + d.id, DIODE_IS * (Math.exp(vj / nvt) - 1));
              });
            }
            if (solverOptions && solverOptions.mosfetModel === 'continuous') {
              mosfets.forEach((f) => {
                const vg = voltages.get(uf.find(f.gate)) || 0;
                const vd = voltages.get(uf.find(f.drain)) || 0;
                const vs = voltages.get(uf.find(f.source)) || 0;
                const ich = mosfetChannelCurrent(f, vg, vd, vs, tempOf(f.id));
                precisionCurrents.set('mosfet:' + f.id, ich + (vd - vs) * MOSFET_OFF_LEAKAGE_G);
              });
            }
            precisionCurrents.forEach((now, key) => {
              if (!previousPrecisionCurrents.has(key)) {
                currentDeltaConverged = false;
                return;
              }
              const prev = previousPrecisionCurrents.get(key);
              const delta = Math.abs(now - prev);
              const tol = abstol + reltol * Math.max(Math.abs(now), Math.abs(prev));
              maxCurrentDelta = Math.max(maxCurrentDelta, delta);
              maxCurrentTolerance = Math.max(maxCurrentTolerance, tol);
              if (delta > tol) currentDeltaConverged = false;
            });
            previousPrecisionCurrents = precisionCurrents;
          } else {
            const seedCurrents = new Map();
            if (solverOptions && solverOptions.diodeModel === 'newton') {
              diodes.forEach((d) => {
                if (d.type !== 'diode') return;
                const va = voltages.get(uf.find(d.a)) || 0;
                const vb = voltages.get(uf.find(d.b)) || 0;
                const vt = THERMAL_VOLTAGE_25C * ((tempOf(d.id) + 273.15) / 298.15);
                const nvt = DIODE_N * vt;
                const vj = Math.max(-5, Math.min(0.8, va - vb));
                seedCurrents.set('diode:' + d.id, DIODE_IS * (Math.exp(vj / nvt) - 1));
              });
            }
            if (solverOptions && solverOptions.mosfetModel === 'continuous') {
              mosfets.forEach((f) => {
                const vg = voltages.get(uf.find(f.gate)) || 0;
                const vd = voltages.get(uf.find(f.drain)) || 0;
                const vs = voltages.get(uf.find(f.source)) || 0;
                seedCurrents.set('mosfet:' + f.id, mosfetChannelCurrent(f, vg, vd, vs, tempOf(f.id)) + (vd - vs) * MOSFET_OFF_LEAKAGE_G);
              });
            }
            previousPrecisionCurrents = seedCurrents;
          }
          previousSolution = xSol.slice();
        }

        if (!changed && (!precisionConvergenceActive || (voltageDeltaConverged && currentDeltaConverged))) {
          stateStable = true;
          break;
        }
      }''',
'iteration convergence')

rep(
'''        relTolerance,
        gmin: solveGmin,
        diodeModel: solverOptions && solverOptions.diodeModel === 'newton' ? 'newton' : 'simple',
        mosfetModel: solverOptions && solverOptions.mosfetModel === 'continuous' ? 'continuous' : 'simple',
      };''',
'''        relTolerance,
        gmin: solveGmin,
        reltol,
        vntol,
        abstol,
        voltageDeltaConverged,
        currentDeltaConverged,
        maxVoltageDelta,
        maxVoltageTolerance,
        maxCurrentDelta,
        maxCurrentTolerance,
        diodeModel: solverOptions && solverOptions.diodeModel === 'newton' ? 'newton' : 'simple',
        mosfetModel: solverOptions && solverOptions.mosfetModel === 'continuous' ? 'continuous' : 'simple',
      };''',
'solver metadata')

p.write_text(s)
