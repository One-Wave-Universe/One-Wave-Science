#!/usr/bin/env node
// Executes the real app and solver with a minimal DOM/canvas adapter. This
// proves controller behavior, not browser rendering or visual usability.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const plain = x => JSON.parse(JSON.stringify(x));
function appHarness() {
  const draw = new Proxy({}, {get: (o,k) => o[k] || (()=>({addColorStop(){}})), set:(o,k,v)=>(o[k]=v,true)});
  class Element {
    constructor(){ this.children=[];this.options=this.children;this.dataset={};this.style={};this.value='';this.listeners={};this.classList={toggle(){},add(){},remove(){}};this.clientWidth=600;this.clientHeight=220;this.scrollTop=0;this.scrollHeight=220; }
    insertBefore(e){this.children.unshift(e);return e;}
    appendChild(e){this.children.push(e);return e;}
    addEventListener(n,fn){(this.listeners[n] ||= []).push(fn);}
    dispatch(n,event={}){for(const fn of this.listeners[n]||[]) fn(event);}
    getContext(){return draw;}
    getBoundingClientRect(){return {left:0,top:0,width:600,height:220};}
    contains(){return false;}
    querySelector(){return new Element();}
    querySelectorAll(){return [];}
    setAttribute(){}
    removeAttribute(){}
    remove(){}
  }
  const elements=new Map();
  const el=id=>{if(!elements.has(id))elements.set(id,new Element());return elements.get(id);};
  const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
  for(const match of html.matchAll(/id="([^"]+)"[^>]*?(?:value="([^"]*)")?[^>]*>/g))el(match[1]);
  el('simSeconds').value='0.1';el('simDt').value='0.001';
  let nextFrame;
  const storage=new Map();
  const context={console, Math, Map, Set, performance:{now:()=>0},setTimeout:()=>0,clearTimeout(){},
    requestAnimationFrame:fn=>{nextFrame=fn;},confirm:()=>true,
    localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},
    document:{getElementById:el,createElement:()=>new Element(),querySelector:()=>new Element(),querySelectorAll:()=>[],addEventListener(){},body:new Element()},
    Board:require('../js/board'),Components:require('../js/components'),CircuitEngine:require('../js/circuit'),AIBuilder:require('../js/ai')};
  context.window=context;context.devicePixelRatio=1;context.addEventListener=()=>{};
  vm.createContext(context); vm.runInContext(fs.readFileSync(path.join(root,'js/app.js'),'utf8'),context,{filename:'app.js'});
  return {api:context.breadboard,el,frame:t=>nextFrame(t),context};
}
let checks=0;
function check(name,fn){fn();console.log('PASS',name);checks++;}
const h=appHarness(), a=h.api;
const terminal=(row,col)=>({row,col});
const spec={layout:'1large',parts:[
  {id:'V1',type:'battery',value:5,terminals:[terminal('e',5),terminal('f',5)]},
  {id:'R1',type:'resistor',value:1000,terminals:[terminal('b',5),terminal('b',10)]},
  {id:'C1',type:'capacitor',value:1e-6,initialV:0,terminals:[terminal('c',10),terminal('g',5)]},
  {id:'P1',type:'diffscope',terminals:[terminal('a',10),terminal('h',5)]},
],nodeNames:{OUT:terminal('d',10),GND:terminal('j',5)},measurements:[{label:'Vcap',a:'OUT',b:'GND'}]};
check('load pauses and retains named IDs',()=>{a.load(spec);assert.equal(a.receipt().status,'UNRUN');assert.equal(a.receipt().running,false);assert.deepEqual(plain(a.spec().parts.map(p=>p.id)),['V1','R1','C1','P1']);});
let first;
check('fixed RC run reports real probe and units',()=>{first=plain(a.run(.001,.00001));assert.equal(first.run.steps,100);assert.equal(first.units.voltage,'V');assert.ok(first.measurements.Vcap>3.1&&first.measurements.Vcap<3.2);assert.equal(first.probes[0].volts,first.measurements.Vcap);assert.equal(first.physicallyValidated,false);});
check('paused animation freezes time/results/trace',()=>{const before=plain(a.receipt());h.frame(100);h.frame(200);assert.deepEqual(plain(a.receipt()),before);});
check('reset preserves circuit and clears state/trace/time',()=>{const before=plain(a.spec());a.reset();const r=a.receipt();assert.equal(r.timeSeconds,0);assert.equal(r.status,'UNRUN');assert.equal(r.probes[0].samples.length,0);assert.deepEqual(plain(a.spec()),before);});
check('repeatable fixed run after reset',()=>{const again=plain(a.run(.001,.00001));assert.deepEqual(again.voltages,first.voltages);assert.deepEqual(again.currents,first.currents);assert.deepEqual(again.probes,first.probes);});
check('failed import atomic including layout and measurements',()=>{const before=plain(a.receipt());for(const mutate of [s=>s.layout='bad',s=>s.parts[1].id='V1',s=>s.parts[0].terminals[0].col=99,s=>s.measurements[0].a='missing',s=>s.parts[1].value='Infinity']){const bad=plain(spec);mutate(bad);assert.throws(()=>a.load(bad));assert.deepEqual(plain(a.receipt()),before);}});
check('invalid duration cannot hang or mutate state',()=>{const before=plain(a.receipt());for(const [s,dt] of [[Infinity,.001],[1,0],[-1,.001],[10,.000001],[1,NaN]])assert.throws(()=>a.run(s,dt));assert.deepEqual(plain(a.receipt()),before);});
check('edited spec reruns with changed measured result',()=>{const edited=plain(spec);edited.parts[1].value=2000;a.load(edited);const r=a.run(.001,.00001);assert.ok(r.measurements.Vcap<2);});
check('CLI and UI produce same RC voltage/current',()=>{a.load(spec);const ui=a.run(.001,.00001);const cli=spawnSync(process.execPath,['simulate.js'],{cwd:root,input:JSON.stringify({...plain(a.spec()),sim:{seconds:.001,dt:.00001}}),encoding:'utf8'});assert.equal(cli.status,0,cli.stderr);const r=JSON.parse(cli.stdout);assert.deepEqual(plain(ui.voltages),r.final.voltages);assert.deepEqual(plain(ui.currents),r.final.currents);});
check('human button path loads, runs and shows receipt',()=>{h.el('circuitSpec').value=JSON.stringify(spec);h.el('specImport').dispatch('click');h.el('simStep').dispatch('click');const r=JSON.parse(h.el('simReceipt').value);assert.equal(r.running,false);assert.equal(r.run.steps,100);assert.ok(r.measurements.Vcap>4.9);h.el('simReset').dispatch('click');assert.equal(a.receipt().status,'UNRUN');});
check('every existing preset round-trips through offline import',()=>{
  for (const id of ['presetLed','presetRC','presetShort','presetCalA','presetCalB','presetCalC','presetCalD','presetCalE','presetMemCell','presetCalF','presetCalG','presetCalH','presetStage1']) {
    h.el(id).dispatch('click'); const saved=plain(a.spec()); a.load(saved);
    assert.equal(a.spec().parts.length,saved.parts.length,id);
  }
});
check('detached export cannot mutate live wiring or names',()=>{a.load(spec);const before=plain(a.spec());const out=a.spec();out.nodeNames.OUT.col=22;out.measurements[0].a='other';out.parts[0].terminals[0].col=40;assert.deepEqual(plain(a.spec()),before);});
check('paused edit invalidates old numbers',()=>{const withSwitch=plain(spec);withSwitch.parts.push({id:'SW',type:'switch',closed:false,terminals:[terminal('a',30),terminal('f',30)]});a.load(withSwitch);a.run(.1,.001);const t=a.receipt().timeSeconds;h.context.__toggleSwitchById('SW');assert.equal(a.receipt().status,'EDITED_PENDING');assert.equal(a.receipt().timeSeconds,t);assert.ok(a.run(.001,.001).measurements.Vcap>4.9,'switch editing must retain capacitor state');});
check('clear removes named-node metadata',()=>{a.load(spec);h.el('btnClear').dispatch('click');assert.deepEqual(plain(a.spec().nodeNames),{});assert.deepEqual(plain(a.spec().measurements),[]);});
check('save/load restores named measurement context',()=>{a.load(spec);h.el('btnSave').dispatch('click');h.el('btnClear').dispatch('click');h.el('btnLoad').dispatch('click');assert.deepEqual(plain(a.spec().nodeNames),spec.nodeNames);assert.equal(a.run(.001,.00001).measurements.Vcap,first.measurements.Vcap);});
check('unknown model params and duplicate holes are rejected',()=>{for (const mutate of [s=>s.parts[0].sourceR=5,s=>s.parts[1].terminals[1]=s.parts[1].terminals[0],s=>s.parts[0].type='hbridge']){const bad=plain(spec);mutate(bad);assert.throws(()=>a.load(bad));}});
check('receipts cannot mutate subsequent reported evidence',()=>{a.load(spec);const r=a.run(.001,.00001);r.run.steps=99999;r.warnings.push('invented');assert.equal(a.receipt().run.steps,100);assert.ok(!a.receipt().warnings.includes('invented'));});
check('non-midpoint potentiometer matches CLI',()=>{
  const pot={parts:[{id:'V',type:'battery',value:5,terminals:[terminal('e',10),terminal('f',12)]},{id:'POT',type:'potentiometer',value:10000,pos:0.2,terminals:[terminal('c',10)]}]};
  a.load(pot);const ui=a.run(.01,.001);
  const run=s=>spawnSync(process.execPath,['simulate.js'],{cwd:root,input:JSON.stringify({...s,sim:{seconds:.01,dt:.001}}),encoding:'utf8'});
  const cli=run(plain(a.spec()));assert.equal(cli.status,0,cli.stdout);assert.deepEqual(plain(ui.voltages),JSON.parse(cli.stdout).final.voltages);
  pot.parts[1].pos=2;assert.equal(run(pot).status,1);assert.throws(()=>a.load(pot));
});
check('same-node preset hole corrections preserve electrical topology',()=>{
  const Board=require('../js/board');const board=Board.build([{size:'large'}]);
  const id=(r,c)=>board.holes.find(h=>h.row===r&&h.col===c).cellId;
  for(const [r1,r2,c] of [['a','c',12],['a','e',16],['d','b',8]])assert.equal(id(r1,c),id(r2,c));
});
check('untrusted JSON markup is rejected atomically',()=>{
  a.load(spec);const before=plain(a.spec());
  for(const mutate of [s=>s.parts[3].id='x\" onmouseover=\"alert(1)',s=>s.parts[3].color='red;\"><img src=x onerror=alert(1)>']) {
    const bad=plain(spec);mutate(bad);assert.throws(()=>a.load(bad));assert.deepEqual(plain(a.spec()),before);
  }
});
check('finite integer windings only',()=>{
  for (const turns of ['Infinity',1.5,0,-1]) assert.throws(()=>a.load({parts:[{id:'T',type:'toroid',turns:[turns],terminals:[terminal('a',1),terminal('a',2)]}]}));
});
check('live frames advance and pause is repeatable',()=>{
 a.load(spec);a.resume();h.frame(300);const t=a.receipt().timeSeconds;assert.ok(t>0);a.pause();h.frame(400);assert.equal(a.receipt().timeSeconds,t);a.resume();h.frame(500);assert.ok(a.receipt().timeSeconds>t);a.pause();
});
console.log(`${checks} practice interface checks passed; visual browser QA remains separate.`);
