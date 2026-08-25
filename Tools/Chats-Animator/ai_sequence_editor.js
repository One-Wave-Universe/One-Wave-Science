(()=>{
'use strict';
const FPS=24;
const FRAME_COUNT=50;
const clone=v=>JSON.parse(JSON.stringify(v));
const assert=(c,m)=>{if(!c)throw new Error(m)};
const wait=ms=>new Promise(r=>setTimeout(r,ms));

function buildFrames(motion){
  assert(motion?.sheetRef,'Saved motion-sheet PNG required');
  assert(Number(motion.frameCount)===FRAME_COUNT,'Motion sheet must contain exactly 50 frames');
  assert(Number(motion.columns)*Number(motion.rows)===FRAME_COUNT,'Motion-sheet grid must contain exactly 50 cells');
  return Array.from({length:FRAME_COUNT},(_,frameIndex)=>{
    const column=frameIndex%motion.columns;
    const row=Math.floor(frameIndex/motion.columns);
    return {
      frameIndex,
      sheetRef:motion.sheetRef,
      sourceMotionId:motion.id,
      motion:motion.motion,
      holdTicks:2,
      crop:{column,row,columns:motion.columns,rows:motion.rows}
    };
  });
}

function loadMotion(library,motionId){
  assert(library&&Array.isArray(library.motions),'Motion library required');
  const motion=library.motions.find(m=>m.id===motionId);
  assert(motion,'Motion not found');
  assert(motion.state==='saved'&&motion.sheetRef,'Motion sheet must be saved before editing');
  return {
    format:'one-wave-ai-sequence-edit',
    version:2,
    character:library.character,
    bodyVariant:library.bodyVariant,
    motionId:motion.id,
    motionName:motion.motion,
    sheetRef:motion.sheetRef,
    fps:FPS,
    frames:buildFrames(motion),
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
    this.sequence=null;this.playing=false;this.stopRequested=false;this.paused=false;
  }
  open(library,motionId){this.sequence=loadMotion(library,motionId);this.onChange(clone(this.sequence));return clone(this.sequence);}
  requireOpen(){assert(this.sequence,'No 50-frame motion is open');}
  touch(){this.sequence.revision+=1;this.onChange(clone(this.sequence));}
  frame(i){this.requireOpen();assert(Number.isInteger(i)&&i>=0&&i<FRAME_COUNT,'Frame index must be 0..49');return this.sequence.frames[i];}
  setHold(index,ticks){this.frame(index).holdTicks=Math.max(1,Math.min(240,Number(ticks)||1));this.touch();}
  setMotionLabel(index,motion){this.frame(index).motion=String(motion||this.sequence.motionName);this.touch();}
  swap(a,b){this.frame(a);this.frame(b);const f=this.sequence.frames;[f[a],f[b]]=[f[b],f[a]];this.touch();}
  reorder(order){
    this.requireOpen();
    assert(Array.isArray(order)&&order.length===FRAME_COUNT,'Reorder must contain exactly 50 indices');
    const sorted=[...order].sort((a,b)=>a-b);assert(sorted.every((v,i)=>v===i),'Reorder must use each frame index exactly once');
    this.sequence.frames=order.map(i=>clone(this.sequence.frames[i]));this.touch();
  }
  replaceFrame(index,{sheetRef,sourceFrameIndex,columns,rows,motion}={}){
    const f=this.frame(index);
    assert(sheetRef,'Replacement sheetRef required');
    assert(Number.isInteger(sourceFrameIndex)&&sourceFrameIndex>=0&&sourceFrameIndex<FRAME_COUNT,'sourceFrameIndex must be 0..49');
    columns=Number(columns);rows=Number(rows);assert(columns*rows===FRAME_COUNT,'Replacement sheet must contain 50 cells');
    f.sheetRef=String(sheetRef);f.frameIndex=sourceFrameIndex;f.crop={column:sourceFrameIndex%columns,row:Math.floor(sourceFrameIndex/columns),columns,rows};
    if(motion!=null)f.motion=String(motion);this.touch();
  }
  applyCommands(commands=[]){
    assert(Array.isArray(commands),'AI commands must be an array');
    for(const cmd of commands){
      assert(cmd&&cmd.type,'Command type required');
      if(cmd.type==='set-hold')this.setHold(cmd.index,cmd.ticks);
      else if(cmd.type==='set-motion')this.setMotionLabel(cmd.index,cmd.motion);
      else if(cmd.type==='swap')this.swap(cmd.a,cmd.b);
      else if(cmd.type==='reorder')this.reorder(cmd.order);
      else if(cmd.type==='replace-frame')this.replaceFrame(cmd.index,cmd);
      else throw new Error(`Unsupported AI edit command: ${cmd.type}`);
    }
    return clone(this.sequence);
  }
  async save(){this.requireOpen();const saved=await this.saveRevision(clone(this.sequence));assert(saved!==false,'Sequence revision was not saved');return clone(this.sequence);}
  pause(){if(this.playing)this.paused=true;}
  resume(){if(this.playing)this.paused=false;}
  stop(){this.stopRequested=true;this.paused=false;}
  async run({loop=false}={}){
    this.requireOpen();assert(!this.playing,'Sequence already running');this.playing=true;this.stopRequested=false;this.paused=false;
    try{
      do{
        for(let i=0;i<FRAME_COUNT;i+=1){
          if(this.stopRequested)return;while(this.paused&&!this.stopRequested)await wait(20);if(this.stopRequested)return;
          const frame=this.sequence.frames[i];await this.presentFrame(clone(frame),i,clone(this.sequence));
          await wait((Math.max(1,Number(frame.holdTicks)||1)/FPS)*1000);
        }
      }while(loop&&!this.stopRequested);
    }finally{this.playing=false;this.paused=false;this.stopRequested=false;}
  }
}

window.OneWaveAISequenceEditor={FPS,FRAME_COUNT,buildFrames,loadMotion,AISequenceEditor};
})();
