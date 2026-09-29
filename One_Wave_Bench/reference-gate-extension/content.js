(() => {
  const REQUIRED=["source","target","direction","reference","intention","consequence","selectedRoute","fallbackRoutes"];
  const state={enabled:false,hosts:[],card:null};
  const validCard=c=>c&&typeof c==="object"&&REQUIRED.every(k=>typeof c[k]==="string"&&c[k].trim());
  const enabled=()=>state.enabled&&state.hosts.includes(location.hostname);
  function overlay(reason){
    let box=document.getElementById("one-wave-reference-gate");
    if(!box){box=document.createElement("div");box.id="one-wave-reference-gate";Object.assign(box.style,{position:"fixed",zIndex:2147483647,top:"12px",right:"12px",maxWidth:"420px",padding:"12px",background:"#111",color:"#fff",border:"2px solid #fff",borderRadius:"8px",font:"13px/1.4 sans-serif",whiteSpace:"pre-wrap"});document.documentElement.appendChild(box);}
    const c=state.card||{};
    box.textContent="Reference Goblin HOLD\n\n"+reason+"\n\nReference: "+(c.reference||"MISSING")+"\nRoute: "+(c.selectedRoute||"MISSING")+"\nFallback: "+(c.fallbackRoutes||"MISSING")+"\n\nOpen the One-Wave extension popup to create/update the reference card.";
  }
  function looksLikeSend(el){if(!(el instanceof Element))return false;const t=[el.getAttribute("aria-label"),el.getAttribute("title"),el.textContent].filter(Boolean).join(" ").toLowerCase();return /\b(send|submit|post|run|execute|apply)\b/.test(t);}
  function gate(e,reason){if(!enabled())return;if(!validCard(state.card)){e.preventDefault();e.stopImmediatePropagation();overlay(reason);return;}state.card.timestamp=new Date().toISOString();chrome.storage.local.set({oneWaveReferenceCard:state.card});}
  document.addEventListener("submit",e=>gate(e,"Submission held: reference card incomplete."),true);
  document.addEventListener("click",e=>{if(looksLikeSend(e.target))gate(e,"Outbound action held: reference card incomplete.");},true);
  document.addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey&&(e.ctrlKey||e.metaKey))gate(e,"Keyboard send held: reference card incomplete.");},true);
  chrome.storage.local.get(["oneWaveGateEnabled","oneWaveGateHosts","oneWaveReferenceCard"],v=>{state.enabled=Boolean(v.oneWaveGateEnabled);state.hosts=Array.isArray(v.oneWaveGateHosts)?v.oneWaveGateHosts:[];state.card=v.oneWaveReferenceCard||null;});
  chrome.storage.onChanged.addListener(ch=>{if(ch.oneWaveGateEnabled)state.enabled=Boolean(ch.oneWaveGateEnabled.newValue);if(ch.oneWaveGateHosts)state.hosts=ch.oneWaveGateHosts.newValue||[];if(ch.oneWaveReferenceCard)state.card=ch.oneWaveReferenceCard.newValue||null;});
})();