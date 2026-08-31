(() => {
  const PIECES = {
    '♙':'P','♖':'R','♘':'N','♗':'B','♕':'Q','♔':'K',
    '♟':'P','♜':'R','♞':'N','♝':'B','♛':'Q','♚':'K'
  };
  const white=new Set(['♙','♖','♘','♗','♕','♔']);
  const black=new Set(['♟','♜','♞','♝','♛','♚']);
  const value={P:1,N:3,B:3,R:5,Q:9,K:100};
  const sideOf=p=>white.has(p)?'FIELD':black.has(p)?'VOID':null;
  const inside=(r,c)=>r>=0&&r<8&&c>=0&&c<8;
  const enemy=(a,b)=>b&&sideOf(a)!==sideOf(b);

  function rayMoves(b,r,c,dirs){
    const out=[],p=b[r][c];
    for(const [dr,dc] of dirs){
      let rr=r+dr,cc=c+dc;
      while(inside(rr,cc)){
        if(!b[rr][cc]) out.push([rr,cc]);
        else { if(enemy(p,b[rr][cc])) out.push([rr,cc]); break; }
        rr+=dr;cc+=dc;
      }
    }
    return out;
  }

  function movesFor(b,r,c){
    const p=b[r][c]; if(!p)return [];
    const t=PIECES[p], s=sideOf(p), out=[];
    if(t==='P'){
      const d=s==='FIELD'?-1:1, start=s==='FIELD'?6:1;
      if(inside(r+d,c)&&!b[r+d][c]){
        out.push([r+d,c]);
        if(r===start && !b[r+2*d][c]) out.push([r+2*d,c]);
      }
      for(const dc of [-1,1]) if(inside(r+d,c+dc)&&enemy(p,b[r+d][c+dc])) out.push([r+d,c+dc]);
    } else if(t==='N'){
      for(const [dr,dc] of [[-2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]]){
        const rr=r+dr,cc=c+dc;if(inside(rr,cc)&&(!b[rr][cc]||enemy(p,b[rr][cc])))out.push([rr,cc]);
      }
    } else if(t==='B') return rayMoves(b,r,c,[[-1,-1],[-1,1],[1,-1],[1,1]]);
    else if(t==='R') return rayMoves(b,r,c,[[-1,0],[1,0],[0,-1],[0,1]]);
    else if(t==='Q') return rayMoves(b,r,c,[[-1,-1],[-1,1],[1,-1],[1,1],[-1,0],[1,0],[0,-1],[0,1]]);
    else if(t==='K'){
      for(let dr=-1;dr<=1;dr++)for(let dc=-1;dc<=1;dc++)if(dr||dc){const rr=r+dr,cc=c+dc;if(inside(rr,cc)&&(!b[rr][cc]||enemy(p,b[rr][cc])))out.push([rr,cc]);}
    }
    return out;
  }

  function allMoves(side){
    const out=[];
    for(let r=0;r<8;r++)for(let c=0;c<8;c++){
      const p=window.board?.[r]?.[c];
      if(p&&sideOf(p)===side){
        for(const [rr,cc] of movesFor(window.board,r,c)) out.push({from:{r,c},to:{r:rr,c:cc},piece:p,pieceType:PIECES[p],capture:window.board[rr][cc]||'',captureType:PIECES[window.board[rr][cc]]||''});
      }
    }
    return out;
  }

  function localFallback(side,ms){
    const gate=side==='FIELD'?(window.fieldStep||0):(window.voidStep||0);
    const sound=side==='FIELD'?window.FIELD_SOUND_TOKEN:window.VOID_SOUND_TOKEN;
    const pitch=sound?.diff?.pitch||0;
    ms.sort((a,b)=>score(b)-score(a));return ms[0];
    function score(m){
      const capture=(value[m.captureType]||0)*12;
      const advance=side==='FIELD'?(m.from.r-m.to.r):(m.to.r-m.from.r);
      const center=3.5-(Math.abs(3.5-m.to.r)+Math.abs(3.5-m.to.c))/2;
      return side==='FIELD'?capture+advance*(2+gate*.25)+center*1.3+pitch*.4+Math.random()*2:capture+center*(2+gate*.2)-advance*.4-pitch*.4+Math.random()*2.5;
    }
  }

  async function choose(side){
    const ms=allMoves(side); if(!ms.length)return null;
    const gate=side==='FIELD'?(window.fieldStep||0):(window.voidStep||0);
    const sound=side==='FIELD'?window.FIELD_SOUND_TOKEN:window.VOID_SOUND_TOKEN;
    if(window.ONE_WAVE_LOCAL_BRAINS){
      try{
        const res=await window.ONE_WAVE_LOCAL_BRAINS.choose(side,ms,gate,sound);
        if(res?.move){
          window.ONE_WAVE_LAST_BRAIN_REPLY=res;
          return res.move;
        }
      }catch(e){ console.warn('Local brain unavailable; using browser fallback.',e); }
    }
    return localFallback(side,ms);
  }

  function kingAlive(side){
    const k=side==='FIELD'?'♔':'♚';
    return window.board?.some(row=>row.includes(k));
  }

  let timer=null, running=false, delay=900, busy=false;
  async function step(){
    if(!running||busy)return;
    if(!kingAlive('FIELD')||!kingAlive('VOID')){ stop(); return; }
    const side=window.turn;
    busy=true;
    try{
      const m=await choose(side);
      if(!m){stop();return;}
      if(window.ONE_WAVE_POINTERS) await window.ONE_WAVE_POINTERS.touch(side,m);
      window.selected={...m.from};
      window.clickSquare(m.to.r,m.to.c);
    } finally { busy=false; }
  }
  function start(){
    if(running)return;
    running=true;
    timer=setInterval(step,delay);
    const b=document.getElementById('autoMatchBtn');if(b)b.textContent='■ STOP MATCH';
  }
  function stop(){
    running=false;if(timer){clearInterval(timer);timer=null;}
    const b=document.getElementById('autoMatchBtn');if(b)b.textContent='▶ START MATCH';
  }
  function setSpeed(ms){delay=Math.max(700,Number(ms)||900);if(running){stop();start();}}

  function addControls(){
    const controls=document.querySelector('.controls');if(!controls)return;
    if(document.getElementById('autoMatchBtn'))return;
    const btn=document.createElement('button');btn.id='autoMatchBtn';btn.textContent='▶ START MATCH';btn.onclick=()=>running?stop():start();
    const speed=document.createElement('select');speed.id='matchSpeed';speed.innerHTML='<option value="1500">Slow</option><option value="900" selected>Match</option><option value="700">Fast</option>';
    speed.onchange=()=>setSpeed(speed.value);
    controls.prepend(speed);controls.prepend(btn);
  }

  window.ONE_WAVE_MATCH={start,stop,step,setSpeed,get running(){return running;}};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',addControls);else addControls();
})();
