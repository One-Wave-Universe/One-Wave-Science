'use strict';
const $ = id => document.getElementById(id);
let state = null, busy = false, running = false, timer = null;
function hydrate(data){
  $('model').value=data.model;
  for(const id of ['control','side','norm','kick','mode'])if(data.config[id]!==undefined)$(id).value=data.config[id];
  if(data.drive)for(const [j,id] of ['forceX','forceY','forceZ'].entries())$(id).value=data.drive.force_coefficients[j];
  $('forcePending').textContent='Push controls match the active force.';
  $('pending').textContent='Settings match the active experiment.';configVisibility();
}
for(const id of ['model','control','side','norm','kick','mode'])$(id).addEventListener('change',()=>{$('pending').textContent='Settings changed. Start / reset to apply; current experiment is unchanged.';});
const initialCamera = () => ({yaw:.65,pitch:.4,zoom:1,panX:0,panY:0});
let camera = initialCamera();
const canvas=$('view'), ctx=canvas.getContext('2d');
const fmt = n => Number(n).toPrecision(6);
function syncControls(){
  for(const id of ['reset','step','shiftPlus','shiftMinus','export','model','control','side','norm','kick','mode','forceX','forceY','forceZ','applyForce','clearForce']) $(id).disabled=busy;
  $('run').textContent=running?'Pause':'Run';
  $('run').disabled=busy&&!running;
}
function stop(){running=false; clearTimeout(timer); syncControls();}
function configVisibility(){const cavity=$('model').value==='cavity';$('bulkControls').classList.toggle('hidden',cavity);$('cavityControls').classList.toggle('hidden',!cavity);}
$('model').onchange=configVisibility;
for(const id of ['forceX','forceY','forceZ'])$(id).addEventListener('input',()=>{$('forcePending').textContent='Push edits pending. Apply push to change the active force.';});
async function request(command){
  if(busy) return;
  busy=true;syncControls();$('error').textContent='';
  try{
    const response=await fetch(command?'/api/command':'/api/state',command?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(command)}:{});
    const data=await response.json();if(!response.ok)throw Error(data.error||'Request failed');
    if(!state||command?.action==='reset')hydrate(data);
    if(command?.action==='set_force'){for(const [j,id] of ['forceX','forceY','forceZ'].entries())$(id).value=data.drive.force_coefficients[j];$('forcePending').textContent='Push controls match the active force.';}
    state=data;render();
    if(state.source_drift.length){stop();$('error').textContent='Source files changed after startup. Restart the lab before further work: '+state.source_drift.join(', ');}$('status').textContent=`${running?'Running':'Paused'} · generation ${state.generation} · step ${state.step}`;
  }catch(error){stop();$('error').textContent=error.message;}
  finally{busy=false;syncControls();}
}
async function tick(){if(!running)return;await request({action:'step',count:5});if(running)timer=setTimeout(tick,50);}
$('run').onclick=()=>{if(running){stop();$('status').textContent='Paused';}else{running=true;syncControls();tick();}};
$('step').onclick=()=>{stop();request({action:'step',count:5});};
$('reset').onclick=()=>{stop();const model=$('model').value;const params=model==='bulk'?{model,control:$('control').value,side:+$('side').value,norm:+$('norm').value,kick:+$('kick').value}:{model,mode:+$('mode').value};request({action:'reset',...params});};
$('applyForce').onclick=()=>{stop();request({action:'set_force',force:['forceX','forceY','forceZ'].map(id=>+$(id).value)});};
$('clearForce').onclick=()=>{stop();request({action:'set_force',force:[0,0,0]});};
$('shiftPlus').onclick=()=>{stop();request({action:'displace',shift:[1,1,0]});};
$('shiftMinus').onclick=()=>{stop();request({action:'displace',shift:[-1,-1,0]});};
$('export').onclick=()=>{if(!state)return;const blob=new Blob([JSON.stringify(state,null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`field-${state.model}-${state.generation}-${state.step}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);};
function size(c){const r=c.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);c.width=Math.round(r.width*d);c.height=Math.round(r.height*d);return [c.width,c.height];}
function project(p,w,h,extent){
  const cy=Math.cos(camera.yaw),sy=Math.sin(camera.yaw),cp=Math.cos(camera.pitch),sp=Math.sin(camera.pitch);
  const x=cy*p[0]-sy*p[2],z=sy*p[0]+cy*p[2],y=cp*p[1]-sp*z,depth=sp*p[1]+cp*z;
  const perspective=5*extent/(5*extent+depth),scale=Math.min(w,h)*.35/extent*camera.zoom;
  return [w/2+camera.panX*w+x*scale*perspective,h/2+camera.panY*h-y*scale*perspective,depth,perspective];
}
function draw(){
  const [w,h]=size(canvas);ctx.clearRect(0,0,w,h);if(!state)return;
  const extent=Math.max(1,...state.xyz.flat().map(Math.abs)),role=$('role').value;
  const dots=state.xyz.map((p,i)=>{let intensity=0,re=0,im=0;for(let a=0;a<4;a++)if(role==='all'||+role===a){const r=state.real[i][a],v=state.imag[i][a];intensity+=r*r+v*v;re+=r;im+=v;}return {p:project(p,w,h,extent),intensity,phase:Math.atan2(im,re)};}).sort((a,b)=>b.p[2]-a.p[2]);
  const max=Math.max(1e-12,...dots.map(d=>d.intensity));
  const origin=project([0,0,0],w,h,extent);
  ['x','y','z'].forEach((label,j)=>{const xyz=[0,0,0];xyz[j]=extent;const p=project(xyz,w,h,extent);ctx.strokeStyle=['#ca7e8a','#80b792','#81aaca'][j];ctx.beginPath();ctx.moveTo(origin[0],origin[1]);ctx.lineTo(p[0],p[1]);ctx.stroke();ctx.fillStyle=ctx.strokeStyle;ctx.font=`${14*(devicePixelRatio||1)}px system-ui`;ctx.fillText(label,p[0]+5,p[1]);});
  for(const dot of dots){const v=Math.sqrt(dot.intensity/max),hue=((dot.phase/(2*Math.PI)+1)%1)*360;ctx.globalAlpha=.15+.85*v;ctx.fillStyle=`hsl(${hue},75%,65%)`;ctx.beginPath();ctx.arc(dot.p[0],dot.p[1],Math.max(1,(1+7*v)*dot.p[3]*(devicePixelRatio||1)),0,2*Math.PI);ctx.fill();}
  ctx.globalAlpha=1;ctx.fillStyle='#abc4d9';ctx.font=`${12*(devicePixelRatio||1)}px system-ui`;ctx.fillText(`${state.xyz.length} native sites · max intensity ${fmt(max)} · zoom ${camera.zoom.toFixed(2)}×`,14,24*(devicePixelRatio||1));
}
function render(){
  const rows=[['Model',state.model],['Simulation time',fmt(state.time)],['Fixed timestep',fmt(state.dt)],['Internal numerical energy',fmt(state.energy)],['Internal energy change',fmt(state.energy_change)]];
  if(state.model==='bulk')rows.push(['Norm',fmt(state.measurements.norm)],['Norm relative error',fmt(state.norm_relative_error)],['RMS radius',fmt(state.measurements.rms_radius)],['Core fraction r≤2',fmt(state.measurements.core_fraction_r2)],['Origin detector r≤1',fmt(state.detector.intensity)],['Imposed shift',state.imposed_lattice_shift.map(n=>n.toFixed(3)).join(', ')]);
  if(state.drive){const d=state.drive,c=d.centroid;rows.push(['Active force coefficients',d.force_coefficients.map(n=>n.toFixed(3)).join(', ')],['Applied force',d.applied_force.map(fmt).join(', ')],['Total energy',fmt(d.total_energy)],['Switch work',fmt(d.switch_work)],['Translation work',fmt(d.intervention_work)],['Energy − initial − work',fmt(d.energy_balance_residual)],['Centroid displacement',c.displacement?c.displacement.map(n=>n.toExponential(2)).join(', '):'unresolved'],['Chart seam diagnostic',fmt(c.displacement_branch_uncertainty)],['Motion status',c.geometrically_resolved?'Chart policy passed; refine timestep':'Unresolved by chart policy']);}
  $('readouts').replaceChildren();for(const [key,value] of rows){const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=key;dd.textContent=value;$('readouts').append(dt,dd);}
  $('displacement').classList.toggle('hidden',state.model!=='bulk');$('forceDrive').classList.toggle('hidden',state.model!=='bulk');$('response').classList.toggle('hidden',!state.response);
  if(state.response){$('tensor').textContent=state.response.tensor.map((row,i)=>'xyz'[i]+': '+row.map(n=>Number(n).toExponential(2)).join('  ')).join('\n');$('probe').textContent=`Finite-difference diagonal: ${state.response.energy_fd_diagonal.map(fmt).join(', ')}. Max discrepancy ${fmt(state.response.max_diagonal_error)}. Velocity probe ±${state.response.probe_speed}; model units.`;}
  $('phaseLegend').textContent=state.model==='bulk'?'Hue: coherent phase':'Hue: real cavity sign (0 or π)';
  $('scope').textContent=state.model==='bulk'?'The actual complex field evolves; intensity, phase, detector output and numerical energy are sampled from those arrays. The phase kick is an initial condition, not calibrated velocity. '+(state.drive.centroid.valid?'Centroid uses an unwrapped ordinary norm-weighted chart.':'Centroid unavailable: '+state.drive.centroid.reason+'.'):'The actual cavity mode evolves under the existing H/W recurrence. Its carried-profile energy curvature is a separate cycle-averaged diagnostic using the same selected mode and operator; it is not a force-driven translated particle.';
  $('boundary').textContent=state.boundary;$('sources').textContent=Object.entries(state.source_sha256).map(([p,h])=>`${p}\nSHA-256 ${h}`).join('\n\n');draw();plot();
}
function plot(){const c=$('plot'),[w,h]=size(c),g=c.getContext('2d'),rows=state.trace.map(row=>({...row,energy:row.total_energy??row.energy}));g.clearRect(0,0,w,h);const es=rows.map(r=>r.energy),lo=Math.min(...es),hi=Math.max(...es),range=Math.max(1e-9,hi-lo);g.strokeStyle='#77dac5';g.beginPath();rows.forEach((r,i)=>{const x=10+(w-20)*(r.time-rows[0].time)/Math.max(state.dt,rows[rows.length-1].time-rows[0].time),y=h-12-(h-24)*(r.energy-lo)/range;i?g.lineTo(x,y):g.moveTo(x,y);});g.stroke();$('plotLabel').textContent=`Total numerical energy vs simulated time · ${rows.length} samples · range ${fmt(lo)} … ${fmt(hi)}`;}
function zoom(factor){camera.zoom=Math.max(.2,Math.min(8,camera.zoom*factor));draw();}
$('zoomIn').onclick=()=>zoom(1.2);$('zoomOut').onclick=()=>zoom(1/1.2);$('cameraReset').onclick=()=>{camera=initialCamera();draw();};$('role').onchange=draw;
let drag=null;
canvas.onpointerdown=e=>{drag={x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId);};
canvas.onpointermove=e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(e.shiftKey){camera.panX+=dx/canvas.clientWidth;camera.panY+=dy/canvas.clientHeight;}else{camera.yaw+=dx*.008;camera.pitch=Math.max(-1.5,Math.min(1.5,camera.pitch+dy*.008));}drag={x:e.clientX,y:e.clientY};draw();};
canvas.onpointerup=canvas.onpointercancel=()=>drag=null;
canvas.addEventListener('wheel',e=>{e.preventDefault();zoom(Math.exp(-e.deltaY*.001));},{passive:false});
canvas.onkeydown=e=>{if(e.key==='+'||e.key==='=')zoom(1.2);else if(e.key==='-')zoom(1/1.2);else if(e.key.startsWith('Arrow')){e.preventDefault();camera.yaw+=(e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0)*.1;camera.pitch=Math.max(-1.5,Math.min(1.5,camera.pitch+(e.key==='ArrowUp'?-1:e.key==='ArrowDown'?1:0)*.1));draw();}};
window.addEventListener('resize',()=>{draw();if(state)plot();});
request();
