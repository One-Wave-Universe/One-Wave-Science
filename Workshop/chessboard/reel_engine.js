(() => {
  const FPS = 24;
  const FRAME_MS = 1000 / FPS;
  const MAX_FRAMES = FPS * 120;
  const reel = [];
  let seq = 0;
  let running = false;
  let startMs = 0;
  let nextFrameMs = 0;

  function stableId(n){ return `reel-${String(n).padStart(8,'0')}`; }
  function boardSnapshot(){
    const board=document.getElementById('board');
    return board ? [...board.querySelectorAll('.sq')].map(s=>s.childNodes[0]?.nodeValue||'').join('') : '';
  }
  function gate(panel){ return document.querySelector(`${panel} .gate.active`)?.textContent?.trim() || ''; }
  function latestSound(){ return window.ONE_WAVE_SOUND_LANGUAGE?.latest || null; }

  function makeFrame(masterMs){
    const sound = latestSound();
    const frame = Object.freeze({
      id: stableId(seq),
      number: seq,
      fps: FPS,
      hold: 1,
      masterMs,
      sound,
      vision: Object.freeze({
        board: boardSnapshot(),
        turn: document.getElementById('turnBadge')?.textContent?.trim() || ''
      }),
      field: Object.freeze({
        gate: gate('.fieldPanel'),
        sound
      }),
      void: Object.freeze({
        gate: gate('.voidPanel'),
        sound
      })
    });
    seq++;
    reel.push(frame);
    if(reel.length > MAX_FRAMES) reel.shift();

    window.ONE_WAVE_REEL.latest = frame;
    window.FIELD_LOOP_INPUT = frame;
    window.VOID_LOOP_INPUT = frame;
    window.dispatchEvent(new CustomEvent('onewave:reel-frame',{detail:frame}));
    return frame;
  }

  function tick(now){
    if(!running) return;
    if(!startMs){
      startMs = now;
      nextFrameMs = now;
    }
    while(now >= nextFrameMs){
      makeFrame(nextFrameMs - startMs);
      nextFrameMs += FRAME_MS;
    }
    requestAnimationFrame(tick);
  }

  window.ONE_WAVE_REEL = {
    fps: FPS,
    frames: reel,
    latest: null,
    start(){
      if(running) return;
      running = true;
      requestAnimationFrame(tick);
    },
    stop(){ running = false; },
    clear(){ reel.length=0; seq=0; startMs=0; nextFrameMs=0; this.latest=null; },
    setHold(id,hold){
      const f=reel.find(x=>x.id===id);
      if(!f) return false;
      return false; // reel frames are immutable in the live game; holds belong to replay/export copies.
    }
  };

  // Constant reel: it starts with the page and never waits for a move or audio event.
  window.ONE_WAVE_REEL.start();
})();
