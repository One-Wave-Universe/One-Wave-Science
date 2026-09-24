import {CellV1} from "./cell.js";
const cell = new CellV1();
const $ = id => document.getElementById(id);
let running = true;

function input(){
  return {a:+$("a").value,b:+$("b").value,c:+$("c").value};
}
function fmt(x){return Number(x).toFixed(3)}

function drawHex(ctx,cx,cy,r,state){
  ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);
  ctx.save(); ctx.translate(cx,cy);
  ctx.beginPath();
  for(let i=0;i<6;i++){
    const ang=-Math.PI/6+i*Math.PI/3;
    const x=Math.cos(ang)*r,y=Math.sin(ang)*r;
    if(i===0)ctx.moveTo(x,y); else ctx.lineTo(x,y);
  }
  ctx.closePath(); ctx.stroke();

  const labels=["A+","B+","C+","A-","B-","C-"];
  for(let i=0;i<6;i++){
    const ang=i*Math.PI/3;
    const x=Math.cos(ang)*(r+30),y=Math.sin(ang)*(r+30);
    ctx.fillText(labels[i],x-10,y+4);
  }

  ctx.beginPath(); ctx.arc(0,0,18,0,Math.PI*2); ctx.stroke();
  ctx.fillText(state.state,-18,5);

  const leanX = state.lean * (r*0.72);
  ctx.beginPath(); ctx.arc(leanX,0,9,0,Math.PI*2); ctx.fill();

  ctx.fillText("FIELD", -r*0.72, -r*0.55);
  ctx.fillText("VOID",  r*0.48, -r*0.55);
  ctx.restore();
}
function drawHistory(ctx,h){
  ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);
  ctx.beginPath();
  h.forEach((s,i)=>{
    const x=i/(239)*(ctx.canvas.width-10)+5;
    const y=ctx.canvas.height/2 - s.lean*(ctx.canvas.height*0.42);
    if(i===0)ctx.moveTo(x,y); else ctx.lineTo(x,y);
  });
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(0,ctx.canvas.height/2); ctx.lineTo(ctx.canvas.width,ctx.canvas.height/2); ctx.stroke();
}
function tick(){
  if(running){
    const s=cell.update(input());
    $("state").textContent=s.state;
    $("field").textContent=fmt(s.field);
    $("void").textContent=fmt(s.void);
    $("lean").textContent=fmt(s.lean);
    $("memory").textContent=fmt(s.memory);
    $("reinj").textContent=fmt(s.reinjection);
    drawHex($("dish").getContext("2d"),220,190,110,s);
    drawHistory($("history").getContext("2d"),cell.history);
  }
  requestAnimationFrame(tick);
}
$("toggle").onclick=()=>{running=!running;$("toggle").textContent=running?"Pause":"Run"};
$("pulse").onclick=()=>{cell.update(input())};
$("reset").onclick=()=>location.reload();
tick();
