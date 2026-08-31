(() => {
  const state={};
  const sleep=ms=>new Promise(r=>setTimeout(r,ms));

  function ensureStyle(){
    if(document.getElementById('pointerStickStyle')) return;
    const s=document.createElement('style');
    s.id='pointerStickStyle';
    s.textContent=`
      .pointer-stick{position:fixed;z-index:30;width:12px;height:170px;border-radius:8px;pointer-events:none;transform-origin:50% 100%;transition:left .16s linear,top .16s linear,transform .16s linear;box-shadow:0 8px 18px #0008}
      .pointer-stick::after{content:'';position:absolute;left:50%;top:-10px;transform:translateX(-50%);width:24px;height:24px;border-radius:50%;border:2px solid #111;box-shadow:0 3px 8px #0009}
      .pointer-stick.field{background:#e5e5e5;border:1px solid #777}.pointer-stick.field::after{background:#f2f2f2}
      .pointer-stick.void{background:#2d2d2d;border:1px solid #777}.pointer-stick.void::after{background:#191919}
      .pointer-stick.grab{filter:brightness(1.35)}
    `;
    document.head.appendChild(s);
  }

  function make(side){
    ensureStyle();
    const stick=document.createElement('div');
    stick.className='pointer-stick '+(side==='FIELD'?'field':'void');
    document.body.appendChild(stick);
    state[side]={stick};
    park(side);
  }

  function sq(r,c){return document.querySelector(`.sq[data-r="${r}"][data-c="${c}"]`)}
  function center(el){const b=el.getBoundingClientRect();return{x:b.left+b.width/2,y:b.top+b.height/2}}

  function moveTo(side,r,c,lean=0){
    const el=sq(r,c),st=state[side]; if(!el||!st)return;
    const p=center(el);
    st.stick.style.left=`${p.x-6}px`;
    st.stick.style.top=`${p.y-160}px`;
    st.stick.style.transform=`rotate(${lean}deg)`;
  }

  function park(side){
    const st=state[side]; if(!st)return;
    const board=document.getElementById('board');
    if(!board){st.stick.style.top='80px';st.stick.style.left=side==='FIELD'?'20px':'calc(100vw - 32px)';return;}
    const b=board.getBoundingClientRect();
    st.stick.style.top=`${b.top+b.height*.36}px`;
    st.stick.style.left=side==='FIELD'?`${Math.max(14,b.left-48)}px`:`${Math.min(innerWidth-28,b.right+36)}px`;
    st.stick.style.transform=side==='FIELD'?'rotate(24deg)':'rotate(-24deg)';
  }

  async function touch(side,m){
    const st=state[side]; if(!st)return;
    const lean=side==='FIELD'?10:-10;
    moveTo(side,m.from.r,m.from.c,lean); await sleep(220);
    st.stick.classList.add('grab'); await sleep(110);
    moveTo(side,m.to.r,m.to.c,lean); await sleep(320);
    st.stick.classList.remove('grab'); await sleep(100);
    park(side);
  }

  make('FIELD');make('VOID');
  addEventListener('resize',()=>{park('FIELD');park('VOID')});
  window.ONE_WAVE_POINTERS={state,touch,park,moveTo};
})();
