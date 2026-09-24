#!/usr/bin/env node
'use strict';

const CE = require('../js/circuit.js');
const { Circuit, bjtCurrents, bjtSpec, BJT_BETA_F } = CE;
const { smallSignalAc, phasorMagnitude, phasorPhaseDeg } = require('../js/ac-analysis.js');

let checks = 0;
function check(name, condition, detail='') {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`BJT QUALIFICATION FAILED: ${name}`);
}
function close(a,b,t){ return Math.abs(a-b) <= t; }
function v(result,node){ return result.voltages.get(result.uf.find(node)) || 0; }

console.log('=== Virtual Breadboard BJT qualification ===');

check('bjt-helper-exported', typeof bjtCurrents === 'function');
check('bjt-default-beta', bjtSpec({type:'npn'}).betaF === BJT_BETA_F, JSON.stringify(bjtSpec({type:'npn'})));
check('bjt-custom-beta-parameter', bjtSpec({type:'npn',betaF:150}).betaF === 150, JSON.stringify(bjtSpec({type:'npn',betaF:150})));

// Independent Ebers-Moll forward-active reference: Vbe forward, Vbc strongly reverse.
{
  const q={id:'QREF',type:'npn'};
  const i=bjtCurrents(q,0.65,5,0,25);
  check('npn-forward-current-signs', i.collector>0 && i.base>0 && i.emitter<0, JSON.stringify(i));
  check('npn-kcl', Math.abs(i.collector+i.base+i.emitter)<1e-15, `sum=${i.collector+i.base+i.emitter}`);
  check('npn-forward-beta', close(i.collector/i.base,BJT_BETA_F,0.2), `beta=${i.collector/i.base}`);
}

// Exact polarity mirror: mirrored PNP voltages must mirror all terminal currents.
{
  const n=bjtCurrents({id:'QN',type:'npn'},0.65,5,0,25);
  const p=bjtCurrents({id:'QP',type:'pnp'},-0.65,-5,0,25);
  check('pnp-collector-mirror', close(p.collector,-n.collector,1e-15), `N=${n.collector} P=${p.collector}`);
  check('pnp-base-mirror', close(p.base,-n.base,1e-15), `N=${n.base} P=${p.base}`);
  check('pnp-emitter-mirror', close(p.emitter,-n.emitter,1e-15), `N=${n.emitter} P=${p.emitter}`);
}

function npnCircuit(vbase) {
  return {wires:[],components:[
    {id:'VCC',type:'battery',a:'vcc',b:'gnd',value:5},
    {id:'VB',type:'diffsource',a:'base',b:'gnd',value:vbase,sourceR:0.05},
    {id:'RC',type:'resistor',a:'vcc',b:'collector',value:1000},
    {id:'Q1',type:'npn',base:'base',collector:'collector',emitter:'gnd'},
  ]};
}

// Forward-active common-emitter stage: collector current must be supplied by RC and
// the shared precision convergence criteria must actually settle the BJT.
{
  const r=new Circuit().solve(npnCircuit(0.68),1e-3,25,{maxIterations:80});
  const ic=r.currents.get('Q1:collector');
  const ib=r.currents.get('Q1:base');
  const ir=r.currents.get('RC');
  check('npn-circuit-converges', r.solver.converged, JSON.stringify(r.solver));
  check('npn-collector-forward-active', ic>1e-4 && ic<0.003, `Ic=${ic} Vc=${v(r,'collector')}`);
  check('npn-base-current-positive', ib>0, `Ib=${ib}`);
  check('npn-load-kcl', close(ic,ir,2e-6), `Ic=${ic} I(RC)=${ir}`);
  check('npn-collector-above-base-forward-active', v(r,'collector')>v(r,'base'), `Vc=${v(r,'collector')} Vb=${v(r,'base')}`);
}

// Cutoff is continuous leakage-scale behavior, not a hard threshold switch.
{
  const r=new Circuit().solve(npnCircuit(0),1e-3,25,{maxIterations:80});
  check('npn-cutoff-converges', r.solver.converged, JSON.stringify(r.solver));
  check('npn-cutoff-current-small', Math.abs(r.currents.get('Q1:collector'))<1e-9, `Ic=${r.currents.get('Q1:collector')}`);
}

// Heavy base drive must move the device into saturation: collector falls below base,
// activating both junctions rather than pretending beta remains constant forever.
// This is deliberately a hard numerical case and must converge with junction limiting;
// the test is not relaxed to avoid the saturated Ebers-Moll region.
{
  const r=new Circuit().solve(npnCircuit(0.82),1e-3,25,{maxIterations:120});
  check('npn-saturation-converges', r.solver.converged, JSON.stringify(r.solver));
  check('npn-saturation-both-junctions-forward', v(r,'collector')<v(r,'base'), `Vc=${v(r,'collector')} Vb=${v(r,'base')}`);
  check('npn-saturation-beta-collapses', r.currents.get('Q1:collector')/r.currents.get('Q1:base') < BJT_BETA_F/2, `forcedBeta=${r.currents.get('Q1:collector')/r.currents.get('Q1:base')}`);
}

// PNP circuit is the polarity mirror of the NPN stage. Compare voltages relative
// to the emitter because solve() is free to choose a different absolute reference
// node; only voltage differences are physical.
{
  const elements={wires:[],components:[
    {id:'VEE',type:'battery',a:'gnd',b:'vee',value:5},
    {id:'VB',type:'diffsource',a:'gnd',b:'base',value:0.68,sourceR:0.05},
    {id:'RC',type:'resistor',a:'collector',b:'vee',value:1000},
    {id:'Q1',type:'pnp',base:'base',collector:'collector',emitter:'gnd'},
  ]};
  const r=new Circuit().solve(elements,1e-3,25,{maxIterations:80});
  const vce=v(r,'collector')-v(r,'gnd');
  check('pnp-circuit-converges', r.solver.converged, JSON.stringify(r.solver));
  check('pnp-collector-current-negative', r.currents.get('Q1:collector')<0, `Ic=${r.currents.get('Q1:collector')}`);
  check('pnp-mirrored-collector-voltage', vce<0 && vce>-5, `Vce=${vce}`);
}

// AC uses the same three-terminal Jacobian at the solved operating point. A common-
// emitter stage must therefore show nontrivial small-signal gain and inversion.
{
  const ac=smallSignalAc(npnCircuit(0.68),{sourceId:'VB',frequencies:[1000],magnitude:1,solverOptions:{maxIterations:80}});
  const row=ac.rows[0];
  const vin=row.voltages.get(ac.uf.find('base'));
  const vout=row.voltages.get(ac.uf.find('collector'));
  const gain={re:(vout.re*vin.re+vout.im*vin.im)/(vin.re*vin.re+vin.im*vin.im),im:(vout.im*vin.re-vout.re*vin.im)/(vin.re*vin.re+vin.im*vin.im)};
  check('bjt-ac-gain-nontrivial', phasorMagnitude(gain)>1, `|gain|=${phasorMagnitude(gain)}`);
  const phase=Math.abs(phasorPhaseDeg(gain));
  check('bjt-ac-common-emitter-inverts', phase>170, `phase=${phasorPhaseDeg(gain)}`);
}

console.log(`\n=== ALL ${checks} BJT CHECKS PASSED ===`);
