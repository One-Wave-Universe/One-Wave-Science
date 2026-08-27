(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('C15 motion atlas requires Animator + reel');
  const $ = id => document.getElementById(id);
  const aside = document.querySelector('aside');
  if (!aside) return;

  const FORMAT = 'one-wave-motion-atlas';
  const VERSION = 1;
  const DIRECTIONS = ['ANY','N','NE','E','SE','S','SW','W','NW'];
  const CATEGORIES = ['all','locomotion','jump-fall','interaction','gesture','acting','face','speech-mouth'];

  let atlas = { format:FORMAT, version:VERSION, character:'Goblin Raccoon', variant:'base', fps:24, catalog:[], motionProfile:null, sequences:[] };

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>C15 Full Motion Atlas</strong><br>
    Browse large reusable PNG motion libraries: walk/run in 8 directions, jumps, rolls, gestures, acting, facial expressions, and speech mouths.
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">
      <button id="c15-open" type="button">Open .owatlas</button>
      <button id="c15-save" type="button">Save .owatlas</button>
      <input id="c15-file" type="file" accept=".owatlas,.json,application/json" hidden>
    </div>
    <div style="margin-top:8px"><label>Character <input id="c15-character" value="Goblin Raccoon" style="width:100%"></label></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px">
      <label>Category<select id="c15-category" style="width:100%"></select></label>
      <label>Direction<select id="c15-direction" style="width:100%"></select></label>
    </div>
    <div style="margin-top:8px"><label>Search <input id="c15-search" placeholder="walk, angry, roll..." style="width:100%"></label></div>
    <div id="c15-stats" style="margin-top:8px"></div>
    <div id="c15-results" style="margin-top:8px;max-height:440px;overflow:auto"></div>`;
  aside.insertBefore(panel, aside.firstChild);

  CATEGORIES.forEach(x => { const o=document.createElement('option'); o.value=x; o.textContent=x; $('c15-category').appendChild(o); });
  DIRECTIONS.forEach(x => { const o=document.createElement('option'); o.value=x; o.textContent=x; $('c15-direction').appendChild(o); });

  function uid(prefix='seq'){ return A.uid ? A.uid(prefix) : `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2)}`; }
  function sanitizeFrame(frame){ return {snapshot:A.clone(frame.snapshot||frame),hold:Math.max(1,Math.min(24,Number(frame.hold)||2)),anchor:frame.anchor||null,markers:frame.markers||null}; }
  function sanitizeSequence(seq={}){
    return {id:String(seq.id||uid()),name:String(seq.name||seq.action||'Untitled sequence').slice(0,120),character:String(seq.character||atlas.character||'Character').slice(0,80),category:CATEGORIES.includes(seq.category)&&seq.category!=='all'?seq.category:'acting',action:String(seq.action||seq.name||'action').slice(0,80),direction:DIRECTIONS.includes(seq.direction)&&seq.direction!=='ANY'?seq.direction:'S',variant:String(seq.variant||'default').slice(0,80),loop:Boolean(seq.loop),fps:24,tags:Array.isArray(seq.tags)?seq.tags.slice(0,30).map(String):[],notes:String(seq.notes||'').slice(0,1000),frames:Array.isArray(seq.frames)?seq.frames.map(sanitizeFrame):[]};
  }
  function validate(next){
    if(!next||next.format!==FORMAT||Number(next.version)!==VERSION) throw new Error('Unsupported motion atlas');
    if(!Array.isArray(next.sequences)) throw new Error('Atlas has no sequence list');
    return {format:FORMAT,version:VERSION,character:String(next.character||'Character').slice(0,80),variant:String(next.variant||'base').slice(0,80),fps:24,catalog:Array.isArray(next.catalog)?next.catalog.slice(0,1000).map(x=>String(x).slice(0,120)):[],motionProfile:next.motionProfile&&typeof next.motionProfile==='object'?A.clone(next.motionProfile):null,sequences:next.sequences.map(sanitizeSequence)};
  }
  function ticks(seq){ return seq.frames.reduce((n,f)=>n+Math.max(1,Number(f.hold)||1),0); }
  function filtered(){
    const cat=$('c15-category').value, dir=$('c15-direction').value, q=$('c15-search').value.trim().toLowerCase();
    return atlas.sequences.filter(seq=>{ if(cat!=='all'&&seq.category!==cat)return false; if(dir!=='ANY'&&seq.direction!==dir)return false; if(q&&!`${seq.name} ${seq.action} ${seq.variant} ${(seq.tags||[]).join(' ')}`.toLowerCase().includes(q))return false; return true; });
  }
  function render(){
    $('c15-character').value=atlas.character;
    const seqs=filtered();
    const totalPngFrames=atlas.sequences.reduce((n,s)=>n+s.frames.length,0);
    const builtNames=new Set(atlas.sequences.map(s=>String(s.action||s.name).toLowerCase()));
    const catalogTotal=atlas.catalog.length;
    const catalogDone=atlas.catalog.reduce((n,name)=>n+(builtNames.has(String(name).toLowerCase())?1:0),0);
    const progress=catalogTotal?` • catalog ${catalogDone}/${catalogTotal}`:'';
    $('c15-stats').textContent=`${atlas.character}${atlas.variant&&atlas.variant!=='base'?` [${atlas.variant}]`:''} • ${atlas.sequences.length} sequences • ${totalPngFrames} PNG/frame poses${progress} • showing ${seqs.length}`;
    const box=$('c15-results'); box.innerHTML='';
    if(!seqs.length){ box.textContent='No matching completed sequences yet.'; return; }
    seqs.forEach(seq=>{
      const row=document.createElement('div'); row.className='card';
      row.innerHTML=`<strong>${seq.name}</strong><br>${seq.category} • ${seq.direction} • ${seq.frames.length} drawings • ${ticks(seq)} ticks @ 24 fps ${seq.loop?'• loop':''}<br><small>${seq.variant}${seq.tags.length?' • '+seq.tags.join(', '):''}</small><div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:6px"><button data-insert="${seq.id}" type="button">Insert into Reel</button><button data-delete="${seq.id}" type="button">Delete</button></div>`;
      box.appendChild(row);
    });
    box.querySelectorAll('[data-insert]').forEach(btn=>btn.addEventListener('click',()=>insertSequence(btn.dataset.insert)));
    box.querySelectorAll('[data-delete]').forEach(btn=>btn.addEventListener('click',()=>{atlas.sequences=atlas.sequences.filter(s=>s.id!==btn.dataset.delete);render();}));
  }
  function insertSequence(id){
    const seq=atlas.sequences.find(s=>s.id===id); if(!seq||!seq.frames.length)return A.status('Sequence has no frames');
    R.captureCurrent(); const insertAt=Math.min(R.frames.length,R.activeIndex+1); const frames=seq.frames.map(f=>({snapshot:A.clone(f.snapshot),hold:Math.max(1,Number(f.hold)||1)}));
    R.setFrames([...R.frames.slice(0,insertAt),...frames,...R.frames.slice(insertAt)],insertAt); A.status(`${seq.name}: inserted ${frames.length} drawings`);
  }
  function addSequence(sequence){ atlas.sequences.push(sanitizeSequence(sequence)); render(); }
  function captureReelRange({name='Captured sequence',category='acting',action='action',direction='S',variant='default',loop=false,start=R.activeIndex,count=1,tags=[]}={}){
    R.captureCurrent(); const frames=R.frames.slice(Math.max(0,start),Math.min(R.frames.length,Math.max(0,start)+Math.max(1,count))); if(!frames.length)throw new Error('No reel frames to capture'); addSequence({name,category,action,direction,variant,loop,tags,frames:A.clone(frames),character:atlas.character});
  }
  function save(){
    atlas.character=$('c15-character').value.trim()||atlas.character; const blob=new Blob([JSON.stringify(atlas,null,2)],{type:'application/json'}); const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download=`${atlas.character.replace(/[^a-z0-9_-]+/gi,'-').toLowerCase()}-motion-atlas.owatlas`; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(url),0); A.status(`Motion atlas saved: ${atlas.sequences.length} sequences`);
  }
  async function openFile(file){ atlas=validate(JSON.parse(await file.text())); render(); A.status(`Motion atlas opened: ${atlas.character} — ${atlas.sequences.length} completed sequences`); }
  function loadData(data){ atlas=validate(data); render(); return A.clone(atlas); }

  $('c15-category').addEventListener('change',render); $('c15-direction').addEventListener('change',render); $('c15-search').addEventListener('input',render); $('c15-character').addEventListener('change',e=>{atlas.character=e.target.value.trim()||atlas.character;}); $('c15-save').addEventListener('click',save); $('c15-open').addEventListener('click',()=>$('c15-file').click());
  $('c15-file').addEventListener('change',async e=>{const file=e.target.files?.[0];if(!file)return;try{await openFile(file);}catch(err){console.error(err);A.status(`Atlas open failed: ${err.message}`);}finally{e.target.value='';}});

  A.motionAtlas={get atlas(){return A.clone(atlas);},addSequence,captureReelRange,insertSequence,save,openFile,loadData,validate,render};
  render();

  if (!A.motionRoster && !document.querySelector('script[data-c16-motion-roster]')) {
    const script = document.createElement('script');
    script.src = './c16-character-motion-roster.js';
    script.setAttribute('data-c16-motion-roster','true');
    document.body.appendChild(script);
  }
})();
