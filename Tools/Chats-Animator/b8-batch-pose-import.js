(() => {
  const A=window.OneWaveAnimator,reel=window.b4Reel,$=(id)=>document.getElementById(id); if(!A||!reel) throw new Error('B8 requires app.js + B4');
  function naturalSort(files){return [...files].sort((a,b)=>a.name.localeCompare(b.name,undefined,{numeric:true,sensitivity:'base'}));}
  async function importBatch(files){ const selected=A.selectedAsset(); if(!selected) return; const sorted=naturalSort(files); if(!sorted.length)return; window.b4SaveCurrentFrame(); let insertAt=reel.activeIndex+1; let first=-1; const hold=Number($('batch-hold').value)||2;
    for(const file of sorted){ const snap=window.b4Snapshot(); const target=snap.assets.find(a=>a.id===selected.id); if(!target)continue; target.dataUrl=await A.readFileAsDataURL(file); const d=await A.imageDimensions(target.dataUrl); target.width=d.width;target.height=d.height;target.name=file.name; const frame={id:crypto.randomUUID?.()||`frame-${Date.now()}-${Math.random()}`,hold,snapshot:snap}; reel.frames.splice(insertAt,0,frame); if(first<0)first=insertAt; insertAt++; }
    if(first>=0){reel.activeIndex=first;window.b4Restore(reel.frames[first].snapshot);} window.b4RenderFrames();window.b4SaveReel(); }
  $('batch-import-poses').addEventListener('click',()=>{if(!A.selectedAsset())return;$('batch-pose-picker').click();}); $('batch-pose-picker').addEventListener('change',async e=>{await importBatch(e.target.files||[]);e.target.value='';});
  window.b8ImportBatch=importBatch;

  function loadB10Smoke() {
    if (document.querySelector('script[data-onewave-b10]')) return;
    const smoke = document.createElement('script');
    smoke.src = './b10-browser-smoke-test.js';
    smoke.dataset.onewaveB10 = 'true';
    document.body.appendChild(smoke);
  }

  // B9 is isolated in its own feature file. B10 loads only after B9 is available
  // so the smoke test can verify the complete B1–B9 runtime chain.
  if (!document.querySelector('script[data-onewave-b9]')) {
    const script = document.createElement('script');
    script.src = './b9-sprite-sheet-slicer.js';
    script.dataset.onewaveB9 = 'true';
    script.onload = loadB10Smoke;
    document.body.appendChild(script);
  } else if (window.b9SpriteSheetSlicer) {
    loadB10Smoke();
  } else {
    const existing = document.querySelector('script[data-onewave-b9]');
    existing.addEventListener('load', loadB10Smoke, { once: true });
  }
})();
