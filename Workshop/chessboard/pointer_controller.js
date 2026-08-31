(() => {
  const SIDES=['FIELD','VOID'];
  const state={FIELD:null,VOID:null};
  const sleep=ms=>new Promise(r=>setTimeout(r,ms));

  function ensureStyle(){
    if(document.getElementById('pointerStickStyle'))return;
    const s=document.createElement('style');s.id='pointerStickStyle';s.textContent=`
      .pointer-stick{position:fixed;z-index:50;width:10px;height:145px;border-radius:999px;pointer-events:none;transform-origin:50% 100%;transition:left .22s ease,top .22s ease,transform .22s ease,opacity .2s;background:linear-gradient(#fff,#b9c5d0 72%,#65707b);box-shadow:0 0 0 2px #1118,0 8px 20px #0008;opacity:.92}
      .pointer-stick::after{content:'';position:absolute;left:50%;top:-10px;transform:translateX(-50%);width:20px;height:20px;border-radius:50%;background:currentColor;box-shadow:0 0 18px currentColor}
      .pointer-stick.field-stick{color:#dcae56}.pointer-stick.void-stick{color:#79a9df}
      .pointer-stick.touch{filter:brightness(1.6);transform:translateY(5px) rotate(var(--lean,0deg))}
      .pointer-panel{position:fixed;z-index:49;bottom:12px;width:230px;background:#0c1015eF;border:1px solid #39434e;border-radius:12px;padding:9px 10px;font:11px/1.35 ui-monospace,monospace;pointer-events:none}
      .pointer-panel strong{font-size:12px}.pointer-panel.field{left:12px;color:#dcae56}.pointer-panel.void{right:12px;color:#79a9df}.windrow{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-top:6px}.wind{border:1px solid #39434e;border-radius:6px;text-align:center;padding:3px;color:#7e8995}.wind.on{color:#fff;border-color:currentColor;box-shadow:inset 0 0 12px currentColor}
    `;document.head.appendChild(s);
  }

  function makeSide(side){
    ensureStyle();
    const stick=document.createElement('div');stick.className=`pointer-stick ${side==='FIELD'?'field-stick':'void-stick'}`;document.body.appendChild(stick);
    const panel=document.createElement('div');panel.className=`pointer-panel ${side.toLowerCase()}`;panel.innerHTML=`<strong>${side} POINTER</strong><div class="mode">ternary HOLD</div><div class="quad">quadratic oversight: waiting</div><div class="act">override: waiting</div><div class="windrow"><div class="wind" data-w="-1">W−</div><div class="wind on" data-w="0">W0</div><div class="wind" data-w="1">W+</div></div>`;document.body.appendChild(panel);
    state[side]={stick,panel,ternary:0,oversight:null,override:null};
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
  function oversight(side,m){
    const st=state[side];
    const dr=Math.sign(m.to.r-m.from.r),dc=Math.sign(m.to.c-m.from.c);
    // Quadratic view: two signed axes observe the candidate before action.
    st.oversight={vertical:dr,horizontal:dc,from:m.from,to:m.to};
    st.panel.querySelector('.quad').textContent=`quadratic oversight ↑ : V ${dr>=0?'+':''}${dr} / H ${dc>=0?'+':''}${dc}`;
    return st.oversight;
  }
  function override(side,phase,m){
    const st=state[side];st.override=phase;
    st.panel.querySelector('.act').textContent=`override ↓ : ${phase}${m?` ${String.fromCharCode(97+m.to.c)}${8-m.to.r}`:''}`;
  }

  async function touch(side,m){
    const st=state[side];if(!st)return;
    // Three virtual windings: -1, 0, +1.  They select movement phase,
    // while quadratic oversight observes the two board axes before commit.
    ternary(side,0);oversight(side,m);override(side,'VIEW',m);setPos(side,m.from.r,m.from.c,0);await sleep(180);
    st.stick.classList.add('touch');override(side,'SELECT',m);await sleep(120);st.stick.classList.remove('touch');
    const axis=(m.to.c-m.from.c)+(m.to.r-m.from.r);ternary(side,axis<0?-1:axis>0?1:0);override(side,'ACTION',m);setPos(side,m.to.r,m.to.c,axis<0?-7:axis>0?7:0);await sleep(220);
    st.stick.classList.add('touch');override(side,'COMMIT',m);await sleep(120);st.stick.classList.remove('touch');ternary(side,0);override(side,'HOLD',m);
  }

  SIDES.forEach(makeSide);
  window.ONE_WAVE_POINTERS={state,touch,oversight,override,ternary,park};
})();
