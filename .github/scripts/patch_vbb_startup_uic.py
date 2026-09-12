from pathlib import Path


def replace_once(path, old, new):
    p = Path(path)
    s = p.read_text()
    if old not in s:
        raise SystemExit(f'missing anchor in {path}: {old[:120]}')
    p.write_text(s.replace(old, new, 1))

replace_once(
    'Virtual_Breadboard/js/circuit.js',
    "          const iPrev = this._indState.get(ind.id) || 0;",
    "          const iPrev = this._indState.has(ind.id)\n            ? this._indState.get(ind.id)\n            : (Number.isFinite(Number(ind.initialCurrent)) ? Number(ind.initialCurrent) : 0);"
)

p = Path('Virtual_Breadboard/js/spice-analysis.js')
s = p.read_text()
anchor = "\nmodule.exports = { operatingPoint, steppedOperatingPoint, dcSweep, sweepValues };\n"
if anchor not in s:
    raise SystemExit('spice-analysis export anchor missing')
insert = r'''

/**
 * Run a transient analysis with explicit startup semantics.
 *
 * Default behavior mirrors ordinary SPICE transient startup: solve a DC
 * operating point first, then seed reactive storage from that physical
 * steady state before advancing time. `uic: true` skips that operating-point
 * solve and starts directly from component-declared `initialV` (capacitors)
 * and `initialCurrent` (inductors), defaulting either quantity to zero when
 * omitted. This is intentionally only startup policy; timestep control and
 * integration-method choices remain separate roadmap items.
 */
function transientAnalysis(elements, options) {
  options = options || {};
  const dt = options.dt == null ? 1e-4 : finiteNumber('dt', options.dt);
  if (!(dt > 0)) throw new RangeError('dt must be > 0');
  const steps = options.steps == null ? 1 : Math.trunc(options.steps);
  if (!(steps >= 1)) throw new RangeError('steps must be >= 1');
  const ambientC = options.ambientC;
  if (ambientC != null) finiteNumber('ambientC', ambientC);
  const probes = normalizeProbes(options.probes);
  const uic = !!options.uic;
  const work = cloneElements(elements);
  let startupResult = null;

  if (!uic) {
    const startupOptions = {
      ambientC,
      solverOptions: options.solverOptions,
    };
    startupResult = options.continuation
      ? steppedOperatingPoint(work, Object.assign({}, startupOptions, {
          sourceScales: options.sourceScales,
          gminSteps: options.gminSteps,
          targetGmin: options.targetGmin,
        }))
      : operatingPoint(work, startupOptions);
    if (!startupResult.solver || !startupResult.solver.converged) {
      throw new Error('transient startup operating point did not converge');
    }

    for (const c of work.components || []) {
      if (c.type === 'capacitor') {
        const va = startupResult.voltages.get(startupResult.uf.find(c.a)) || 0;
        const vb = startupResult.voltages.get(startupResult.uf.find(c.b)) || 0;
        c.initialV = va - vb;
      } else if (c.type === 'inductor') {
        c.initialCurrent = startupResult.currents.get(c.id) || 0;
      }
    }
  }

  const circuit = new Circuit();
  const rows = [];
  let result = null;
  for (let k = 0; k < steps; k++) {
    result = circuit.solve(work, dt, ambientC, options.solverOptions);
    const values = {};
    for (const probe of probes) {
      let value = null;
      if (probe.type === 'voltage') {
        const root = result.uf.find(probe.node);
        const raw = result.voltages.get(root);
        value = raw == null ? null : raw;
      } else {
        const raw = result.currents.get(probe.componentId);
        value = raw == null ? null : raw;
      }
      values[probe.name] = value;
    }
    rows.push({
      time: (k + 1) * dt,
      values,
      warnings: Array.from(result.warnings || []),
      converged: !!(result.solver && result.solver.converged),
    });
  }

  return {
    analysis: {
      type: 'tran',
      dt,
      steps,
      uic,
      startup: uic ? 'user-initial-conditions' : 'dc-operating-point',
      continuation: !uic && !!options.continuation,
      capacitorInitialCondition: uic ? 'declared-initialV-or-zero' : 'dc-operating-point-voltage',
      inductorInitialCondition: uic ? 'declared-initialCurrent-or-zero' : 'dc-operating-point-current',
    },
    probes,
    rows,
    startupResult,
    finalResult: result,
  };
}
'''
s = s.replace(anchor, insert + "\nmodule.exports = { operatingPoint, steppedOperatingPoint, dcSweep, transientAnalysis, sweepValues };\n", 1)
p.write_text(s)
