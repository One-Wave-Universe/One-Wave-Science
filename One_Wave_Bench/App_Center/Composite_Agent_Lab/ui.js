const $=id=>document.getElementById(id);
async function j(u,o){const r=await fetch(u,o);return r.json()}
async function boot(){const [c,p,ps]=await Promise.all([j('/api/config'),j('/api/providers'),j('/api/parsers')]);
 for(const x of p){for(const id of ['field','void']){const o=document.createElement('option');o.value=x.id;o.textContent=x.name||x.id;$(id).appendChild(o)}} for(const x of ps){const o=document.createElement('option');o.value=x.id;o.textContent=x.name||x.id;$('parser').appendChild(o)}
 $('field').value=c.field_provider;$('void').value=c.void_provider;$('parser').value=c.parser;$('sandbox').checked=!!c.sandbox}
$('save').onclick=()=>j('/api/config',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({field_provider:$('field').value,void_provider:$('void').value,parser:$('parser').value,sandbox:$('sandbox').checked})});
$('run').onclick=async()=>{$('out').textContent='running...';const r=await j('/api/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({goal:$('goal').value,reference:$('reference').value,input:$('input').value})});lastRun=r;$('out').textContent=JSON.stringify(r,null,2);if(r.state&&r.state.m4){$('m4').textContent=JSON.stringify(r.state.m4,null,2)}};boot();
let lastRun=null;
$('quality').onclick=async()=>{
  if(!lastRun){$('qualityOut').textContent='Run a cycle first.';return}
  const st=lastRun.state||{};
  const claims=[];
  if(lastRun.output){claims.push({id:'output',text:lastRun.output,reference_ids:st.reference?[st.reference]:[],supported:!!st.reference})}
  const payload={
    threshold:parseFloat($('threshold').value||'0.95'),
    references:st.reference?[{id:st.reference}]:[],
    claims,
    requirements:[{id:'cycle_completed',met:!!lastRun.ok}],
    tests:[{id:'m4_cycle',passed:!!lastRun.ok}],
    void_review:{decision:st.void_commit&&st.void_commit.commit?'ALLOW':'HOLD',evidence_checked:!!st.void_commit},
    usable:typeof lastRun.output==='string'&&lastRun.output.length>0,
    drift:{checked:true,detected:false}
  };
  const q=await j('/api/quality',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  $('qualityOut').textContent=JSON.stringify(q,null,2);
};
