(() => {
  const URL='http://127.0.0.1:8788';
  async function health(){
    try{const r=await fetch(URL+'/health');return r.ok?await r.json():null}catch(e){return null}
  }
  async function choose(side,moves,gate,sound){
    const payload={side,moves,gate,sound};
    const r=await fetch(URL+'/choose',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    if(!r.ok) throw new Error('local brain '+r.status);
    return r.json();
  }
  window.ONE_WAVE_LOCAL_BRAINS={URL,health,choose};
})();
