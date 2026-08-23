(() => {
  const A=window.OneWaveAnimator, reel=window.b4Reel, $=(id)=>document.getElementById(id);
  if(!A||!reel) throw new Error('B5 requires app.js and b4-frame-reel.js');
  function save(){ window.b4SaveCurrentFrame(); window.b4RenderFrames(); }
  function insert(after){ window.b4AddFrame(after,true); }
  function move(delta){ const i=reel.activeIndex, j=i+delta; if(j<0||j>=reel.frames.length)return; window.b4SaveCurrentFrame(); [reel.frames[i],reel.frames[j]]=[reel.frames[j],reel.frames[i]]; reel.activeIndex=j; window.b4Restore(reel.frames[j].snapshot); window.b4RenderFrames(); window.b4SaveReel(); }
  async function replacePose(file){ const a=A.selectedAsset(); if(!a||!file)return; a.dataUrl=await A.readFileAsDataURL(file); const d=await A.imageDimensions(a.dataUrl); a.width=d.width;a.height=d.height;a.name=file.name; A.renderAll(); A.saveState(); save(); }
  function copyPose(delta){ const source=A.selectedAsset(); if(!source)return; const targetIndex=reel.activeIndex+delta; if(targetIndex<0||targetIndex>=reel.frames.length)return; window.b4SaveCurrentFrame(); const target=reel.frames[targetIndex]; const match=target.snapshot.assets?.find(x=>x.id===source.id); if(!match)return; match.dataUrl=source.dataUrl; match.name=source.name; match.width=source.width; match.height=source.height; window.b4SaveReel(); }
  $('insert-before').addEventListener('click',()=>insert(false)); $('insert-after').addEventListener('click',()=>insert(true)); $('move-frame-left').addEventListener('click',()=>move(-1)); $('move-frame-right').addEventListener('click',()=>move(1));
  $('replace-selected-pose').addEventListener('click',()=>$('replacement-picker').click()); $('replacement-picker').addEventListener('change',async(e)=>{const f=e.target.files?.[0];if(f)await replacePose(f);e.target.value='';});
  $('copy-pose-prev').addEventListener('click',()=>copyPose(-1)); $('copy-pose-next').addEventListener('click',()=>copyPose(1));
})();
