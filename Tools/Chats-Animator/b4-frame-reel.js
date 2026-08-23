(() => {
  const A = window.OneWaveAnimator;
  if (!A) throw new Error('app.js must load before b4-frame-reel.js');
  const REEL_KEY = 'one-wave-video-maker-b8-reel';
  const $ = (id) => document.getElementById(id);
  const clone = A.clone;
  let reel;
  try { reel = JSON.parse(localStorage.getItem(REEL_KEY) || 'null'); } catch (_) { reel = null; }
  if (!reel || !Array.isArray(reel.frames) || !reel.frames.length) reel = { activeIndex:0, frames:[{id:makeId(),hold:2,snapshot:snapshot()}] };
  reel.activeIndex = Math.max(0, Math.min(reel.activeIndex || 0, reel.frames.length - 1));

  function makeId(){ return crypto.randomUUID?.() || `frame-${Date.now()}-${Math.random()}`; }
  function snapshot(){ return clone({ background:A.state.background, calibration:A.state.calibration, calibrationSaved:A.state.calibrationSaved, assets:A.state.assets, selectedAssetId:A.state.selectedAssetId }); }
  function restore(s){
    const x = clone(s); A.state.background=x.background||null; A.state.calibration=x.calibration||A.state.calibration; A.state.calibrationSaved=!!x.calibrationSaved; A.state.assets=x.assets||[]; A.state.selectedAssetId=x.selectedAssetId||null; A.renderAll(); A.saveState();
  }
  function saveReel(){ localStorage.setItem(REEL_KEY, JSON.stringify(reel)); window.dispatchEvent(new CustomEvent('onewave:reel-changed',{detail:{reel:clone(reel)}})); }
  function saveCurrent(){ const f=reel.frames[reel.activeIndex]; if(f) f.snapshot=snapshot(); saveReel(); }
  function select(index){ if(index<0||index>=reel.frames.length)return; saveCurrent(); reel.activeIndex=index; restore(reel.frames[index].snapshot); render(); saveReel(); window.dispatchEvent(new CustomEvent('onewave:frame-selected',{detail:{index}})); }
  function render(){
    const list=$('frame-reel'); list.innerHTML='';
    reel.frames.forEach((f,i)=>{ const b=document.createElement('button'); b.type='button'; b.className='frame-card'+(i===reel.activeIndex?' active':''); b.innerHTML=`<strong>Frame ${i+1}</strong><span>${f.hold || 2}x hold</span>`; b.addEventListener('click',()=>select(i)); list.appendChild(b); });
    $('active-frame-label').textContent=`Frame ${reel.activeIndex+1}`; const hold=reel.frames[reel.activeIndex]?.hold||2; $('frame-hold').value=hold; $('frame-hold-value').textContent=`${hold}x`;
  }
  function addFrame(after=true, duplicate=false){ saveCurrent(); const base=reel.frames[reel.activeIndex]; const f={id:makeId(),hold:base?.hold||2,snapshot:duplicate?clone(base.snapshot):snapshot()}; const at=reel.activeIndex+(after?1:0); reel.frames.splice(at,0,f); reel.activeIndex=at; restore(f.snapshot); render(); saveReel(); return at; }
  function deleteFrame(){ if(reel.frames.length===1){ reel.frames[0]={id:makeId(),hold:2,snapshot:snapshot()}; reel.activeIndex=0; } else { reel.frames.splice(reel.activeIndex,1); reel.activeIndex=Math.min(reel.activeIndex,reel.frames.length-1); restore(reel.frames[reel.activeIndex].snapshot); } render(); saveReel(); }

  $('add-frame').addEventListener('click',()=>addFrame(true,false)); $('duplicate-frame').addEventListener('click',()=>addFrame(true,true)); $('delete-frame').addEventListener('click',deleteFrame);
  $('frame-hold').addEventListener('input',(e)=>{ const v=Number(e.target.value); reel.frames[reel.activeIndex].hold=v; $('frame-hold-value').textContent=`${v}x`; saveReel(); });
  window.addEventListener('onewave:state-changed',()=>{ const f=reel.frames[reel.activeIndex]; if(f) { f.snapshot=snapshot(); saveReel(); } });

  window.b4Reel = reel; window.b4Snapshot=snapshot; window.b4Restore=restore; window.b4RenderFrames=render; window.b4SaveCurrentFrame=saveCurrent; window.b4SaveReel=saveReel; window.b4SelectFrame=select; window.b4AddFrame=addFrame;
  restore(reel.frames[reel.activeIndex].snapshot); render();
})();
