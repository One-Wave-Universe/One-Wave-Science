'use strict';
const assert = require('assert');
const CE = require('../js/circuit.js');
const { Circuit, pwlValue, pulseValue, transientSourceValue, AC_RINT } = CE;
let n=0;
function near(name,a,b,tol=1e-9){ n++; assert(Math.abs(a-b)<=tol, `${name}: expected ${b}, got ${a}`); console.log(`PASS [${name}]`); }
function ok(name,v,msg=''){ n++; assert(v, `${name}${msg?': '+msg:''}`); console.log(`PASS [${name}]${msg?' -- '+msg:''}`); }
console.log('=== Virtual Breadboard PWL / PULSE qualification ===');
near('pwl-holds-first-before-start', pwlValue([[1,2],[2,4]],0), 2);
near('pwl-interpolates-linearly', pwlValue([[0,0],[1,10]],0.25), 2.5);
near('pwl-hits-breakpoint', pwlValue([[0,0],[1,10],[2,-2]],1), 10);
near('pwl-holds-last-after-end', pwlValue([[0,0],[1,10]],3), 10);
near('pwl-sorts-input-points', pwlValue([[1,10],[0,0]],0.5), 5);
const p={type:'pulse',v1:0,v2:5,delay:1,rise:1,width:2,fall:1,period:6};
near('pulse-low-before-delay',pulseValue(p,0.5),0);
near('pulse-rise',pulseValue(p,1.5),2.5);
near('pulse-high',pulseValue(p,2.5),5);
near('pulse-fall',pulseValue(p,4.5),2.5);
near('pulse-low-after-fall',pulseValue(p,5.5),0);
near('pulse-repeats-periodically',pulseValue(p,7.5),2.5);
near('one-shot-returns-low',pulseValue({...p,period:0},20),0);
near('dispatcher-pwl',transientSourceValue({type:'pwl',points:[[0,1],[1,3]]},0.5),2);
near('dispatcher-pulse',transientSourceValue({type:'pulse',v1:-1,v2:1,delay:0,rise:0,width:1,fall:0,period:2},0.5),1);
// Loaded source: 5 V PULSE through the existing 1-ohm source impedance into 99 ohm.
// Explicitly anchor the reference node, as a real bench circuit must.
const c=new Circuit();
const elements={wires:[{a:'gnd',b:'gnd'}],components:[
 {id:'VP',type:'pulse',a:'out',b:'gnd',v1:0,v2:5,delay:0,rise:0,fall:0,width:1,period:2},
 {id:'R',type:'resistor',a:'out',b:'gnd',value:99},
]};
const r=c.solve(elements,0.5,25);
const v=r.voltages.get(r.uf.find('out'));
const expected=5*99/(99+AC_RINT);
near('pulse-loaded-voltage-uses-source-impedance',v,expected,2e-6);
near('pulse-current-report-matches-load',Math.abs(r.currents.get('VP')),expected/99,2e-8);
ok('pulse-solver-converges',r.solver.converged,JSON.stringify(r.solver));
console.log(`=== ALL ${n} PWL/PULSE CHECKS PASSED ===`);
