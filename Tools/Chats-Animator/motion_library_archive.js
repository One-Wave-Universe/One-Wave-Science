(()=>{
  'use strict';
  const MANIFEST='library.json';
  const assert=(c,m)=>{if(!c)throw new Error(m)};
  const clone=v=>JSON.parse(JSON.stringify(v));

  function buildArchivePlan(library){
    assert(library?.format==='one-wave-character-motion-library','Unsupported motion library');
    const entries=[{path:MANIFEST,type:'json',content:JSON.stringify(library,null,2)}];
    for(const frame of library.frames||[]){
      if(frame.state!=='saved'||!frame.assetRef)continue;
      entries.push({path:`frames/${frame.filename}`,type:'asset',assetRef:frame.assetRef,mimeType:'image/png'});
    }
    return {character:library.character,bodyVariant:library.bodyVariant,entries};
  }

  async function exportZip(library,{zipWriter,readAsset}={}){
    assert(typeof zipWriter==='function','zipWriter adapter required');
    assert(typeof readAsset==='function','readAsset adapter required');
    const plan=buildArchivePlan(library);
    const files=[];
    for(const entry of plan.entries){
      if(entry.type==='json') files.push({path:entry.path,data:entry.content,mimeType:'application/json'});
      else files.push({path:entry.path,data:await readAsset(entry.assetRef),mimeType:'image/png'});
    }
    return zipWriter(files,{filename:`${String(library.character||'character').replace(/[^a-z0-9_-]+/gi,'-').toLowerCase()}-motion-library.zip`});
  }

  async function importZip(zipData,{zipReader,persistAsset}={}){
    assert(typeof zipReader==='function','zipReader adapter required');
    assert(typeof persistAsset==='function','persistAsset adapter required');
    const files=await zipReader(zipData);
    const manifest=files.find(f=>f.path===MANIFEST);
    assert(manifest,'ZIP is missing library.json');
    const library=JSON.parse(typeof manifest.data==='string'?manifest.data:new TextDecoder().decode(manifest.data));
    assert(library?.format==='one-wave-character-motion-library','ZIP manifest is not a motion library');
    for(const frame of library.frames||[]){
      if(frame.state!=='saved')continue;
      const file=files.find(f=>f.path===`frames/${frame.filename}`);
      assert(file,`ZIP is missing ${frame.filename}`);
      frame.assetRef=await persistAsset({character:library.character,bodyVariant:library.bodyVariant,filename:frame.filename,mimeType:'image/png',data:file.data});
      frame.transparent=true;
    }
    return clone(library);
  }

  window.OneWaveMotionLibraryArchive={MANIFEST,buildArchivePlan,exportZip,importZip};
})();
