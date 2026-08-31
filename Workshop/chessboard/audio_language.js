(() => {
  const S = { last:null, history:[], max:1024, analyser:null, timer:null };
  const s3=(x,e=0.02)=>x>e?1:x<-e?-1:0;
  const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
  const parity=n=>Math.abs(Math.trunc(n))%2===0?'E':'O';

  function spectralFeatures(analyser, ac){
    const bins=new Float32Array(analyser.frequencyBinCount);
    const wave=new Float32Array(analyser.fftSize);
    analyser.getFloatFrequencyData(bins);
    analyser.getFloatTimeDomainData(wave);

    let rms=0; for(const v of wave) rms+=v*v; rms=Math.sqrt(rms/wave.length);
    let sum=0, weighted=0, peak=-Infinity, peakI=0;
    const nyq=ac.sampleRate/2;
    for(let i=0;i<bins.length;i++){
      const p=Math.pow(10,bins[i]/20);
      sum+=p; weighted+=p*(i/bins.length)*nyq;
      if(bins[i]>peak){peak=bins[i];peakI=i}
    }
    const centroid=sum?weighted/sum:0;
    const peakHz=(peakI/bins.length)*nyq;

    let zc=0; for(let i=1;i<wave.length;i++) if((wave[i-1]<0)!=(wave[i]<0)) zc++;
    const zcr=zc/wave.length;
    return {rms,centroid,peakHz,zcr};
  }

  function toMachineToken(f){
    const prev=S.last||f;
    const dRms=f.rms-prev.rms, dCent=f.centroid-prev.centroid, dPeak=f.peakHz-prev.peakHz, dZ=f.zcr-prev.zcr;

    // Root from dominant frequency in MIDI-like semitone space; no English label needed.
    const root=f.peakHz>0 ? Math.round(69+12*Math.log2(f.peakHz/440)) : 0;
    const x2=root*2;
    const token={
      root,
      local:[x2-1,x2,x2+1],
      parent:Math.trunc(x2/2),
      parity:parity(x2),
      diff:{
        pressure:s3(dRms,0.003),
        pitch:s3(dPeak,8),
        brightness:s3(dCent,25),
        texture:s3(dZ,0.01)
      },
      level:{
        pressure:clamp(f.rms*8,0,1),
        brightness:clamp(f.centroid/5000,0,1),
        texture:clamp(f.zcr*5,0,1)
      },
      raw:f,
      t:performance.now()
    };
    S.last=f; S.history.push(token); if(S.history.length>S.max)S.history.shift();
    return token;
  }

  function compact(t){
    const sg=x=>x>0?'+1':x<0?'-1':'0';
    return `R${t.root} X${t.root*2} W[${t.local.join('|')}] P${sg(t.diff.pitch)} Q${sg(t.diff.pressure)} B${sg(t.diff.brightness)} T${sg(t.diff.texture)}`;
  }

  function install(){
    const doc=document;
    const w=window;
    const wait=setInterval(()=>{
      if(!w.ac || !w.master) return;
      clearInterval(wait);
      const analyser=w.ac.createAnalyser();
      analyser.fftSize=2048;
      analyser.smoothingTimeConstant=0.55;
      // Tap the existing game audio without changing what reaches the speakers.
      try{ w.master.connect(analyser); }catch(e){}
      S.analyser=analyser;
      w.ONE_WAVE_SOUND_LANGUAGE={latest:null,history:S.history};

      S.timer=setInterval(()=>{
        const f=spectralFeatures(analyser,w.ac);
        const tok=toMachineToken(f);
        w.ONE_WAVE_SOUND_LANGUAGE.latest=tok;
        w.FIELD_SOUND_TOKEN=tok;
        w.VOID_SOUND_TOKEN=tok;
        const code=compact(tok);
        const ear=doc.getElementById('earReadout');
        if(ear){
          const base=(ear.textContent||'').replace(/ · LANG .*/, '');
          ear.textContent=`${base} · LANG ${code}`;
        }
        const fs=doc.getElementById('fieldStatus'),vs=doc.getElementById('voidStatus');
        if(fs)fs.dataset.soundLanguage=code;
        if(vs)vs.dataset.soundLanguage=code;
      },30);
    },100);
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',install); else install();
})();
