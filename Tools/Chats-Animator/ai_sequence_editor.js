/*
PAGE REFERENCE — THIS NOTE PERTAINS TO THIS FILE ONLY. IT HAS NOTHING TO DO WITH RULES OR UPDATES FOR ANY OTHER FILE OR PAGE. DO NOT SUMMARIZE ANOTHER PAGE INTO THIS ONE OR APPLY THIS NOTE OUTSIDE ai_sequence_editor.js.

WHO YOU ARE HERE: You are working on the One-Wave Animator AI reel-sequence editor.
WHAT THIS FILE DOES: Opens a saved sequence, edits frame order/holds/motion labels, saves revisions, and presents completed still frames at project FPS.
ANIMATION MODEL HERE: Every sequence item references one saved PNG frame file. Playback advances completed still-frame states. This file must not convert the reel into tweening, moving placeholders, or sprite-sheet-as-frame storage.
PLAN HERE: Keep AI edits compatible with the same manually editable animator project. AI changes frame references/order/holds; the real animator presents those frames.
TEST HERE: Sequence behavior must ultimately be verified by the actual animator presenting real frame PNGs at FPS, not by a detached mock player.
*/
(()=>{
'use strict';
const FPS=24;
const BATCH_SIZE=50;
const clone=v=>JSON.parse(JSON.stringify(v));
const assert=(c,m)=>{if(!c)throw new Error(m)};
const wait=ms=>new Promise(r=>setTimeout(r,ms));

function normalizeFrame(frame,index){
  assert(frame,'Missing frame');
  assert(frame.assetRef,'Frame must reference a saved PNG');
  return {
    ...clone(frame),
    batchIndex:index,
    holdTicks:Math.max(1,Math.min(240,Number(frame.holdTicks)||2)),
    state:'saved',
    mimeType:'image/png'
  };
}

function loadBatch(library,batchId){
  assert(library&&Array.isArray(library.batches),'Motion library required');
  const batch=library.batches.find(b=>b.id===batchId);
  assert(batch,'Batch not found');
  assert(Array.isArray(batch.jobs)&&batch.jobs.length===BATCH_SIZE,`A4 requires a ${BATCH_SIZE}-frame batch`);
  assert(batch.jobs.every(j=>j.state==='saved'&&j.assetRef),'All 50 PNG frames must be saved before editing');
  return {
    format:'one-wave-ai-sequence-edit',
    version:1,
    character:library.character,
    bodyVariant:library.bodyVariant,
    batchId:batch.id,
    fps:FPS,
    frames:batch.jobs.map((j,i)=>normalizeFrame(j,i)),
    revision:0
  };
}

class AISequenceEditor{
  constructor({presentFrame,saveRevision,onChange}={}){
    assert(typeof presentFrame==='function','presentFrame adapter required');
    assert(typeof saveRevision==='function','saveRevision adapter required');
    this.presentFrame=presentFrame;
    this.saveRevision=saveRevision;
    this.onChange=typeof onChange==='function'?onChange:()=>{};
    this.sequence=null;
    this.playing=false;
    this.stopRequested=false;
    this.paused=false;
  }

  open(library,batchId){
    this.sequence=loadBatch(library,batchId);
    this.onChange(clone(this.sequence));
    return clone(this.sequence);
  }

  requireOpen(){assert(this.sequence,'No 50-frame sequence is open');}
  touch(){this.sequence.revision+=1;this.onChange(clone(this.sequence));}
  frame(i){this.requireOpen();assert(Number.isInteger(i)&&i>=0&&i<BATCH_SIZE,'Frame index must be 0..49');return this.sequence.frames[i];}

  replaceFrame(index,{assetRef,width,height,motion,filename}={}){
    const f=this.frame(index);
    assert(assetRef,'Replacement PNG assetRef required');
    f.assetRef=String(assetRef);
    if(width!=null)f.width=Number(width);
    if(height!=null)f.height=Number(height);
    if(motion!=null)f.motion=String(motion);
    if(filename!=null)f.filename=String(filename);
    f.mimeType='image/png';f.state='saved';
    this.touch();
  }

  setHold(index,ticks){
    this.frame(index).holdTicks=Math.max(1,Math.min(240,Number(ticks)||1));
    this.touch();
  }

  setMotion(index,motion){this.frame(index).motion=String(motion||'pose');this.touch();}

  swap(a,b){
    this.frame(a);this.frame(b);
    const frames=this.sequence.frames;
    [frames[a],frames[b]]=[frames[b],frames[a]];
    frames.forEach((f,i)=>f.batchIndex=i);
    this.touch();
  }

  reorder(order){
    this.requireOpen();
    assert(Array.isArray(order)&&order.length===BATCH_SIZE,'Reorder must contain exactly 50 indices');
    const sorted=[...order].sort((a,b)=>a-b);
    assert(sorted.every((v,i)=>v===i),'Reorder must use each frame index exactly once');
    this.sequence.frames=order.map(i=>clone(this.sequence.frames[i]));
    this.sequence.frames.forEach((f,i)=>f.batchIndex=i);
    this.touch();
  }

  applyCommands(commands=[]){
    assert(Array.isArray(commands),'AI commands must be an array');
    for(const cmd of commands){
      assert(cmd&&cmd.type,'Command type required');
      if(cmd.type==='replace-frame')this.replaceFrame(cmd.index,cmd);
      else if(cmd.type==='set-hold')this.setHold(cmd.index,cmd.ticks);
      else if(cmd.type==='set-motion')this.setMotion(cmd.index,cmd.motion);
      else if(cmd.type==='swap')this.swap(cmd.a,cmd.b);
      else if(cmd.type==='reorder')this.reorder(cmd.order);
      else throw new Error(`Unsupported AI edit command: ${cmd.type}`);
    }
    return clone(this.sequence);
  }

  async save(){
    this.requireOpen();
    const saved=await this.saveRevision(clone(this.sequence));
    assert(saved!==false,'Sequence revision was not saved');
    return clone(this.sequence);
  }

  pause(){if(this.playing)this.paused=true;}
  resume(){if(this.playing)this.paused=false;}
  stop(){this.stopRequested=true;this.paused=false;}

  async run({loop=false}={}){
    this.requireOpen();
    assert(!this.playing,'Sequence already running');
    this.playing=true;this.stopRequested=false;this.paused=false;
    try{
      do{
        for(let i=0;i<BATCH_SIZE;i+=1){
          if(this.stopRequested)return;
          while(this.paused&&!this.stopRequested)await wait(20);
          if(this.stopRequested)return;
          const frame=this.sequence.frames[i];
          await this.presentFrame(clone(frame),i,clone(this.sequence));
          const ticks=Math.max(1,Number(frame.holdTicks)||1);
          await wait((ticks/FPS)*1000);
        }
      }while(loop&&!this.stopRequested);
    }finally{this.playing=false;this.paused=false;this.stopRequested=false;}
  }
}

window.OneWaveAISequenceEditor={FPS,BATCH_SIZE,loadBatch,AISequenceEditor};
})();