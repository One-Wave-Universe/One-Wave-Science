(() => {
  // Continuous sensory reel: audio is sampled fast, translated into the shared
  // signed relational language, then every display frame is committed as one
  // immutable sensory frame for both state-machine loops.
  const S = {
    last:null,
    audioHistory:[],
    reel:[],
    maxAudio:2048,
    maxReel:1800, // ~30 s at 60 fps
    analyser:null,
    audioTimer:null,
    raf:null,
    frameNo:0,
    latestToken:null
  };

  const s3=(x,e=0.02)=>x>e?1:x<-e?-1:0;
  const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
  const parity=n=>Math.abs(Math.trunc(n))%2===0?'E':'O';

  function spectralFeatures(analyser, ac){
    const bins=new Float32Array(analyser.frequencyBinCount);
    const wave=new Float32Array(analyser.fftSize);
    analyser.getFloatFrequencyData(bins);
    analyser.getFloatTimeDomainData(wave);

    let rms=0;
    for(const v of wave) rms+=v*v;
    rms=Math.sqrt(rms/wave.length);

    let sum=0, weighted=0, peak=-Infinity, peakI=0;
    const nyq=ac.sampleRate/2;
    for(let i=0;i<bins.length;i++){
      const p=Math.pow(10,bins[i]/20);
      sum+=p;
      weighted+=p*(i/bins.length)*nyq;
      if(bins[i]>peak){peak=bins[i];peakI=i;}
    }
    const centroid=sum?weighted/sum:0;
    const peakHz=(peakI/bins.length)*nyq;

    let zc=0;
    for(let i=1;i<wave.length;i++) if((wave[i-1]<0)!=(wave[i]<0)) zc++;
    const zcr=zc/wave.length;
    return {rms,centroid,peakHz,zcr};
  }

  function toMachineToken(f){
    const prev=S.last||f;
    const dRms=f.rms-prev.rms;
    const dCent=f.centroid-prev.centroid;
    const dPeak=f.peakHz-prev.peakHz;
    const dZ=f.zcr-prev.zcr;

    // Dominant frequency becomes a numeric root. The root is doubled into the
    // next nested cycle and receives its reversible -1 | root | +1 wrapper.
    const root=f.peakHz>0 ? Math.round(69+12*Math.log2(f.peakHz/440)) : 0;
    const x2=root*2;
    const token=Object.freeze({
      root,
      scaleRoot:x2,
      local:Object.freeze([x2-1,x2,x2+1]),
      parent:Math.trunc(x2/2),
      parity:parity(x2),
      diff:Object.freeze({
        pressure:s3(dRms,0.003),
        pitch:s3(dPeak,8),
        brightness:s3(dCent,25),
        texture:s3(dZ,0.01)
      }),
      level:Object.freeze({
        pressure:clamp(f.rms*8,0,1),
        brightness:clamp(f.centroid/5000,0,1),
        texture:clamp(f.zcr*5,0,1)
      }),
      raw:Object.freeze({...f}),
      t:performance.now()
    });

    S.last=f;
    S.latestToken=token;
    S.audioHistory.push(token);
    if(S.audioHistory.length>S.maxAudio) S.audioHistory.shift();
    return token;
  }

  function compact(t){
    if(!t) return 'SILENT';
    const sg=x=>x>0?'+1':x<0?'-1':'0';
    return `R${t.root} X${t.scaleRoot} W[${t.local.join('|')}] P${sg(t.diff.pitch)} Q${sg(t.diff.pressure)} B${sg(t.diff.brightness)} T${sg(t.diff.texture)}`;
  }

  function boardSignature(){
    const b=document.getElementById('board');
    if(!b) return '';
    return [...b.querySelectorAll('.sq')].map(s=>s.childNodes[0]?.nodeValue||'').join('');
  }

  function activeGate(panel){
    return document.querySelector(`${panel} .gate.active`)?.textContent?.trim()||'';
  }

  function commitReelFrame(now){
    const tok=S.latestToken;
    const frame=Object.freeze({
      frame:S.frameNo++,
      t:now,
      sound:tok,
      code:compact(tok),
      field:Object.freeze({
        gate:activeGate('.fieldPanel'),
        gateIndex:typeof window.fieldStep==='number'?window.fieldStep:null,
        turn:window.turn==='FIELD',
        input:tok
      }),
      void:Object.freeze({
        gate:activeGate('.voidPanel'),
        gateIndex:typeof window.voidStep==='number'?window.voidStep:null,
        turn:window.turn==='VOID',
        input:tok
      }),
      vision:Object.freeze({
        board:boardSignature(),
        turn:document.getElementById('turnBadge')?.textContent?.trim()||''
      })
    });

    S.reel.push(frame);
    if(S.reel.length>S.maxReel) S.reel.shift();

    // These are the live inputs consumed by the two loops. They are replaced
    // every frame, like individual pictures on a cartoon/film reel.
    window.FIELD_LOOP_INPUT=frame;
    window.VOID_LOOP_INPUT=frame;
    window.ONE_WAVE_REEL.latest=frame;

    // Let any present/future state-machine worker subscribe without coupling
    // the translator to a specific implementation.
    window.dispatchEvent(new CustomEvent('onewave:sensory-frame',{detail:frame}));

    const ear=document.getElementById('earReadout');
    if(ear && tok){
      const base=(ear.textContent||'').replace(/ · LANG .*/, '').replace(/ · REEL .*/, '');
      ear.textContent=`${base} · LANG ${frame.code} · REEL F${frame.frame}`;
    }

    S.raf=requestAnimationFrame(commitReelFrame);
  }

  function install(){
    const wait=setInterval(()=>{
      if(!window.ac || !window.master) return;
      clearInterval(wait);

      const analyser=window.ac.createAnalyser();
      analyser.fftSize=2048;
      analyser.smoothingTimeConstant=0.55;
      try{ window.master.connect(analyser); }catch(e){}
      S.analyser=analyser;

      window.ONE_WAVE_SOUND_LANGUAGE={latest:null,history:S.audioHistory};
      window.ONE_WAVE_REEL={latest:null,frames:S.reel};

      // Hearing stays faster than the visual reel. It continuously updates the
      // sound token underneath the ~60 fps sensory-frame loop.
      S.audioTimer=setInterval(()=>{
        const f=spectralFeatures(analyser,window.ac);
        const tok=toMachineToken(f);
        window.ONE_WAVE_SOUND_LANGUAGE.latest=tok;
        window.FIELD_SOUND_TOKEN=tok;
        window.VOID_SOUND_TOKEN=tok;

        const code=compact(tok);
        const fs=document.getElementById('fieldStatus');
        const vs=document.getElementById('voidStatus');
        if(fs) fs.dataset.soundLanguage=code;
        if(vs) vs.dataset.soundLanguage=code;
      },10);

      S.raf=requestAnimationFrame(commitReelFrame);
    },100);
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',install);
  else install();
})();
