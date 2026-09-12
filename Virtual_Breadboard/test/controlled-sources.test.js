#!/usr/bin/env node
'use strict';

const { Circuit } = require('../js/circuit.js');
const { smallSignalAc, phasorMagnitude } = require('../js/ac-analysis.js');

let checks = 0;
function check(name, condition, detail='') {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`CONTROLLED-SOURCE QUALIFICATION FAILED: ${name}`);
}
function close(a,b,t=2e-5){ return Math.abs(a-b) <= t; }
function v(result,node){ return result.voltages.get(result.uf.find(node)) || 0; }

console.log('=== Virtual Breadboard current + controlled-source qualification ===');

// Independent current source: 2 mA from ground -> out through 1 kOhm gives 2 V.
{
  const elements={wires:[],components:[
    {id:'I1',type:'isource',a:'gnd',b:'out',value:0.002},
    {id:'R1',type:'resistor',a:'out',b:'gnd',value:1000},
  ]};
  const r=new Circuit().solve(elements,1e-3,25,{});
  check('isource-converges',r.solver.converged,JSON.stringify(r.solver));
  check('isource-ohms-law',close(v(r,'out'),2,5e-5),`Vout=${v(r,'out')}`);
  check('isource-current-reported',r.currents.get('I1')===0.002,`I=${r.currents.get('I1')}`);
}

// VCCS: 1 mS * 1 V control, oriented ground -> out, drives ~1 V into 1 kOhm.
{
  const elements={wires:[],components:[
    {id:'VCTRL',type:'battery',a:'ctrl',b:'gnd',value:1},
    {id:'G1',type:'vccs',a:'gnd',b:'out',controlP:'ctrl',controlN:'gnd',gain:0.001},
    {id:'R1',type:'resistor',a:'out',b:'gnd',value:1000},
  ]};
  const r=new Circuit().solve(elements,1e-3,25,{});
  check('vccs-gain',close(v(r,'out'),0.999999,5e-4),`Vout=${v(r,'out')}`);
  check('vccs-current-reported',close(r.currents.get('G1'),0.001,2e-6),`I=${r.currents.get('G1')}`);
}

// VCVS: output is exactly gain * differential control voltage. The control
// input is ideal/high-impedance, so the 1-ohm battery source resistance has
// no control-side drop here: 1.5 V * 2 = 3.0 V.
{
  const elements={wires:[],components:[
    {id:'VCTRL',type:'battery',a:'ctrl',b:'gnd',value:1.5},
    {id:'E1',type:'vcvs',a:'out',b:'gnd',controlP:'ctrl',controlN:'gnd',gain:2},
    {id:'R1',type:'resistor',a:'out',b:'gnd',value:1000},
  ]};
  const r=new Circuit().solve(elements,1e-3,25,{});
  check('vcvs-gain',close(v(r,'out'),3.0,5e-6),`Vout=${v(r,'out')}`);
}

// Current-controlled sources use the named voltage-source MNA branch current.
// With a +1 V source feeding 1 kOhm through its real 1-ohm source resistance,
// MNA control current is about -0.999 mA (positive branch direction is + -> -).
{
  const base=[
    {id:'VSENSE',type:'battery',a:'ctrl',b:'gnd',value:1},
    {id:'RCTRL',type:'resistor',a:'ctrl',b:'gnd',value:1000},
  ];
  const cccs={wires:[],components:[...base,
    {id:'F1',type:'cccs',a:'out',b:'gnd',controlSourceId:'VSENSE',gain:2},
    {id:'ROUT',type:'resistor',a:'out',b:'gnd',value:1000},
  ]};
  const rf=new Circuit().solve(cccs,1e-3,25,{});
  check('cccs-current-gain-sign',v(rf,'out')>1.9 && v(rf,'out')<2.1,`Vout=${v(rf,'out')} I(F1)=${rf.currents.get('F1')}`);

  const ccvs={wires:[],components:[...base,
    {id:'H1',type:'ccvs',a:'out',b:'gnd',controlSourceId:'VSENSE',gain:1000},
    {id:'ROUT',type:'resistor',a:'out',b:'gnd',value:1000},
  ]};
  const rh=new Circuit().solve(ccvs,1e-3,25,{});
  check('ccvs-transresistance-sign',v(rh,'out')<-0.95 && v(rh,'out')>-1.05,`Vout=${v(rh,'out')} I(H1)=${rh.currents.get('H1')}`);
}

// AC: current source can be the selected small-signal excitation.
{
  const elements={wires:[],components:[
    {id:'IAC',type:'isource',a:'gnd',b:'out',value:0},
    {id:'R1',type:'resistor',a:'out',b:'gnd',value:1000},
  ]};
  const ac=smallSignalAc(elements,{sourceId:'IAC',frequencies:[1000],magnitude:0.001});
  const z=ac.rows[0].voltages.get(ac.uf.find('out'));
  check('ac-current-source-excitation',close(phasorMagnitude(z),0.999999,5e-5),`|Vout|=${phasorMagnitude(z)}`);
}

// AC VCVS: 2x voltage gain must remain 2x in small-signal linearization.
{
  const elements={wires:[],components:[
    {id:'VIN',type:'battery',a:'in',b:'gnd',value:0},
    {id:'E1',type:'vcvs',a:'out',b:'gnd',controlP:'in',controlN:'gnd',gain:2},
    {id:'R1',type:'resistor',a:'out',b:'gnd',value:1000},
  ]};
  const ac=smallSignalAc(elements,{sourceId:'VIN',frequencies:[1000],magnitude:1});
  const vin=ac.rows[0].voltages.get(ac.uf.find('in'));
  const vout=ac.rows[0].voltages.get(ac.uf.find('out'));
  check('ac-vcvs-gain',close(phasorMagnitude(vout)/phasorMagnitude(vin),2,2e-5),`gain=${phasorMagnitude(vout)/phasorMagnitude(vin)}`);
}

// Invalid current-control references fail loudly rather than silently producing zero gain.
{
  let threw=false;
  try {
    new Circuit().solve({wires:[],components:[
      {id:'Fbad',type:'cccs',a:'out',b:'gnd',controlSourceId:'missing',gain:2},
      {id:'R',type:'resistor',a:'out',b:'gnd',value:1000},
    ]},1e-3,25,{});
  } catch (e) { threw=/controlSourceId/.test(String(e)); }
  check('bad-control-reference-rejected',threw);
}

console.log(`\n=== ALL ${checks} CURRENT/CONTROLLED-SOURCE CHECKS PASSED ===`);
