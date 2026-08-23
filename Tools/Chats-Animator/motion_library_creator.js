(()=>{
  'use strict';
  const BATCH_SIZE=50;
  const FORMAT='one-wave-character-motion-library';
  const VERSION=2;
  const clone=v=>JSON.parse(JSON.stringify(v));
  const assert=(c,m)=>{if(!c)throw new Error(m)};
  const slug=(v,f='pose')=>String(v||f).trim().replace(/[^a-z0-9_-]+/gi,'-').replace(/^-+|-+$/g,'').toLowerCase()||f;

  function makeLibrary({character,bodyVariant='base'}={}){
    assert(character,'Character is required');
    return {format:FORMAT,version:VERSION,character:String(character),bodyVariant:String(bodyVariant),createdAt:new Date().toISOString(),updatedAt:new Date().toISOString(),frames:[],batches:[],status:'idle'};
  }

  function makeBatch(library,motions){
    assert(library?.format===FORMAT,'Unsupported motion library');
    assert(Array.isArray(motions)&&motions.length>0&&motions.length<=BATCH_SIZE,`Batch must contain 1-${BATCH_SIZE} motions`);
    const start=library.frames.length;
    const batchId=`batch-${String(library.batches.length+1).padStart(4,'0')}`;
    const jobs=motions.map((motion,i)=>({
      globalIndex:start+i,
      batchIndex:i,
      motion:String(motion),
      state:'pending',
      filename:`${String(start+i+1).padStart(5,'0')}_${slug(motion)}.png`,
      width:null,height:null,transparent:null,assetRef:null,error:null
    }));
    library.frames.push(...jobs);
    library.batches.push({id:batchId,start,count:jobs.length,status:'pending'});
    library.updatedAt=new Date().toISOString();
    return batchId;
  }

  function validateFrame(result){
    assert(result&&typeof result==='object','No generated frame');
    assert(result.mimeType==='image/png','One PNG per generation job is required');
    assert(result.transparent===true,'Transparent background required');
    assert(result.imageCount===undefined||Number(result.imageCount)===1,'Sprite sheets/composite boards rejected');
    assert(Number(result.width)>0&&Number(result.height)>0,'PNG dimensions missing');
    assert(result.assetRef,'PNG must be persisted before completion');
  }

  class MotionLibraryCreator{
    constructor({generateOne,persistLibrary,onProgress}={}){
      assert(typeof generateOne==='function','generateOne adapter required');
      assert(typeof persistLibrary==='function','persistLibrary adapter required');
      this.generateOne=generateOne;this.persistLibrary=persistLibrary;this.onProgress=typeof onProgress==='function'?onProgress:()=>{};this.running=false;this.stopRequested=false;
    }
    requestStop(){this.stopRequested=true;}
    async checkpoint(library){library.updatedAt=new Date().toISOString();await this.persistLibrary(clone(library));this.onProgress(clone(library));}
    async runBatch(library,batchId,context={}){
      if(this.running)throw new Error('Creator already running');
      const batch=library.batches.find(b=>b.id===batchId);assert(batch,'Unknown batch');
      this.running=true;this.stopRequested=false;batch.status='generating';await this.checkpoint(library);
      try{
        for(let i=batch.start;i<batch.start+batch.count;i+=1){
          const frame=library.frames[i];if(frame.state==='saved')continue;if(this.stopRequested)break;
          frame.state='generating';frame.error=null;await this.checkpoint(library);
          try{
            const result=await this.generateOne({character:library.character,bodyVariant:library.bodyVariant,index:frame.globalIndex,motion:frame.motion,filename:frame.filename,transparentBackground:true,singleFrameOnly:true,context:clone(context)});
            frame.state='validating';await this.checkpoint(library);validateFrame(result);
            frame.width=Number(result.width);frame.height=Number(result.height);frame.transparent=true;frame.assetRef=String(result.assetRef);frame.state='saved';await this.checkpoint(library);
          }catch(error){frame.state='failed';frame.error=String(error?.message||error);batch.status='failed';await this.checkpoint(library);throw error;}
        }
        batch.status=library.frames.slice(batch.start,batch.start+batch.count).every(f=>f.state==='saved')?'complete':'paused';
      }finally{this.running=false;library.status=library.batches.every(b=>b.status==='complete')?'complete':'idle';await this.checkpoint(library);}
      return clone(library);
    }
  }

  window.OneWaveMotionLibraryCreator={BATCH_SIZE,FORMAT,VERSION,makeLibrary,makeBatch,validateFrame,MotionLibraryCreator};
})();
