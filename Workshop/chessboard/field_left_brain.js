(() => {
  'use strict';

  // FIELD half only. It perceives and generates expressive possibilities.
  // It does not move a checker, validate a move, or drive the stick.
  const FPS = 24;
  const FRAME_MS = 1000 / FPS;
  const MAX_EPISODES = 96;
  const MAX_CONSTELLATION_EDGES = 384;
  const FIELD_WEIGHT = 0.68;
  const VOID_WEIGHT = 0.32;

  const state = {
    frame: 0,
    running: false,
    timer: null,
    lastVision: null,
    lastAudio: null,
    episodes: [],
    constellation: new Map(),
    hopCursor: null,
    latest: null,
    hopfield: { W: null, n: 64 }
  };

  const clamp = (x,a,b) => Math.max(a,Math.min(b,x));
  const sign3 = (x,e=1e-9) => x > e ? 1 : x < -e ? -1 : 0;

  function boardVector(){
    const board = window.ONE_WAVE_BOARD?.board;
    if(!board) return Array(64).fill(0);
    const out=[];
    for(let r=0;r<8;r++) for(let c=0;c<8;c++){
      const p=board[r][c];
      out.push(p==='f'||p==='F' ? 1 : p==='v'||p==='V' ? -1 : 0);
    }
    return out;
  }

  function audioVector(){
    const t = window.ONE_WAVE_SOUND_LANGUAGE?.latest || window.FIELD_SOUND_TOKEN || null;
    if(!t) return [0,0,0,0,0,0,0];
    return [
      t.diff?.pressure||0,
      t.diff?.pitch||0,
      t.diff?.brightness||0,
      t.diff?.texture||0,
      t.level?.pressure||0,
      t.level?.brightness||0,
      t.level?.texture||0
    ];
  }

  function delta(a,b){
    if(!a) return b.map(sign3);
    return b.map((v,i)=>sign3(v-(a[i]||0)));
  }

  function cosine(a,b){
    let d=0,aa=0,bb=0;
    for(let i=0;i<a.length;i++){
      const x=a[i]||0,y=b[i]||0;
      d+=x*y; aa+=x*x; bb+=y*y;
    }
    return aa&&bb ? d/Math.sqrt(aa*bb) : 0;
  }

  function rebuildHopfield(){
    const n=state.hopfield.n;
    const W=Array.from({length:n},()=>new Float32Array(n));
    if(!state.episodes.length){ state.hopfield.W=W; return; }
    for(const ep of state.episodes){
      const x=ep.vision;
      for(let i=0;i<n;i++){
        const xi=x[i]||0;
        if(!xi) continue;
        for(let j=0;j<n;j++) if(i!==j) W[i][j]+=xi*(x[j]||0);
      }
    }
    const scale=1/Math.max(1,state.episodes.length*n);
    for(let i=0;i<n;i++) for(let j=0;j<n;j++) W[i][j]*=scale;
    state.hopfield.W=W;
  }

  function hopfieldRecall(seed,steps=3){
    const W=state.hopfield.W;
    if(!W) return seed.slice();
    let x=seed.slice();
    for(let s=0;s<steps;s++){
      const next=x.slice();
      for(let i=0;i<x.length;i++){
        let h=0;
        for(let j=0;j<x.length;j++) h+=W[i][j]*(x[j]||0);
        next[i]=sign3(h,0.00001);
      }
      x=next;
    }
    return x;
  }

  function hopfieldEnergy(x){
    const W=state.hopfield.W;
    if(!W) return 0;
    let e=0;
    for(let i=0;i<x.length;i++) for(let j=0;j<x.length;j++) e += (x[i]||0)*W[i][j]*(x[j]||0);
    return -0.5*e;
  }

  function connectConstellation(a,b,weight){
    if(!a||!b||a===b) return;
    if(!state.constellation.has(a)) state.constellation.set(a,new Map());
    if(!state.constellation.has(b)) state.constellation.set(b,new Map());
    state.constellation.get(a).set(b,weight);
    state.constellation.get(b).set(a,weight);
    let count=0;
    for(const m of state.constellation.values()) count+=m.size;
    if(count>MAX_CONSTELLATION_EDGES*2){
      for(const [k,m] of state.constellation){
        const weakest=[...m.entries()].sort((x,y)=>x[1]-y[1])[0];
        if(weakest){m.delete(weakest[0]); state.constellation.get(weakest[0])?.delete(k); break;}
      }
    }
  }

  function rabbitHop(seedEpisode){
    if(!seedEpisode) return null;
    const neighbors=state.constellation.get(seedEpisode.id);
    if(!neighbors?.size) return seedEpisode;
    let best=null,bestScore=-Infinity;
    for(const [id,w] of neighbors){
      const ep=state.episodes.find(x=>x.id===id);
      if(!ep) continue;
      const novelty=1-Math.abs(cosine(seedEpisode.vision,ep.vision));
      const score=w*0.7 + novelty*0.3;
      if(score>bestScore){bestScore=score;best=ep;}
    }
    return best || seedEpisode;
  }

  function boltzmannSample(candidates,temperature=0.72){
    if(!candidates.length) return null;
    const t=Math.max(0.05,temperature);
    const mx=Math.max(...candidates.map(x=>x.score));
    const weights=candidates.map(x=>Math.exp((x.score-mx)/t));
    const total=weights.reduce((a,b)=>a+b,0);
    let r=Math.random()*total;
    for(let i=0;i<candidates.length;i++){
      r-=weights[i];
      if(r<=0) return candidates[i];
    }
    return candidates[candidates.length-1];
  }

  function expressiveCandidates(vision,audio,visionDelta,audioDelta){
    const recalled=hopfieldRecall(vision);
    const attractorSimilarity=cosine(vision,recalled);
    const candidates=[];
    for(const ep of state.episodes.slice(-24)){
      const association=cosine(vision,ep.vision);
      const soundAssociation=cosine(audio,ep.audio);
      const novelty=1-Math.abs(association);
      const fieldDrive=(novelty*0.52 + Math.max(0,association)*0.28 + Math.max(0,soundAssociation)*0.20);
      const voidCheck=(Math.abs(association)*0.55 + (1-Math.abs(soundAssociation))*0.45);
      candidates.push({
        episodeId:ep.id,
        score:FIELD_WEIGHT*fieldDrive + VOID_WEIGHT*voidCheck,
        association,
        soundAssociation,
        novelty
      });
    }
    if(!candidates.length){
      candidates.push({episodeId:null,score:0.5,association:0,soundAssociation:0,novelty:1});
    }
    const sampled=boltzmannSample(candidates,clamp(0.9-(audio[4]||0)*0.35,0.35,0.9));
    return {sampled,recalled,attractorSimilarity,energy:hopfieldEnergy(recalled),visionDelta,audioDelta};
  }

  function remember(vision,audio,expression){
    const id=`F-${String(state.frame).padStart(8,'0')}`;
    const ep=Object.freeze({id,frame:state.frame,vision:vision.slice(),audio:audio.slice(),expression,t:performance.now()});
    const prev=state.episodes[state.episodes.length-1];
    state.episodes.push(ep);
    if(state.episodes.length>MAX_EPISODES) state.episodes.shift();
    if(prev){
      const w=0.5+0.5*cosine(prev.vision,vision);
      connectConstellation(prev.id,id,w);
    }
    for(const older of state.episodes.slice(-8,-1)){
      const sim=cosine(older.vision,vision);
      if(sim>0.72) connectConstellation(older.id,id,sim);
    }
    rebuildHopfield();
    return ep;
  }

  function tick(){
    const vision=boardVector();
    const audio=audioVector();
    const vd=delta(state.lastVision,vision);
    const ad=delta(state.lastAudio,audio);
    const expression=expressiveCandidates(vision,audio,vd,ad);
    const ep=remember(vision,audio,expression);
    const hopped=rabbitHop(ep);
    state.hopCursor=hopped?.id||ep.id;
    state.latest=Object.freeze({
      frame:state.frame,
      fieldDominance:FIELD_WEIGHT,
      voidCounterweight:VOID_WEIGHT,
      vision,
      audio,
      expression,
      rabbitHop:state.hopCursor,
      memoryCount:state.episodes.length,
      constellationNodes:state.constellation.size,
      constantFrameMs:FRAME_MS
    });
    state.lastVision=vision;
    state.lastAudio=audio;
    state.frame++;
    window.FIELD_LEFT_BRAIN_OUTPUT=state.latest;
    window.dispatchEvent(new CustomEvent('onewave:field-left-brain',{detail:state.latest}));
  }

  function start(){
    if(state.running) return;
    state.running=true;
    tick();
    state.timer=setInterval(tick,FRAME_MS);
  }

  function stop(){
    state.running=false;
    if(state.timer){clearInterval(state.timer);state.timer=null;}
  }

  window.ONE_WAVE_FIELD_LEFT_BRAIN={
    state,start,stop,tick,hopfieldRecall,hopfieldEnergy,rabbitHop,boltzmannSample,
    weights:Object.freeze({field:FIELD_WEIGHT,void:VOID_WEIGHT}),
    timing:Object.freeze({fps:FPS,frameMs:FRAME_MS})
  };

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start,{once:true});
  else start();
})();
