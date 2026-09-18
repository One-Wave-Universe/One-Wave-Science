import * as THREE from 'three';
import { OrbitControls } from './node_modules/three/examples/jsm/controls/OrbitControls.js';

const API={
  async get(path){const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw new Error(path+': '+r.status);return r.json();},
  async post(path,body){const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const data=await r.json();if(!r.ok||data.ok===false)throw new Error(data.error||path+': '+r.status);return data;}
};
const $=s=>document.querySelector(s);
const worldEl=$('#world'),bridgeStatus=$('#bridgeStatus'),worldStatus=$('#worldStatus'),agentList=$('#agentList');
const chatLog=$('#chatLog'),chatForm=$('#chatForm'),chatInput=$('#chatInput'),benchForm=$('#benchForm');
const benchName=$('#benchName'),benchAction=$('#benchAction'),benchSummary=$('#benchSummary'),benchFeed=$('#benchFeed');
const seqReadout=$('#seqReadout'),toastEl=$('#toast');

const renderer=new THREE.WebGLRenderer({antialias:false,powerPreference:'high-performance'});
renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,1));renderer.setSize(innerWidth,innerHeight);renderer.shadowMap.enabled=true;renderer.outputColorSpace=THREE.SRGBColorSpace;worldEl.appendChild(renderer.domElement);
const scene=new THREE.Scene();scene.background=new THREE.Color(0x050c11);scene.fog=new THREE.Fog(0x050c11,18,38);
const camera=new THREE.PerspectiveCamera(48,innerWidth/innerHeight,.1,100);camera.position.set(12,13,16);
const controls=new OrbitControls(camera,renderer.domElement);controls.target.set(0,.3,0);controls.enableDamping=true;controls.dampingFactor=.08;controls.maxPolarAngle=Math.PI*.48;controls.minDistance=7;controls.maxDistance=30;
scene.add(new THREE.HemisphereLight(0x9be9ff,0x0d1217,1.55));
const keyLight=new THREE.DirectionalLight(0xc9fbff,2.2);keyLight.position.set(4,12,6);keyLight.castShadow=true;scene.add(keyLight);
const rim=new THREE.PointLight(0xff72d6,20,18);rim.position.set(-7,4,-5);scene.add(rim);
const latticeGroup=new THREE.Group(),roomGroup=new THREE.Group(),avatarGroup=new THREE.Group();scene.add(latticeGroup,roomGroup,avatarGroup);

const raycaster=new THREE.Raycaster(),mouse=new THREE.Vector2(),benchMeshes=[],avatarObjects=new Map(),labelCache=new Map();
let manifest=null,state=null,localAgent=localStorage.getItem('miniverseAgentId')||'operator',activeBench=null,lastChatSeq=-1,lastBenchSeq=-1,toastTimer=null;
const palette={default:0x14303a,reference:0x1f6672,code:0x1d4d80,experiment:0x6b285f,review:0x5c4b1f,storage:0x3a4652,memory:0x3e2a71,router:0x1f6650};

function axialToWorld(q,r){const s=1.37;return new THREE.Vector3(s*Math.sqrt(3)*(q+r/2),0,s*1.5*r);}
function labelTexture(text,color,bg){
  color=color||'#9df7ff';bg=bg||'rgba(3,10,13,.92)';const key=text+'|'+color+'|'+bg;if(labelCache.has(key))return labelCache.get(key);
  const c=document.createElement('canvas');c.width=512;c.height=96;const ctx=c.getContext('2d');ctx.imageSmoothingEnabled=false;ctx.fillStyle=bg;ctx.fillRect(0,0,512,96);ctx.strokeStyle=color;ctx.lineWidth=5;ctx.strokeRect(3,3,506,90);ctx.fillStyle=color;ctx.font='bold 30px monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(text,256,48);
  const tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;tex.magFilter=THREE.NearestFilter;tex.minFilter=THREE.NearestFilter;labelCache.set(key,tex);return tex;
}
function makeLabel(text,color,scale){
  scale=scale||1;const mat=new THREE.MeshBasicMaterial({map:labelTexture(text,color),transparent:true,depthWrite:false,side:THREE.DoubleSide});const mesh=new THREE.Mesh(new THREE.PlaneGeometry(3.2*scale,.6*scale),mat);mesh.renderOrder=10;return mesh;
}
function addRoomShell(){
  const floor=new THREE.Mesh(new THREE.BoxGeometry(24,.35,20),new THREE.MeshStandardMaterial({color:0x07151b,roughness:.86,metalness:.2}));floor.position.y=-.35;floor.receiveShadow=true;roomGroup.add(floor);
  const wm=new THREE.MeshStandardMaterial({color:0x0b2029,roughness:.75,metalness:.25});const back=new THREE.Mesh(new THREE.BoxGeometry(24,3.5,.35),wm);back.position.set(0,1.35,-9.8);const left=new THREE.Mesh(new THREE.BoxGeometry(.35,3.5,20),wm);left.position.set(-11.8,1.35,0);roomGroup.add(back,left);
  const stripeMat=new THREE.MeshBasicMaterial({color:0x225969});for(let i=-10;i<=10;i+=2){const strip=new THREE.Mesh(new THREE.BoxGeometry(.95,.03,19.1),stripeMat);strip.position.set(i,-.15,0);roomGroup.add(strip);}
  const title=makeLabel('SANDBOX // MINIVERSE','#6df6ff',1.15);title.position.set(0,2.1,-9.55);roomGroup.add(title);
}
function makeBench(zone,position){
  const g=new THREE.Group(),base=palette[zone.kind]||palette.default,mat=new THREE.MeshStandardMaterial({color:base,roughness:.5,metalness:.5}),accent=new THREE.MeshBasicMaterial({color:zone.kind==='experiment'?0xff74dc:0x71f4ff});
  const desk=new THREE.Mesh(new THREE.BoxGeometry(2.2,.18,1),mat);desk.position.y=.55;desk.castShadow=true;
  const leg1=new THREE.Mesh(new THREE.BoxGeometry(.18,.55,.18),mat);leg1.position.set(-.8,.25,0);const leg2=leg1.clone();leg2.position.x=.8;
  const screen=new THREE.Mesh(new THREE.BoxGeometry(1.25,.7,.08),mat);screen.position.set(0,1.03,-.32);screen.rotation.x=-.18;
  const glow=new THREE.Mesh(new THREE.PlaneGeometry(1.05,.5),accent);glow.position.set(0,1.03,-.275);glow.rotation.x=-.18;
  [desk,leg1,leg2,screen,glow].forEach(m=>{m.userData.zoneId=zone.id;benchMeshes.push(m);g.add(m);});
  const label=makeLabel(zone.label,zone.kind==='experiment'?'#ff7edb':'#8df8ff',.62);label.position.set(0,1.65,0);g.add(label);g.position.copy(position);g.position.y=.05;g.lookAt(0,g.position.y,0);return g;
}
function buildLattice(){
  const zoneByCell=new Map(manifest.zones.map(z=>[z.cell,z])),hexGeo=new THREE.CylinderGeometry(1.22,1.22,.10,6),edgeGeo=new THREE.EdgesGeometry(hexGeo),edgeMat=new THREE.LineBasicMaterial({color:0x1d5b69,transparent:true,opacity:.7});
  manifest.cells.forEach(cell=>{
    const zone=zoneByCell.get(cell.id),kind=zone?zone.kind:'default',mat=new THREE.MeshStandardMaterial({color:palette[kind],roughness:.82,metalness:.18,emissive:zone?(palette[kind]||0):0,emissiveIntensity:zone?.13:0});
    const tile=new THREE.Mesh(hexGeo,mat);tile.position.copy(axialToWorld(cell.q,cell.r));tile.position.y=-.06;tile.receiveShadow=true;tile.userData.cellId=cell.id;const edges=new THREE.LineSegments(edgeGeo,edgeMat);edges.position.copy(tile.position);latticeGroup.add(tile,edges);
    if(zone){const p=axialToWorld(cell.q,cell.r);if(zone.kind==='reference'){const ring=new THREE.Mesh(new THREE.TorusGeometry(.92,.06,4,6),new THREE.MeshBasicMaterial({color:0x77f7ff}));ring.rotation.x=Math.PI/2;ring.position.copy(p);ring.position.y=.07;latticeGroup.add(ring);const label=makeLabel(zone.label,'#9affff',.6);label.position.copy(p).add(new THREE.Vector3(0,1.2,0));roomGroup.add(label);}else roomGroup.add(makeBench(zone,p));}
  });
  const grid=new THREE.GridHelper(23,23,0x173d46,0x0b2830);grid.position.y=-.12;roomGroup.add(grid);
}
function box(group,size,pos,color,emissive){
  const mat=new THREE.MeshStandardMaterial({color:color,roughness:.62,metalness:.15,emissive:emissive||0,emissiveIntensity:emissive?.42:0});const mesh=new THREE.Mesh(new THREE.BoxGeometry(...size),mat);mesh.position.set(...pos);mesh.castShadow=true;group.add(mesh);return mesh;
}
function makeAvatar(agent){
  const g=new THREE.Group(),c=new THREE.Color(agent.color||'#62e6ff').getHex(),dark=new THREE.Color(c).multiplyScalar(.42).getHex(),pale=new THREE.Color(c).lerp(new THREE.Color(0xffffff),.55).getHex();
  box(g,[.42,.5,.42],[-.23,.25,0],dark);box(g,[.42,.5,.42],[.23,.25,0],dark);box(g,[.95,.74,.52],[0,.85,0],c);box(g,[.2,.62,.24],[-.61,.86,0],dark);box(g,[.2,.62,.24],[.61,.86,0],dark);box(g,[.67,.62,.6],[0,1.54,0],pale);box(g,[.55,.16,.05],[0,1.58,.325],0x061015,0x7df8ff);box(g,[.12,.22,.12],[0,1.98,0],c);box(g,[.22,.1,.22],[0,2.09,0],0xffd45e,0xffd45e);
  const label=makeLabel(agent.name.toUpperCase(),agent.color||'#62e6ff',.52);label.position.set(0,2.52,0);g.add(label);g.scale.setScalar(.72);avatarGroup.add(g);return g;
}
function esc(v){return String(v??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[ch]));}
function updateAgents(agents){
  const ids=new Set(Object.keys(agents));avatarObjects.forEach((o,id)=>{if(!ids.has(id)){avatarGroup.remove(o);avatarObjects.delete(id);}});
  Object.values(agents).forEach(a=>{let o=avatarObjects.get(a.id);if(!o){o=makeAvatar(a);avatarObjects.set(a.id,o);}const qr=a.cell.split(',').map(Number),t=axialToWorld(qr[0],qr[1]);t.y=.15;o.userData.target=t;});
  agentList.innerHTML=Object.values(agents).map(a=>'<div class="agent"><span class="agent-dot" style="background:'+esc(a.color)+'"></span><span class="agent-name">'+esc(a.name)+'</span><span class="agent-role">'+esc(a.role)+' · '+esc(a.cell)+'</span></div>').join('')||'<div class="agent-role">No bodies connected.</div>';
}
function updateChat(chat){
  const newest=chat.length?chat[chat.length-1].seq:0;if(newest===lastChatSeq)return;lastChatSeq=newest;chatLog.innerHTML=chat.map(m=>'<div class="msg"><span class="msg-name">'+esc(m.name)+'</span><span class="agent-role"> '+esc(m.role)+'</span><br><span class="msg-text">'+esc(m.text)+'</span></div>').join('');chatLog.scrollTop=chatLog.scrollHeight;
}
function updateBenches(receipts){
  const newest=receipts.length?receipts[receipts.length-1].seq:0;if(newest===lastBenchSeq)return;lastBenchSeq=newest;benchFeed.innerHTML=receipts.slice(-8).reverse().map(r=>'<div class="receipt"><strong>'+esc(r.action)+'</strong> @ '+esc(r.bench_id)+'<br>'+esc(r.summary)+'</div>').join('');
}
function toast(msg){toastEl.textContent=msg;toastEl.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>toastEl.classList.remove('show'),1800);}
async function ensureLocalAgent(){await API.post('/api/join',{agent_id:localAgent,name:localAgent==='operator'?'OPERATOR':localAgent,role:'HUMAN / LOCAL',color:'#ffd36b'});localStorage.setItem('miniverseAgentId',localAgent);}
async function poll(){
  try{const p=await API.get('/api/state');manifest=p.manifest;state=p.state;bridgeStatus.textContent='BRIDGE: LIVE';bridgeStatus.style.color='#98ffb4';worldStatus.textContent='LATTICE: '+manifest.cells.length+' CELLS / '+manifest.zones.length+' ZONES';seqReadout.textContent='SEQ '+state.seq;updateAgents(state.agents);updateChat(state.chat);updateBenches(state.bench_receipts);}
  catch(e){bridgeStatus.textContent='BRIDGE: OFFLINE';bridgeStatus.style.color='#ff6f79';}
}
async function init(){const p=await API.get('/api/state');manifest=p.manifest;state=p.state;addRoomShell();buildLattice();await ensureLocalAgent();await poll();setInterval(poll,700);}
chatForm.addEventListener('submit',async e=>{e.preventDefault();const text=chatInput.value.trim();if(!text)return;try{await API.post('/api/say',{agent_id:localAgent,text:text});chatInput.value='';await poll();}catch(err){toast(err.message);}});
benchForm.addEventListener('submit',async e=>{e.preventDefault();if(!activeBench)return toast('CLICK A WORKBENCH FIRST');const summary=benchSummary.value.trim();if(!summary)return;try{await API.post('/api/bench',{agent_id:localAgent,bench_id:activeBench,action:benchAction.value,summary:summary});benchSummary.value='';await poll();}catch(err){toast(err.message);}});
const keyMap={KeyD:'A+',KeyE:'B+',KeyW:'C+',KeyA:'A-',KeyQ:'B-',KeyS:'C-'};
addEventListener('keydown',async e=>{if(e.target.matches('textarea,input,select'))return;const direction=keyMap[e.code];if(!direction)return;e.preventDefault();try{await API.post('/api/move',{agent_id:localAgent,direction:direction});await poll();}catch(err){toast(err.message);}});
renderer.domElement.addEventListener('pointerdown',e=>{const rect=renderer.domElement.getBoundingClientRect();mouse.x=((e.clientX-rect.left)/rect.width)*2-1;mouse.y=-((e.clientY-rect.top)/rect.height)*2+1;raycaster.setFromCamera(mouse,camera);const hits=raycaster.intersectObjects(benchMeshes,false);if(hits.length){activeBench=hits[0].object.userData.zoneId;const zone=manifest.zones.find(z=>z.id===activeBench);benchName.textContent=zone?zone.label:activeBench;toast('BENCH SELECTED: '+benchName.textContent);}});
addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);});
const clock=new THREE.Clock();
function animate(){requestAnimationFrame(animate);const dt=Math.min(clock.getDelta(),.05);avatarObjects.forEach(o=>{if(o.userData.target)o.position.lerp(o.userData.target,1-Math.pow(.002,dt));});controls.update();renderer.render(scene,camera);}
init().catch(e=>{bridgeStatus.textContent='BRIDGE: START FAILED';bridgeStatus.style.color='#ff6f79';toast(e.message);});animate();
