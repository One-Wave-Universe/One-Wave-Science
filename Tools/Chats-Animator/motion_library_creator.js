/*
PAGE REFERENCE — THIS NOTE PERTAINS TO THIS FILE ONLY. IT HAS NOTHING TO DO WITH RULES OR UPDATES FOR ANY OTHER FILE OR PAGE. DO NOT SUMMARIZE ANOTHER PAGE INTO THIS ONE OR APPLY THIS NOTE OUTSIDE motion_library_creator.js.

WHO YOU ARE HERE: You are working on the One-Wave Animator motion-library creation logic.
WHAT THIS FILE DOES: Creates and persists reusable motion-frame PNG entries and batches for a character.
ANIMATION MODEL HERE: One PNG file equals one animation frame. A motion is a folder/sequence of individual PNG frame files. This file must reject sprite-sheet/composite storage as the canonical editable frame model.
PLAN HERE: Reuse existing motion frames first and create only the missing frame files needed by the current scene. The library grows as real scenes are produced, not by blindly generating a giant library in advance.
TEST HERE: Validate that each saved motion entry points to exactly one transparent PNG frame and can be consumed by the real animator sequence/reel workflow.
*/
(()=>{
'use strict';
const FORMAT='one-wave-character-motion-library';
const VERSION=2;
const BATCH_SIZE=50;
const clone=v=>JSON.parse(JSON.stringify(v));
const assert=(c,m)=>{if(!c)throw new Error(m)};
const slug=s=>String(s||'pose').trim().replace(/[^a-z0-9_-]+/gi,'-').replace(/^-+|-+$/g,'').toLowerCase()||'pose';

function makeLibrary({character,bodyVariant='base'}={}){
  assert(character,'Character is required');
  return {format:FORMAT,version:VERSION,character:String(character),bodyVariant:String(bodyVariant),createdAt:new Date().toISOString(),updatedAt:new Date().toISOString(),frames:[],batches:[]};
}

function makeBatch(library,motions=[]){
  assert(library?.format===FORMAT,'Unsupported library');
  assert(Array.isArray(motions)&&motions.length===BATCH_SIZE,`A generation batch must contain exactly ${BATCH_SIZE} motion jobs`);
  const batchIndex=library.batches.length;
  const startIndex=library.frames.length;
  const id=`batch-${String(batchIndex+1).padStart(4,'0')}`;
  const jobs=motions.map((motion,i)=>({
    libraryIndex:startIndex+i,
    batchIndex:i,
    motion:String(motion),
    state:'pending',
    filename:`${String(startIndex+i+1).padStart(6,'0')}_${slug(motion)}.png`,
    mimeType:null,width:null,height:null,transparent:null,assetRef:null,error:null
  }));
  const batch={id,index:batchIndex,size:BATCH_SIZE,startIndex,endIndex:startIndex+BATCH_SIZE-1,status:'pending',createdAt:new Date().toISOString(),completed:0,zipRef:null,manifestRef:null,jobs};
  library.batches.push(batch);
  library.frames.push(...jobs.map(j=>({...j,batchId:id})));
  library.updatedAt=new Date().toISOString();
  return batch;
}

function validateGeneratedFrame(result){
  assert(result&&typeof result==='object','Generator returned no result');
  assert(result.mimeType==='image/png','Each motion frame must be one PNG');
  assert(result.transparent===true,'Motion frame must have transparent background');
  assert(Number(result.width)>0&&Number(result.height)>0,'PNG dimensions missing');
  assert(result.assetRef,'PNG must be persisted before completion');
  assert(result.imageCount===undefined||Number(result.imageCount)===1,'Sprite sheets/composite boards are rejected');
  return result;
}

function buildBatchManifest(library,batch){
  return {
    format:'one-wave-motion-batch-manifest',version:1,
    libraryFormat:FORMAT,libraryVersion:VERSION,
    character:library.character,bodyVariant:library.bodyVariant,
    batchId:batch.id,batchIndex:batch.index,size:batch.size,
    frames:batch.jobs.map(j=>({libraryIndex:j.libraryIndex,batchIndex:j.batchIndex,motion:j.motion,filename:j.filename,width:j.width,height:j.height,transparent:j.transparent,assetRef:j.assetRef}))
  };
}

class MotionLibraryCreator{
  constructor({generateOne,persistLibrary,packZip,unpackZip,onProgress}={}){
    assert(typeof generateOne==='function','generateOne adapter required');
    assert(typeof persistLibrary==='function','persistLibrary adapter required');
    this.generateOne=generateOne;
    this.persistLibrary=persistLibrary;
    this.packZip=packZip;
    this.unpackZip=unpackZip;
    this.onProgress=typeof onProgress==='function'?onProgress:()=>{};
    this.running=false;this.stopRequested=false;
  }
  async checkpoint(library){library.updatedAt=new Date().toISOString();await this.persistLibrary(clone(library));this.onProgress(clone(library));}
  requestStop(){this.stopRequested=true;}
  async runBatch(library,batchId,context={}){
    assert(!this.running,'Creator already running');
    const batch=library.batches.find(b=>b.id===batchId);assert(batch,'Batch not found');
    this.running=true;this.stopRequested=false;batch.status='generating';await this.checkpoint(library);
    try{
      for(const job of batch.jobs){
        if(job.state==='saved')continue;if(this.stopRequested)break;
        job.state='generating';job.error=null;await this.checkpoint(library);
        try{
          const result=validateGeneratedFrame(await this.generateOne({character:library.character,bodyVariant:library.bodyVariant,batchId:batch.id,libraryIndex:job.libraryIndex,batchIndex:job.batchIndex,motion:job.motion,filename:job.filename,transparentBackground:true,singleFrameOnly:true,context:clone(context)}));
          Object.assign(job,{state:'saved',mimeType:'image/png',width:Number(result.width),height:Number(result.height),transparent:true,assetRef:String(result.assetRef)});
          const frame=library.frames.find(f=>f.libraryIndex===job.libraryIndex);if(frame)Object.assign(frame,clone(job),{batchId:batch.id});
          batch.completed=batch.jobs.filter(j=>j.state==='saved').length;await this.checkpoint(library);
        }catch(error){job.state='failed';job.error=String(error?.message||error);batch.status='failed';await this.checkpoint(library);throw error;}
      }
      batch.completed=batch.jobs.filter(j=>j.state==='saved').length;
      batch.status=batch.completed===batch.size?'complete':'paused';
      await this.checkpoint(library);
      return clone(batch);
    }finally{this.running=false;}
  }
  async zipBatch(library,batchId){
    assert(typeof this.packZip==='function','packZip adapter required');
    const batch=library.batches.find(b=>b.id===batchId);assert(batch,'Batch not found');assert(batch.completed===batch.size,'Batch must be complete before zipping');
    const manifest=buildBatchManifest(library,batch);
    const packed=await this.packZip({filename:`${slug(library.character)}-${slug(library.bodyVariant)}-${batch.id}.zip`,manifest,files:batch.jobs.map(j=>({filename:j.filename,assetRef:j.assetRef}))});
    assert(packed?.zipRef,'ZIP was not persisted');batch.zipRef=String(packed.zipRef);batch.manifestRef=packed.manifestRef?String(packed.manifestRef):null;await this.checkpoint(library);return clone(batch);
  }
  async importZip(library,zipRef){
    assert(typeof this.unpackZip==='function','unpackZip adapter required');
    const unpacked=await this.unpackZip(zipRef);assert(unpacked?.manifest,'ZIP manifest missing');
    const m=unpacked.manifest;assert(m.format==='one-wave-motion-batch-manifest','Wrong ZIP manifest format');assert(m.character===library.character,'ZIP belongs to another character');assert(m.bodyVariant===library.bodyVariant,'ZIP belongs to another body variant');assert(Array.isArray(m.frames),'ZIP frame list missing');
    const seen=new Set(library.frames.map(f=>f.filename));
    for(const frame of m.frames){if(seen.has(frame.filename))continue;library.frames.push({...frame,state:'saved',mimeType:'image/png',batchId:m.batchId,error:null});seen.add(frame.filename);}
    if(!library.batches.some(b=>b.id===m.batchId))library.batches.push({id:m.batchId,index:m.batchIndex,size:m.size,startIndex:Math.min(...m.frames.map(f=>f.libraryIndex)),endIndex:Math.max(...m.frames.map(f=>f.libraryIndex)),status:'complete',createdAt:new Date().toISOString(),completed:m.frames.length,zipRef:String(zipRef),manifestRef:null,jobs:m.frames.map(f=>({...f,state:'saved',mimeType:'image/png',error:null}))});
    library.frames.sort((a,b)=>a.libraryIndex-b.libraryIndex);await this.checkpoint(library);return clone(library);
  }
}

window.OneWaveMotionLibraryCreator={FORMAT,VERSION,BATCH_SIZE,makeLibrary,makeBatch,validateGeneratedFrame,buildBatchManifest,MotionLibraryCreator};
})();