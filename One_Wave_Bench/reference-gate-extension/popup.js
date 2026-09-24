const ids=["source","target","direction","reference","intention","consequence","selectedRoute","fallbackRoutes"];
const by=id=>document.getElementById(id);
chrome.storage.local.get(["oneWaveGateEnabled","oneWaveGateHosts","oneWaveReferenceCard"],v=>{
  by("enabled").checked=Boolean(v.oneWaveGateEnabled);
  by("hosts").value=(v.oneWaveGateHosts||[]).join("\n");
  const c=v.oneWaveReferenceCard||{};
  ids.forEach(id=>by(id).value=c[id]||"");
});
by("save").addEventListener("click",()=>{
  const card={timestamp:new Date().toISOString()};
  ids.forEach(id=>card[id]=by(id).value.trim());
  const hosts=by("hosts").value.split(/\n+/).map(x=>x.trim()).filter(Boolean);
  chrome.storage.local.set({oneWaveGateEnabled:by("enabled").checked,oneWaveGateHosts:hosts,oneWaveReferenceCard:card});
  by("save").textContent="Saved";
  setTimeout(()=>by("save").textContent="Save reference card",900);
});