(()=>{
'use strict';
const FORMAT='one-wave-character-motion-library';
const VERSION=3;
const FRAMES_PER_SHEET=50;
const DEFAULT_COLUMNS=10;
const DEFAULT_ROWS=5;
const clone=v=>JSON.parse(JSON.stringify(v));
const assert=(c,m)=>{if(!c)throw new Error(m)};
const slug=s=>String(s||'motion').trim().replace(/[^a-z0-9_-]+/gi,'-').replace(/^-+|-+$/g,'').toLowerCase()||'motion';

function makeLibrary({character,bodyVariant='base'}={}){
  assert(character,'Character is required');
  return {
    format:FORMAT,
    version:VERSION,
    character:String(character),
    bodyVariant:String(bodyVariant),
    createdAt:new Date().toISOString(),
    updatedAt:new Date().toISOString(),
    motions:[]
  };
}

function makeMotionSheet(library,{motion,folder='general',columns=DEFAULT_COLUMNS,rows=DEFAULT_ROWS}={}){
  assert(library?.format===FORMAT,'Unsupported library');
  assert(motion,'Motion name is required');
  columns=Number(columns);rows=Number(rows);
  assert(columns>0&&rows>0&&columns*rows===FRAMES_PER_SHEET,`Motion sheet must contain exactly ${FRAMES_PER_SHEET} cells`);
  const index=library.motions.length;
  const id=`motion-${String(index+1).padStart(5,'0')}`;
  const filename=`${slug(folder)}/${String(index+1).padStart(5,'0')}_${slug(motion)}.png`;
  const entry={
    id,index,motion:String(motion),folder:String(folder),filename,
    frameCount:FRAMES_PER_SHEET,columns,rows,
    state:'pending',mimeType:'image/png',width:null,height:null,
    transparent:null,sheetRef:null,error:null,createdAt:new Date().toISOString()
  };
  library.motions.push(entry);
  library.updatedAt=new Date().toISOString();
  return entry;
}

function validateGeneratedSheet(result,entry){
  assert(result&&typeof result==='object','Generator returned no result');
  assert(result.mimeType==='image/png','Each motion must be stored as one PNG sheet');
  assert(result.transparent===true,'Motion sheet must have transparent background');
  assert(Number(result.width)>0&&Number(result.height)>0,'PNG dimensions missing');
  assert(result.assetRef||result.sheetRef,'Motion sheet PNG must be persisted before completion');
  if(result.frameCount!=null)assert(Number(result.frameCount)===FRAMES_PER_SHEET,`Motion sheet must contain exactly ${FRAMES_PER_SHEET} frames`);
  if(result.columns!=null&&result.rows!=null)assert(Number(result.columns)*Number(result.rows)===FRAMES_PER_SHEET,`Motion sheet grid must contain exactly ${FRAMES_PER_SHEET} cells`);
  assert(entry.columns*entry.rows===FRAMES_PER_SHEET,'Stored motion-sheet grid is invalid');
  return result;
}

function frameAddress(entry,frameIndex){
  assert(entry?.sheetRef,'Motion sheet is not saved');
  assert(Number.isInteger(frameIndex)&&frameIndex>=0&&frameIndex<FRAMES_PER_SHEET,'Frame index must be 0..49');
  const column=frameIndex%entry.columns;
  const row=Math.floor(frameIndex/entry.columns);
  return {
    sheetRef:entry.sheetRef,
    frameIndex,
    column,row,
    columns:entry.columns,rows:entry.rows,
    u0:column/entry.columns,v0:row/entry.rows,
    u1:(column+1)/entry.columns,v1:(row+1)/entry.rows
  };
}

class MotionLibraryCreator{
  constructor({generateSheet,persistLibrary,onProgress}={}){
    assert(typeof generateSheet==='function','generateSheet adapter required');
    assert(typeof persistLibrary==='function','persistLibrary adapter required');
    this.generateSheet=generateSheet;
    this.persistLibrary=persistLibrary;
    this.onProgress=typeof onProgress==='function'?onProgress:()=>{};
    this.running=false;this.stopRequested=false;
  }
  async checkpoint(library){library.updatedAt=new Date().toISOString();await this.persistLibrary(clone(library));this.onProgress(clone(library));}
  requestStop(){this.stopRequested=true;}
  async generateMotion(library,motionId,context={}){
    assert(!this.running,'Creator already running');
    const entry=library.motions.find(m=>m.id===motionId);assert(entry,'Motion not found');
    this.running=true;this.stopRequested=false;entry.state='generating';entry.error=null;await this.checkpoint(library);
    try{
      if(this.stopRequested){entry.state='paused';await this.checkpoint(library);return clone(entry);}
      const result=validateGeneratedSheet(await this.generateSheet({
        character:library.character,
        bodyVariant:library.bodyVariant,
        motion:entry.motion,
        folder:entry.folder,
        filename:entry.filename,
        frameCount:FRAMES_PER_SHEET,
        columns:entry.columns,
        rows:entry.rows,
        transparentBackground:true,
        singlePngSheet:true,
        context:clone(context)
      }),entry);
      Object.assign(entry,{
        state:'saved',mimeType:'image/png',width:Number(result.width),height:Number(result.height),
        transparent:true,sheetRef:String(result.sheetRef||result.assetRef),error:null
      });
      await this.checkpoint(library);
      return clone(entry);
    }catch(error){entry.state='failed';entry.error=String(error?.message||error);await this.checkpoint(library);throw error;}
    finally{this.running=false;}
  }
}

window.OneWaveMotionLibraryCreator={
  FORMAT,VERSION,FRAMES_PER_SHEET,DEFAULT_COLUMNS,DEFAULT_ROWS,
  makeLibrary,makeMotionSheet,validateGeneratedSheet,frameAddress,MotionLibraryCreator
};
})();
