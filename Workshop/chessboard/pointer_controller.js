(() => {
  const SIDES=['FIELD','VOID'];
  const state={FIELD:null,VOID:null};
  const sleep=ms=>new Promise(r=>setTimeout(r,ms));
  const FLIP_MS=95;
  const NERVE_PER_SUPERVISOR=3;
  const FULL_PIPELINE_FLIPS=6;

  function ensureStyle(){
    if(document.getElementById('pointerStickStyle'))return;
    const s=document.createElement('style');s.id='pointerStickStyle';s.textContent=`
      .pointer-stick{position:fixed;z-index:50;width:10px;height:145px;border-radius:999px;pointer-events:none;transform-origin:50% 100%;transition:left .12s linear,top .12s linear,transform .12s linear,opacity .2s;background:linear-gradient(#fff,#b9c5d0 72%,#65707b);box-shadow:0 0 0 2px #1118,0 8px 20px #0008;opacity:.92}
      .pointer-stick::after{content:'';position:absolute;left:50%;top:-10px;transform:translateX(-50%);width:20px;height:20px;border-radius:50%;background:currentColor;box-shadow:0 0 18px currentColor}
      .pointer-stick.field-stick{color:#dcae56}.pointer-stick.void-stick{color:#79a9df}
      .pointer-stick.touch{filter:brightness(1.65);transform:translateY(5px) rotate(var(--lean,0deg))}
      .pointer-panel{position:fixed;z-index:49;bottom:12px;width:260px;background:#0c1015ef;border:1px solid #39434e;border-radius:12px;padding:9px 10px;font:11px/1.35 ui-monospace,monospace;pointer-events:none}
      .pointer-panel strong{font-size:12px}.pointer-panel.field{left:12px;color:#dcae56}.pointer-panel.void{right:12px;color:#79a9df}.windrow{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-top:6px}.wind{border:1px solid #39434e;border-radius:6px;text-align:center;padding:3px;color:#7e8995}.wind.on{color:#fff;border-color:currentColor;box-shadow:inset 0 0 12px currentColor}.pipe{margin-top:5px;color:#aab5c0}.flip{color:#fff}.up{color:#8ef0c8}.down{color:#f3b37b}
    `;document.head.appendChild(s);
  }

  function makeSide(side){
    ensureStyle();
    const stick=document.createElement('div');stick.className=`pointer-stick ${side==='FIELD'?'field-stick':'void-stick'}`;document.body.appendChild(stick);
    const panel=document.createElement('div');panel.className=`pointer-panel ${side.toLowerCase()}`;
    panel.innerHTML=`<strong>${side} POINTER</strong>
      <div class="mode">ternary HOLD</div>
      <div class="quad">oversight ↑ : waiting</div>
      <div class="act">override ↓ : waiting</div>
      <div class="pipe">nerve flip <span class="flip">0/6</span> · 3:1 fast layer · 6:1 full pipeline</div>
      <div class="windrow"><div class="wind" data-w="-1">W−</div><div class="wind on" data-w="0">W0</div><div class="wind" data-w="1">W+</div></div>`;
    document.body.appendChild(panel);
    state[side]={stick,panel,ternary:0,oversight:null,override:null,nerveFlip:0,pendingDown:null,lastOversight:null};
    park(side);
  }

  function squareEl(r,c){return document.querySelectorAll('.sq')[r*8+c]||null;}
  function center(el){const b=el.getBoundingClientRect();return {x:b.left+b.width/2,y:b.top+b.height/2};}
  function setPos(side,r,c,lean=0){const st=state[side],sq=squareEl(r,c);if(!st||!sq)return;const p=center(sq);st.stick.style.left=`${p.x-5}px`;st.stick.style.top=`${Math.max(8,p.y-138)}px`;st.stick.style.setProperty('--lean',`${lean}deg`);st.stick.style.transform=`rotate(${lean}deg)`;}
  function park(side){const st=state[side];if(!st)return;st.stick.style.left=side==='FIELD'?'32%':'68%';st.stick.style.top='18px';st.stick.style.transform='rotate(0deg)';}

  function ternary(side,v){
    const st=state[side];st.ternary=v;
    st.panel.querySelector('.mode').textContent=`ternary ${v<0?'−1 REVERSE':v>0?'+1 FORWARD':'0 HOLD'}`;
    st.panel.querySelectorAll('.wind').forEach(x=>x.classList.toggle('on',Number(x.dataset.w)===v));
  }

  function makeOversight(m){
    return {vertical:Math.sign(m.to.r-m.from.r),horizontal:Math.sign(m.to.c-m.from.c),from:{...m.from},to:{...m.to}};
  }

  function supervisoryExchange(side,m,label){
    const st=state[side];
    const newUp=makeOversight(m);
    const oldDown=st.pendingDown;
    st.lastOversight=newUp;
    st.oversight=newUp;
    st.panel.querySelector('.quad').innerHTML=`<span class="up">oversight ↑</span> NEW ${label} : V ${newUp.vertical>=0?'+':''}${newUp.vertical} / H ${newUp.horizontal>=0?'+':''}${newUp.horizontal}`;
    if(oldDown){
      st.override=oldDown;
      st.panel.querySelector('.act').innerHTML=`<span class="down">override ↓</span> LAST : ${oldDown.label}`;
    }else{
      st.panel.querySelector('.act').innerHTML=`<span class="down">override ↓</span> LAST : none yet`;
    }
    st.pendingDown={label,move:m,oversight:newUp};
    window.dispatchEvent(new CustomEvent('onewave:supervisor-exchange',{detail:{side,newUp,oldDown,flip:st.nerveFlip}}));
    return oldDown;
  }

  async function nerveFlip(side,m,i){
    const st=state[side];
    st.nerveFlip=i;
    st.panel.querySelector('.flip').textContent=`${i}/${FULL_PIPELINE_FLIPS}`;
    const dr=m.to.r-m.from.r, dc=m.to.c-m.from.c;
    const signed=Math.sign((Math.abs(dc)>=Math.abs(dr)?dc:dr));
    const phase=((i-1)%3);
    ternary(side,phase===0?signed:phase===1?0:-signed);
    const u=i/FULL_PIPELINE_FLIPS;
    const rr=Math.round(m.from.r+(m.to.r-m.from.r)*u);
    const cc=Math.round(m.from.c+(m.to.c-m.from.c)*u);
    setPos(side,rr,cc,signed*5);
    if(i%NERVE_PER_SUPERVISOR===0){
      const label=i===3?'MID / CURRENT VIEW':'ARRIVAL / NEW VIEW';
      supervisoryExchange(side,m,label);
    }
    await sleep(FLIP_MS);
  }

  async function touch(side,m){
    const st=state[side];if(!st)return;
    st.nerveFlip=0;st.panel.querySelector('.flip').textContent=`0/${FULL_PIPELINE_FLIPS}`;
    ternary(side,0);setPos(side,m.from.r,m.from.c,0);
    st.stick.classList.add('touch');await sleep(FLIP_MS);st.stick.classList.remove('touch');
    for(let i=1;i<=FULL_PIPELINE_FLIPS;i++) await nerveFlip(side,m,i);
    setPos(side,m.to.r,m.to.c,0);ternary(side,0);st.stick.classList.add('touch');await sleep(FLIP_MS);st.stick.classList.remove('touch');
    st.panel.querySelector('.mode').textContent='ternary 0 HOLD · cycle complete';
  }

  SIDES.forEach(makeSide);
  window.ONE_WAVE_POINTERS={state,touch,ternary,park,supervisoryExchange,
    ratios:{nerveToSupervisor:NERVE_PER_SUPERVISOR,fullPipeline:FULL_PIPELINE_FLIPS}};
})();
