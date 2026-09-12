'use strict';
const assert = require('assert');
const { Circuit, BATTERY_RINT, capacitorESR, capacitorLeakageR } = require('../js/circuit.js');

let checks = 0;
function ok(name, cond, detail='') { checks++; assert(cond, `${name}${detail ? ': '+detail : ''}`); console.log(`PASS [${name}]${detail ? ' -- '+detail : ''}`); }
function near(name, actual, expected, tol) { checks++; assert(Number.isFinite(actual)); assert(Math.abs(actual-expected)<=tol, `${name}: expected ${expected}, got ${actual}, tol=${tol}`); console.log(`PASS [${name}] -- expected=${expected} actual=${actual}`); }

function run(elements, method, dt, steps, node) {
  const c = new Circuit();
  const values=[];
  let r;
  for (let k=0;k<steps;k++) {
    r=c.solve(elements, dt, 25, {integrationMethod:method});
    values.push(r.voltages.get(r.uf.find(node)) || 0);
    assert(r.solver.converged, `${method} failed to converge at step ${k}`);
  }
  return {values, result:r};
}

console.log('=== Virtual Breadboard integration-method qualification ===');

// Independent analytic RC reference including battery Rint, capacitor ESR and leakage.
const R=999, C=1e-6, V=1;
const cap={id:'C',type:'capacitor',a:'out',b:'gnd',value:C,initialV:0};
const rc={wires:[],components:[
  {id:'BAT',type:'battery',a:'src',b:'gnd',value:V},
  {id:'R',type:'resistor',a:'src',b:'out',value:R}, cap,
]};
const rs=R+BATTERY_RINT, re=capacitorESR(cap), rl=capacitorLeakageR(cap);
const xInf=V*rl/(rs+rl);
const tau=C*(re + 1/(1/rs+1/rl));
const gs=1/rs, ge=1/re, gl=1/rl;
function exactTerminal(t) {
  const x=xInf*(1-Math.exp(-t/tau));
  return (gs*V + ge*x)/(gs+ge+gl);
}
const dt=2e-4, steps=20, exact=exactTerminal(dt*steps);
const be=run(rc,'backward-euler',dt,steps,'out');
const tr=run(rc,'trapezoidal',dt,steps,'out');
const g2=run(rc,'gear2',dt,steps,'out');
const eBe=Math.abs(be.values.at(-1)-exact), eTr=Math.abs(tr.values.at(-1)-exact), eG=Math.abs(g2.values.at(-1)-exact);
ok('trapezoidal-beats-backward-euler-on-analytic-rc', eTr < eBe, `BE=${eBe} TR=${eTr}`);
ok('gear2-beats-backward-euler-on-analytic-rc', eG < eBe, `BE=${eBe} G2=${eG}`);
near('trapezoidal-analytic-rc', tr.values.at(-1), exact, 3e-4);
near('gear2-analytic-rc', g2.values.at(-1), exact, 6e-4);
ok('solver-reports-trapezoidal', tr.result.solver.integrationMethod === 'trapezoidal');
ok('solver-reports-gear2', g2.result.solver.integrationMethod === 'gear2');

// Stiff RC: dt is much larger than tau. Trapezoidal's known weak damping should
// alternate around steady state, while Gear2 should damp the parasitic ringing.
const stiffDt=8*tau;
const stiffTrap=run(rc,'trapezoidal',stiffDt,10,'out').values;
const stiffGear=run(rc,'gear2',stiffDt,10,'out').values;
let trapSignChanges=0;
for(let i=2;i<stiffTrap.length;i++) {
  const a=stiffTrap[i-1]-xInf, b=stiffTrap[i]-xInf;
  if(a*b<0) trapSignChanges++;
}
ok('stiff-trapezoidal-exposes-alternating-ringing', trapSignChanges>=2, `signChanges=${trapSignChanges}`);
const trapTail=Math.abs(stiffTrap.at(-1)-xInf), gearTail=Math.abs(stiffGear.at(-1)-xInf);
ok('gear2-damps-stiff-numerical-ringing', gearTail < trapTail, `trapTail=${trapTail} gearTail=${gearTail}`);

// Underdamped RLC ring-down from stored capacitor energy. A disconnected 0 V
// battery anchors the reference without loading the RLC loop.
const L=10e-3, Cr=1e-6;
const rlc={wires:[],components:[
  {id:'REF',type:'battery',a:'unused',b:'gnd',value:0},
  {id:'C',type:'capacitor',a:'n1',b:'gnd',value:Cr,initialV:1},
  {id:'L',type:'inductor',a:'n1',b:'n2',value:L,initialCurrent:0},
  {id:'R',type:'resistor',a:'n2',b:'gnd',value:0.2},
]};
const period=2*Math.PI*Math.sqrt(L*Cr);
const rdt=period/40, rsteps=240;
const ringBE=run(rlc,'backward-euler',rdt,rsteps,'n1').values;
const ringTR=run(rlc,'trapezoidal',rdt,rsteps,'n1').values;
function tailPeak(a){ return Math.max(...a.slice(Math.floor(a.length*0.6)).map(Math.abs)); }
const peakBE=tailPeak(ringBE), peakTR=tailPeak(ringTR);
ok('trapezoidal-preserves-rlc-ringing-better-than-be', peakTR > peakBE*1.5, `BE=${peakBE} TR=${peakTR}`);
ok('rlc-trapezoidal-remains-bounded', peakTR < 1.05, `peak=${peakTR}`);

assert.throws(()=>new Circuit().solve(rc,dt,25,{integrationMethod:'bogus'}), /unknown integrationMethod/);
checks++; console.log('PASS [invalid-integration-method-fails-loudly]');

console.log(`=== ALL ${checks} INTEGRATION-METHOD CHECKS PASSED ===`);
