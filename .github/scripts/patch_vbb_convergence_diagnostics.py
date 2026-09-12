from pathlib import Path
p=Path('Virtual_Breadboard/js/circuit.js')
s=p.read_text()

def rep(a,b):
    global s
    if a not in s:
        raise SystemExit('missing anchor: '+a[:160])
    s=s.replace(a,b,1)

anchor="""      const rowMemCore = (mcK, windingIdx) => memCoreRowOffsets[mcK] + windingIdx;
      const ctrlVRowBase = memCoreRowBase + nMemCoreRows;
      const rowCtrlV = (k) => ctrlVRowBase + k;
      const size = ctrlVRowBase + controlledVoltageSources.length;

      const gi = (rt) => (rt === groundRoot ? -1 : nodeIndex.get(rt));
"""
replacement="""      const rowMemCore = (mcK, windingIdx) => memCoreRowOffsets[mcK] + windingIdx;
      const ctrlVRowBase = memCoreRowBase + nMemCoreRows;
      const rowCtrlV = (k) => ctrlVRowBase + k;
      const size = ctrlVRowBase + controlledVoltageSources.length;

      // Stable equation labels make convergence diagnostics actionable and
      // deterministic. Node rows are KCL equations; every extra MNA row is a
      // branch/constraint equation tied back to the owning component id.
      const equationLabels = new Array(size);
      for (const [rootName, row] of nodeIndex.entries()) equationLabels[row] = { kind: 'node', id: String(rootName), row };
      batteries.forEach((c,k)=>{ equationLabels[rowBat(k)] = { kind:'branch', id:c.id, type:c.type, row:rowBat(k) }; });
      vgnds.forEach((c,k)=>{ equationLabels[rowVgnd(k)] = { kind:'branch', id:c.id, type:c.type, row:rowVgnd(k) }; });
      inductors.forEach((c,k)=>{ equationLabels[rowInd(k)] = { kind:'branch', id:c.id, type:c.type, row:rowInd(k) }; });
      acsources.forEach((c,k)=>{ equationLabels[rowAc(k)] = { kind:'branch', id:c.id, type:c.type, row:rowAc(k) }; });
      mtjsensors.forEach((c,k)=>{
        equationLabels[rowMtjSin(k)] = { kind:'branch', id:c.id+':sin', type:c.type, row:rowMtjSin(k) };
        equationLabels[rowMtjCos(k)] = { kind:'branch', id:c.id+':cos', type:c.type, row:rowMtjCos(k) };
      });
      toroids.forEach((c,tk)=>c.windings.forEach((w,wi)=>{ equationLabels[rowToroid(tk,wi)] = { kind:'branch', id:c.id+':w'+wi, type:c.type, row:rowToroid(tk,wi) }; }));
      memoryCores.forEach((c,mk)=>c.windings.forEach((w,wi)=>{ equationLabels[rowMemCore(mk,wi)] = { kind:'branch', id:c.id+':w'+wi, type:c.type, row:rowMemCore(mk,wi) }; }));
      controlledVoltageSources.forEach((c,k)=>{ equationLabels[rowCtrlV(k)] = { kind:'branch', id:c.id, type:c.type, row:rowCtrlV(k) }; });
      for (let r=0; r<size; r++) if (!equationLabels[r]) equationLabels[r] = { kind: r < nNodes ? 'node' : 'branch', id: `row-${r}`, row:r };

      const gi = (rt) => (rt === groundRoot ? -1 : nodeIndex.get(rt));
"""
rep(anchor,replacement)

old="""      let maxResidual = 0;
      let maxEquationScale = 0;
      if (size && finalA && finalB) {
        for (let i = 0; i < size; i++) {
          let ax = 0;
          let scale = Math.abs(finalB[i]);
          for (let j = 0; j < size; j++) {
            const term = finalA[i][j] * xSol[j];
            ax += term;
            scale += Math.abs(term);
          }
          maxResidual = Math.max(maxResidual, Math.abs(ax - finalB[i]));
          maxEquationScale = Math.max(maxEquationScale, scale);
        }
      }
      const absTolerance = solverOptions && Number.isFinite(solverOptions.absTolerance)
        ? Math.max(0, solverOptions.absTolerance) : 1e-9;
      const relTolerance = solverOptions && Number.isFinite(solverOptions.relTolerance)
        ? Math.max(0, solverOptions.relTolerance) : 1e-6;
      const residualTolerance = absTolerance + relTolerance * maxEquationScale;
      const numericalConverged = Number.isFinite(maxResidual) && maxResidual <= residualTolerance;
      const solver = {
"""
new="""      let maxResidual = 0;
      let maxEquationScale = 0;
      let worstResidual = null;
      let worstNodeResidual = null;
      let worstBranchResidual = null;
      const absTolerance = solverOptions && Number.isFinite(solverOptions.absTolerance)
        ? Math.max(0, solverOptions.absTolerance) : 1e-9;
      const relTolerance = solverOptions && Number.isFinite(solverOptions.relTolerance)
        ? Math.max(0, solverOptions.relTolerance) : 1e-6;
      if (size && finalA && finalB) {
        for (let i = 0; i < size; i++) {
          let ax = 0;
          let scale = Math.abs(finalB[i]);
          for (let j = 0; j < size; j++) {
            const term = finalA[i][j] * xSol[j];
            ax += term;
            scale += Math.abs(term);
          }
          const residual = Math.abs(ax - finalB[i]);
          const tolerance = absTolerance + relTolerance * scale;
          const normalized = tolerance > 0 ? residual / tolerance : (residual === 0 ? 0 : Infinity);
          const label = equationLabels[i] || { kind: i < nNodes ? 'node' : 'branch', id: `row-${i}`, row:i };
          const diag = { row:i, kind:label.kind, id:label.id, type:label.type || null, residual, scale, tolerance, normalized };
          // Strict '>' preserves row order as the deterministic tie-breaker.
          if (!worstResidual || residual > worstResidual.residual) worstResidual = diag;
          if (diag.kind === 'node' && (!worstNodeResidual || residual > worstNodeResidual.residual)) worstNodeResidual = diag;
          if (diag.kind === 'branch' && (!worstBranchResidual || residual > worstBranchResidual.residual)) worstBranchResidual = diag;
          maxResidual = Math.max(maxResidual, residual);
          maxEquationScale = Math.max(maxEquationScale, scale);
        }
      }
      const residualTolerance = absTolerance + relTolerance * maxEquationScale;
      const numericalConverged = Number.isFinite(maxResidual) && maxResidual <= residualTolerance;
      const anyNonFinite = !Number.isFinite(maxResidual) || xSol.some((v)=>!Number.isFinite(v));
      let failureReason = null;
      if (anyNonFinite) failureReason = 'NON_FINITE_SOLUTION';
      else if (!stateStable && iterationsUsed >= iterations) failureReason = 'ITERATION_LIMIT_STATE_UNSTABLE';
      else if (!stateStable) failureReason = 'DEVICE_STATE_UNSTABLE';
      else if (!numericalConverged) failureReason = 'RESIDUAL_EXCEEDED';
      const solver = {
"""
rep(old,new)

rep("""        maxResidual,
        residualTolerance,
        absTolerance,
""","""        maxResidual,
        residualTolerance,
        worstResidual,
        worstNodeResidual,
        worstBranchResidual,
        failureReason,
        absTolerance,
""")

oldwarn="""      if (!solver.converged) {
        warnings.push(`SOLVER FAILED: nonlinear solve did not converge in ${solver.iterations}/${solver.maxIterations} iterations (stateStable=${solver.stateStable}, residual=${solver.maxResidual}, tolerance=${solver.residualTolerance})`);
      }
"""
newwarn="""      if (!solver.converged) {
        const wr = solver.worstResidual;
        const where = wr ? `${wr.kind}:${wr.id} row=${wr.row} residual=${wr.residual} tolerance=${wr.tolerance}` : 'no-equation-diagnostic';
        warnings.push(`SOLVER FAILED: nonlinear solve did not converge in ${solver.iterations}/${solver.maxIterations} iterations (reason=${solver.failureReason || 'UNKNOWN'}, stateStable=${solver.stateStable}, ${where})`);
      }
"""
rep(oldwarn,newwarn)
p.write_text(s)
