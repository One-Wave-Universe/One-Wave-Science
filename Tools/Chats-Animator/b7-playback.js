(() => {
  const reel=window.b4Reel, $=(id)=>document.getElementById(id); if(!reel) throw new Error('B7 requires B4');
  let playing=false,timer=null,cursor=0,sequence=[];
  function fps(){return Number($('fps-control').value)||24;}
  function buildSequence(){ window.b4SaveCurrentFrame(); const out=[]; reel.frames.forEach((f,i)=>{for(let n=0;n<Math.max(1,f.hold||1);n++)out.push(i);}); return out; }
  function stop(){playing=false;if(timer)clearTimeout(timer);timer=null;$('play-button').textContent='Play'; document.getElementById('calibration-overlay').hidden=true;}
  function tick(){ if(!playing)return; if(cursor>=sequence.length)cursor=0; const idx=sequence[cursor++]; const original=reel.activeIndex; reel.activeIndex=idx; window.b4Restore(reel.frames[idx].snapshot); document.getElementById('calibration-overlay').hidden=true; if(window.b6RenderOnion)document.getElementById('onion-layer').innerHTML=''; reel.activeIndex=original; timer=setTimeout(tick,1000/fps()); }
  function play(){ if(playing){stop();return;} sequence=buildSequence(); if(!sequence.length)return; playing=true;cursor=0;$('play-button').textContent='Stop';tick(); }
  $('play-button').addEventListener('click',play); $('fps-control').addEventListener('input',e=>{$('fps-value').textContent=e.target.value;}); $('fps-value').textContent=$('fps-control').value; window.addEventListener('beforeunload',stop); window.b7StopPlayback=stop;
})();
