(() => {
  const STORAGE_KEY = 'one-wave-video-maker-b8';
  const legacyKeys = ['one-wave-video-maker-b7','one-wave-video-maker-b6','one-wave-video-maker-b5','one-wave-video-maker-b4','one-wave-video-maker-b3','one-wave-video-maker-b2','one-wave-video-maker-b1'];
  const defaultCalibration = { horizonY: 0.36, groundFarY: 0.48, groundNearY: 0.92, nearScale: 1, farScale: 0.35 };
  const defaultState = { background: null, calibration: { ...defaultCalibration }, calibrationSaved: false, assets: [], selectedAssetId: null, placementMode: false };

  function clone(v){ return JSON.parse(JSON.stringify(v)); }
  function loadState(){
    const keys = [STORAGE_KEY, ...legacyKeys];
    for (const key of keys) {
      try {
        const raw = localStorage.getItem(key);
        if (raw) return { ...clone(defaultState), ...JSON.parse(raw), calibration: { ...defaultCalibration, ...(JSON.parse(raw).calibration || {}) } };
      } catch (_) {}
    }
    return clone(defaultState);
  }

  const state = loadState();
  const $ = (id) => document.getElementById(id);
  const stage = $('scene-stage');
  const bg = $('scene-background');
  const placeholder = $('background-placeholder');
  const overlay = $('calibration-overlay');
  const assetLayer = $('asset-layer');
  const status = $('runtime-status');

  function saveState(){
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    window.dispatchEvent(new CustomEvent('onewave:state-changed', { detail: { state: clone(state) } }));
  }
  function setStatus(text){ if (status) status.textContent = text; }
  function selectedAsset(){ return state.assets.find(a => a.id === state.selectedAssetId) || null; }
  function depthScale(asset){
    const c = state.calibration;
    const span = Math.max(0.0001, c.groundNearY - c.groundFarY);
    const t = Math.max(0, Math.min(1, (asset.groundY - c.groundFarY) / span));
    return c.farScale + (c.nearScale - c.farScale) * t;
  }
  function renderBackground(){
    if (state.background?.dataUrl) {
      bg.src = state.background.dataUrl; bg.hidden = false; placeholder.hidden = true;
      $('background-meta').textContent = `${state.background.name || 'Background'} · ${state.background.width || '?'}×${state.background.height || '?'}`;
    } else {
      bg.hidden = true; bg.removeAttribute('src'); placeholder.hidden = false; $('background-meta').textContent = 'No background loaded';
    }
  }
  function renderCalibration(){
    const c = state.calibration;
    const show = !overlay.hidden;
    if (!show) return;
    const h = c.horizonY * 100, f = c.groundFarY * 100, n = c.groundNearY * 100;
    overlay.innerHTML = `<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
      <line class="horizon-line" x1="0" y1="${h}" x2="100" y2="${h}"/>
      <line class="edge-line" x1="0" y1="${n}" x2="50" y2="${h}"/><line class="edge-line" x1="100" y1="${n}" x2="50" y2="${h}"/>
      <line class="grid-line" x1="0" y1="${f}" x2="100" y2="${f}"/><line class="grid-line" x1="0" y1="${n}" x2="100" y2="${n}"/>
      <line class="grid-line" x1="25" y1="${n}" x2="50" y2="${h}"/><line class="grid-line" x1="75" y1="${n}" x2="50" y2="${h}"/>
    </svg>`;
  }
  function renderAssets(){
    assetLayer.innerHTML = '';
    for (const asset of state.assets) {
      const img = document.createElement('img');
      img.className = 'scene-asset' + (asset.id === state.selectedAssetId ? ' selected' : '');
      img.src = asset.dataUrl; img.alt = asset.name || asset.kind || 'asset'; img.dataset.assetId = asset.id;
      const scale = depthScale(asset) * (asset.manualScale || 1);
      img.style.left = `${asset.x * 100}%`; img.style.bottom = `${(1 - asset.groundY) * 100}%`;
      img.style.width = `${Math.max(3, 22 * scale)}%`; img.style.transform = 'translate(-50%, 0)';
      img.addEventListener('click', (e) => { e.stopPropagation(); state.selectedAssetId = asset.id; renderAll(); saveState(); });
      assetLayer.appendChild(img);
    }
  }
  function syncControls(){
    const c = state.calibration;
    const pairs = [['horizon-y','horizonY',2],['ground-far-y','groundFarY',2],['ground-near-y','groundNearY',2],['near-scale','nearScale',2],['far-scale','farScale',2]];
    for (const [id,key,d] of pairs) { const el=$(id); if(el){ el.value=c[key]; const out=$(id+'-value'); if(out) out.textContent=Number(c[key]).toFixed(d); } }
    $('calibration-state').textContent = state.calibrationSaved ? 'Calibration saved' : 'Calibration needs save/review';
    const a = selectedAsset(); $('no-selection').hidden = !!a; $('selected-controls').hidden = !a;
    if (a) {
      $('selected-name').textContent = a.name || a.kind;
      $('asset-x').value = a.x; $('asset-x-value').textContent = Number(a.x).toFixed(2);
      $('asset-ground-y').value = a.groundY; $('asset-ground-y-value').textContent = Number(a.groundY).toFixed(2);
      $('asset-manual-scale').value = a.manualScale || 1; $('asset-manual-scale-value').textContent = Number(a.manualScale || 1).toFixed(2);
      $('auto-scale-value').textContent = depthScale(a).toFixed(2);
    }
  }
  function renderAll(){ renderBackground(); renderCalibration(); renderAssets(); syncControls(); }
  function readFileAsDataURL(file){ return new Promise((resolve,reject)=>{ const r=new FileReader(); r.onload=()=>resolve(r.result); r.onerror=reject; r.readAsDataURL(file); }); }
  function imageDimensions(dataUrl){ return new Promise((resolve,reject)=>{ const i=new Image(); i.onload=()=>resolve({width:i.naturalWidth,height:i.naturalHeight}); i.onerror=reject; i.src=dataUrl; }); }
  async function addAssetFromFile(file, kind){
    const dataUrl = await readFileAsDataURL(file); const d = await imageDimensions(dataUrl);
    const asset = { id: crypto.randomUUID?.() || `asset-${Date.now()}-${Math.random()}`, kind, name:file.name, dataUrl, width:d.width, height:d.height, x:0.5, groundY:0.72, manualScale:1 };
    state.assets.push(asset); state.selectedAssetId = asset.id; state.placementMode = true; overlay.hidden = false; renderAll(); saveState(); setStatus(`${kind} added`); return asset;
  }
  function wirePicker(buttonId,pickerId,kind){ $(buttonId).addEventListener('click',()=>$(pickerId).click()); $(pickerId).addEventListener('change',async(e)=>{ const f=e.target.files?.[0]; if(f) await addAssetFromFile(f,kind); e.target.value=''; }); }

  $('load-background').addEventListener('click',()=> $('background-picker').click());
  $('background-picker').addEventListener('change', async (e)=>{ const f=e.target.files?.[0]; if(!f)return; const dataUrl=await readFileAsDataURL(f); const d=await imageDimensions(dataUrl); state.background={name:f.name,dataUrl,width:d.width,height:d.height}; state.calibrationSaved=false; renderAll(); saveState(); setStatus('Background loaded — calibration review required'); e.target.value=''; });
  $('clear-background').addEventListener('click',()=>{ state.background=null; state.calibrationSaved=false; renderAll(); saveState(); setStatus('Background removed'); });
  $('toggle-calibration').addEventListener('click',()=>{ overlay.hidden=!overlay.hidden; renderCalibration(); setStatus(overlay.hidden?'Calibration grid hidden':'Calibration grid visible'); });
  $('save-calibration').addEventListener('click',()=>{ state.calibrationSaved=true; overlay.hidden=true; state.placementMode=false; renderAll(); saveState(); setStatus('Calibration saved'); });
  $('toggle-placement').addEventListener('click',()=>{ state.placementMode=!state.placementMode; overlay.hidden=!state.placementMode; renderAll(); saveState(); setStatus(state.placementMode?'Placement mode':'Placement finished'); });
  wirePicker('add-character','character-picker','character'); wirePicker('add-prop','prop-picker','prop');
  $('remove-selected').addEventListener('click',()=>{ if(!state.selectedAssetId)return; state.assets=state.assets.filter(a=>a.id!==state.selectedAssetId); state.selectedAssetId=null; renderAll(); saveState(); setStatus('Selected asset removed'); });
  stage.addEventListener('click',()=>{ state.selectedAssetId=null; renderAll(); saveState(); });

  for (const [id,key] of [['horizon-y','horizonY'],['ground-far-y','groundFarY'],['ground-near-y','groundNearY'],['near-scale','nearScale'],['far-scale','farScale']]) {
    $(id).addEventListener('input',(e)=>{ state.calibration[key]=Number(e.target.value); state.calibrationSaved=false; overlay.hidden=false; renderAll(); saveState(); });
  }
  for (const [id,key] of [['asset-x','x'],['asset-ground-y','groundY'],['asset-manual-scale','manualScale']]) {
    $(id).addEventListener('input',(e)=>{ const a=selectedAsset(); if(!a)return; a[key]=Number(e.target.value); renderAll(); saveState(); });
  }

  window.OneWaveAnimator = { state, saveState, renderAll, selectedAsset, depthScale, readFileAsDataURL, imageDimensions, addAssetFromFile, clone };
  renderAll();
})();
