#!/usr/bin/env node
'use strict';

const CE = require('../js/circuit.js');
const { Circuit, MOSFET_MODEL_CARDS, mosfetSpec, mosfetChannelCurrent } = CE;
const { smallSignalAc, phasorMagnitude } = require('../js/ac-analysis.js');

let checks = 0;
function check(name, condition, detail='') {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`MOSFET MODEL-CARD QUALIFICATION FAILED: ${name}`);
}
function close(a,b,t){ return Math.abs(a-b) <= t; }

console.log('=== Virtual Breadboard MOSFET model-card qualification ===');

check('four-built-in-cards', Object.keys(MOSFET_MODEL_CARDS).length === 4, Object.keys(MOSFET_MODEL_CARDS).join(','));

const legacy = mosfetSpec({type:'nmos',value:1.5});
const named = mosfetSpec({type:'nmos',model:'AO3400A'});
check('legacy-selector-preserved', legacy.name === 'AO3400A-class (logic-level)', JSON.stringify(legacy));
check('named-card-matches-legacy-rdson', close(named.rdsOn, legacy.rdsOn, 0), `named=${named.rdsOn} legacy=${legacy.rdsOn}`);
check('named-card-matches-legacy-vth', close(named.vth, legacy.vth, 0), `named=${named.vth} legacy=${legacy.vth}`);
check('named-card-preserves-old-body-diode', named.bodyDiodeVf === 0.7 && named.bodyDiodeRon === 5, JSON.stringify(named));

const small = mosfetSpec({type:'nmos',model:'2N7000'});
check('second-nmos-card-resolves', small.name === '2N7000-class', JSON.stringify(small));
check('cards-carry-full-parameter-set', ['vth','rdsOn','vgsMax','vdsMax','ciss','betaCalVov','lambda','offLeakageG','rdsonTempco','bodyDiodeVf','bodyDiodeRon'].every(k => Number.isFinite(small[k])), JSON.stringify(small));

const custom = mosfetSpec({type:'nmos',model:'AO3400A',rdsOn:0.2,lambda:0.1,ciss:2e-9,offLeakageG:1e-6,bodyDiodeVf:0.35,bodyDiodeRon:2});
check('instance-overrides-apply', custom.rdsOn===0.2 && custom.lambda===0.1 && custom.ciss===2e-9 && custom.offLeakageG===1e-6 && custom.bodyDiodeVf===0.35 && custom.bodyDiodeRon===2, JSON.stringify(custom));

const inline = mosfetSpec({type:'pmos',modelCard:{name:'bench PMOS',type:'pmos',vth:-1,rdsOn:0.1,vgsMax:8,vdsMax:20,ciss:1e-9,betaCalVov:2,lambda:0.03,offLeakageG:1e-8,rdsonTempco:0.005,bodyDiodeVf:0.5,bodyDiodeRon:3}});
check('inline-card-supported', inline.name==='bench PMOS' && inline.type==='pmos' && inline.rdsOn===0.1, JSON.stringify(inline));

let unknownRejected=false;
try { mosfetSpec({type:'nmos',model:'NOT_A_REAL_CARD'}); } catch(e) { unknownRejected=/Unknown MOSFET model card/.test(e.message); }
check('unknown-card-rejected', unknownRejected);
let polarityRejected=false;
try { mosfetSpec({type:'pmos',model:'AO3400A'}); } catch(e) { polarityRejected=/cannot use it for pmos/.test(e.message); }
check('wrong-polarity-card-rejected', polarityRejected);

// Continuous model must actually use per-card RDS(on) and lambda rather than
// only exposing them as metadata.
{
  const base={type:'nmos',model:'AO3400A'};
  const highR={type:'nmos',model:'AO3400A',rdsOn:0.3};
  const noLambda={type:'nmos',model:'AO3400A',lambda:0};
  const highLambda={type:'nmos',model:'AO3400A',lambda:0.2};
  const iBase=mosfetChannelCurrent(base,5,1,0,25);
  const iHighR=mosfetChannelCurrent(highR,5,1,0,25);
  const iNoLambda=mosfetChannelCurrent(noLambda,5,5,0,25);
  const iHighLambda=mosfetChannelCurrent(highLambda,5,5,0,25);
  check('rdson-override-changes-channel-current', iHighR < iBase/5, `base=${iBase} highR=${iHighR}`);
  check('lambda-override-changes-saturation-current', iHighLambda > iNoLambda*1.5, `lambda0=${iNoLambda} lambda0.2=${iHighLambda}`);
}

// Off-state leakage is a real stamped path and must follow the selected card.
{
  const elements={wires:[],components:[
    {id:'V',type:'battery',a:'vcc',b:'gnd',value:5},
    {id:'RG',type:'resistor',a:'gate',b:'gnd',value:1000},
    {id:'RD',type:'resistor',a:'vcc',b:'drain',value:1000},
    {id:'Q',type:'nmos',gate:'gate',drain:'drain',source:'gnd',model:'AO3400A',offLeakageG:1e-4},
  ]};
  const r=new Circuit().solve(elements,1e-3,25,{maxIterations:40});
  const iq=r.currents.get('Q');
  check('custom-leakage-solve-converges', r.solver.converged, JSON.stringify(r.solver));
  check('custom-leakage-affects-real-current', iq>2e-4, `Iq=${iq}`);
}

// AC analysis must use the same card's Ciss. With a 1k source resistance,
// an intentionally huge Ciss should heavily attenuate the gate at 100 kHz;
// a tiny Ciss should not. This proves the card survives into frequency domain.
function acGate(ciss) {
  const elements={wires:[],components:[
    {id:'VDD',type:'battery',a:'vcc',b:'gnd',value:5},
    {id:'VIN',type:'diffsource',a:'gate',b:'gnd',value:3,sourceR:1000},
    {id:'RD',type:'resistor',a:'vcc',b:'drain',value:1000},
    {id:'Q',type:'nmos',gate:'gate',drain:'drain',source:'gnd',model:'AO3400A',ciss},
  ]};
  const ac=smallSignalAc(elements,{sourceId:'VIN',frequencies:[100000],magnitude:1,solverOptions:{maxIterations:80}});
  return phasorMagnitude(ac.rows[0].voltages.get(ac.uf.find('gate')));
}
{
  const tiny=acGate(1e-12);
  const huge=acGate(1e-6);
  check('ciss-card-affects-ac-input-loading', tiny>0.9 && huge<0.01, `tiny=${tiny} huge=${huge}`);
}

console.log(`\n=== ALL ${checks} MOSFET MODEL-CARD CHECKS PASSED ===`);
