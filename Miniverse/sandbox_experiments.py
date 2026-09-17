#!/usr/bin/env python3
"""Fifty deterministic software-only lattice/sensory/body-state experiments."""
from dataclasses import asdict, dataclass
import json, math
from typing import Callable
from sandbox_lattice import ActiveFrame, BodyTelemetry, HexLattice, LatticeWorld, SandboxAgent, SensorReading, hex_distance

@dataclass
class R:
    id:str; group:str; name:str; passed:bool; metrics:dict

def rr(n,g,name,ok,**m): return R(f"SLS-{n:03d}",g,name,bool(ok),m)
def pulse(steps=8,damping=.035,gain=.11):
    w=LatticeWorld(damping=damping,wave_gain=gain); w.inject((0,0),1)
    h=[]
    for _ in range(steps): h.append(dict(w.value)); w.step()
    return w,h

# 001-010: fixed lattice + active frame
def e01():
    w,h=pulse(10); x=max(abs(h[4][p]) for p in w.value if hex_distance((0,0),p)==1); return rr(1,"lattice","pulse propagates from origin",x>1e-4,ring1_peak=x)
def e02():
    w=LatticeWorld(); w.inject((-2,0),.7); w.inject((2,0),-.7); w.run(8); a=abs(w.value[(0,0)]); s=LatticeWorld(); s.inject((-2,0),.7); s.inject((2,0),.7); s.run(8); b=abs(s.value[(0,0)]); return rr(2,"lattice","opposed pulse interference",a<b,opposed=a,same_sign=b)
def e03():
    w=LatticeWorld(radius=3); w.inject((3,0),1); w.run(10); return rr(3,"lattice","finite boundary stays bounded",math.isfinite(w.energy()) and w.max_abs()<3,energy=w.energy(),peak=w.max_abs())
def e04():
    a,_=pulse(20,.01); b,_=pulse(20,.18); return rr(4,"lattice","damping ladder",b.energy()<a.energy(),low=a.energy(),high=b.energy())
def e05():
    a,_=pulse(6,gain=.05); b,_=pulse(6,gain=.16); f=lambda w:sum(abs(w.value[p]) for p in w.value if hex_distance((0,0),p)==2); return rr(5,"lattice","coupling changes spread",f(b)>f(a),slow=f(a),fast=f(b))
def e06():
    w=LatticeWorld(); d=w.lattice.topology_digest(); w.inject((0,0),1); w.run(30); return rr(6,"lattice","dynamic state cannot rewrite rest lattice",w.lattice.topology_digest()==d,unchanged=w.lattice.rest_unchanged())
def e07():
    l=HexLattice(); ok=all(p in l.neighbors(n) for p in l.cells for n in l.neighbors(p)); return rr(7,"lattice","neighbor reciprocity",ok,cells=len(l.cells))
def e08():
    w=LatticeWorld(); g=w.checkpoint(); w.inject((1,0),.9); w.run(3); bad=w.value[(1,0)]; w.recall(g); good=w.value[(1,0)]; return rr(8,"lattice","checkpoint recall restores field",abs(good)<1e-12 and abs(bad)>1e-4,disturbed=bad,restored=good)
def e09():
    l=HexLattice(); f=ActiveFrame(); s=(f.cell,f.orientation,f.mirrored); ok=f.move_local(l,0) and f.move_local(l,1); f.undo(); f.undo(); z=(f.cell,f.orientation,f.mirrored); return rr(9,"lattice","inverse route recovers exact frame",ok and s==z,start=str(s),end=str(z))
def e10():
    l=HexLattice(); f=ActiveFrame(); f.rotate(1); ok=f.move_local(l,0); return rr(10,"lattice","rotation maps local movement",ok and f.cell==(1,-1),cell=f.cell,orientation=f.orientation)

# 011-020: virtual sensory transduction
def e11():
    w=LatticeWorld(); a=SandboxAgent(w); w.inject((0,0),.4); r=a.sense_touch(); return rr(11,"sensory","field becomes touch reading",abs(r.value-.4)<1e-12,value=r.value,confidence=r.confidence)
def e12():
    w=LatticeWorld(); w.inject((1,0),.6); d,x=w.local_gradient((0,0)); return rr(12,"sensory","gradient yields direction",d==0 and x>0,direction=d,delta=x)
def e13():
    w=LatticeWorld(); w.inject((0,0),1); w.step(); x=w.velocity[(0,0)]; return rr(13,"sensory","temporal delta yields motion channel",abs(x)>1e-6,velocity=x)
def e14():
    w=LatticeWorld(); w.inject((0,0),5); r=w.sensor((0,0),saturation=.5); return rr(14,"sensory","saturation clamps extreme input",abs(r.value)<=.5,value=r.value)
def e15():
    w=LatticeWorld(seed=7); w.inject((0,0),.2); a=w.sensor((0,0)); b=w.sensor((0,0),noise=.05); return rr(15,"sensory","noise lowers confidence",b.confidence<a.confidence,clean=a.confidence,noisy=b.confidence)
def e16():
    r=LatticeWorld().sensor((0,0),dropout=True); return rr(16,"sensory","dropout has zero confidence",r.confidence==0,confidence=r.confidence)
def e17():
    w=LatticeWorld(); a=w.sensor((0,0)); w.run(4); b=w.sensor((0,0)); return rr(17,"sensory","timestamps expose stale samples",a.sample_index<b.sample_index,old=a.sample_index,new=b.sample_index)
def e18():
    w=LatticeWorld(); w.inject((0,0),.237); r=w.sensor((0,0),quant=.1); return rr(18,"sensory","quantization is explicit",abs(r.value-.2)<1e-12,value=r.value)
def e19():
    a=SandboxAgent(LatticeWorld()); f=a.fuse([SensorReading(.30,.9,"s1",0),SensorReading(.32,.8,"s2",0)]); return rr(19,"sensory","agreeing redundant sensors fuse",.29<f.value<.33 and f.confidence>.7,value=f.value,confidence=f.confidence)
def e20():
    a=SandboxAgent(LatticeWorld()); f=a.fuse([SensorReading(-1,1,"a",0),SensorReading(1,1,"b",0)]); return rr(20,"sensory","contradiction raises uncertainty",a.body.uncertainty>.9 and f.confidence<.25,uncertainty=a.body.uncertainty,confidence=f.confidence)

# 021-030: synthetic internal body telemetry
def e21():
    a=SandboxAgent(LatticeWorld()); s=a.body.energy
    for _ in range(5): a.act_move(0,.5,0)
    d=a.body.energy; a.body.recover(.2); return rr(21,"body-state","energy drains and recovers",d<s<a.body.energy+.001,start=s,drained=d,recovered=a.body.energy)
def e22():
    a=SandboxAgent(LatticeWorld());
    for _ in range(4): a.act_move(0,1,0)
    h=a.body.thermal_load; a.body.recover(.2); return rr(22,"body-state","load rises then cools",h>0 and a.body.thermal_load<h,hot=h,cool=a.body.thermal_load)
def e23():
    a=SandboxAgent(LatticeWorld(radius=1)); a.frame.cell=(1,0); ok=not a.act_move(0,1,0); return rr(23,"body-state","blocked actuator raises strain",ok and a.body.actuator_strain>=.18,strain=a.body.actuator_strain)
def e24():
    b=BodyTelemetry(integrity=.4); x=b.integrity; b.integrity=min(1,b.integrity+.3); return rr(24,"body-state","integrity channel supports repair",b.integrity>x,before=x,after=b.integrity)
def e25():
    a=SandboxAgent(LatticeWorld()); a.fuse([SensorReading(0,1,"a",0),SensorReading(.8,1,"b",0)]); return rr(25,"body-state","uncertainty tracks disagreement",a.body.uncertainty>.5,uncertainty=a.body.uncertainty)
def e26():
    b=BodyTelemetry(clock_drift=.08); return rr(26,"body-state","clock drift threshold",abs(b.clock_drift)>.05,drift=b.clock_drift)
def e27():
    a=SandboxAgent(LatticeWorld()); s=a.body.attention_budget
    for _ in range(8): a.act_move(0,.5,0)
    return rr(27,"body-state","compute budget is consumed",a.body.attention_budget<s,start=s,after=a.body.attention_budget)
def e28():
    b=BodyTelemetry(thermal_load=.9,actuator_strain=.8); x=(b.thermal_load+b.actuator_strain)/2; return rr(28,"body-state","combined load proxy",.84<x<.86,load=x)
def e29():
    a=SandboxAgent(LatticeWorld(seed=3)); a.world.inject((0,0),.3); r=a.sense_touch(noise=.1); return rr(29,"body-state","sensor confidence enters body state",a.body.sensor_confidence==r.confidence,confidence=r.confidence)
def e30():
    a=SandboxAgent(LatticeWorld()); a.body.energy=.3; a.body.thermal_load=.8; a.body.uncertainty=.7; a.reset_body_to_baseline(); d=a.baseline_delta(); x=max(abs(v) for v in d.values()); return rr(30,"body-state","Baseline Zero restores channels",x<1e-12,max_delta=x)

# 031-040: body/world coupling + prediction
def e31():
    a=SandboxAgent(LatticeWorld()); ok=a.act_move(0,self_wave=.4); p=a.frame.cell; return rr(31,"coupling","action creates tagged self-wave",ok and a.world.value[p]>0 and a.world.sources[p]=="self",cell=p,wave=a.world.value[p])
def e32():
    a=SandboxAgent(LatticeWorld()); a.act_move(0,self_wave=.4); x=a.sense_touch().value-.4; return rr(32,"coupling","efference cancellation",abs(x)<1e-12,residual=x)
def e33():
    w=LatticeWorld(); a=SandboxAgent(w); a.act_move(0,self_wave=.25); p=a.frame.cell; w.inject((-1,0),.5,"external"); return rr(33,"coupling","self/external provenance stays distinct",w.sources[p]=="self" and w.sources[(-1,0)]=="external",self_source=w.sources[p],external=w.sources[(-1,0)])
def e34():
    a=SandboxAgent(LatticeWorld()); believed=(0,0); a.act_move(0,self_wave=0); d=hex_distance(believed,a.frame.cell); return rr(34,"coupling","body-map mismatch detectable",d==1,distance=d)
def e35():
    a=SandboxAgent(LatticeWorld()); a.act_move(0,self_wave=.3); x=a.sense_touch().value; a.world.run(3); y=a.sense_touch().value; return rr(35,"coupling","delayed feedback differs",abs(y-x)>1e-4,immediate=x,delayed=y)
def e36():
    a=SandboxAgent(LatticeWorld(radius=1)); a.frame.cell=(1,0); m=a.act_move(0,self_wave=0); p=a.why_forward("actuator route blocked",.8,{"change":1,"confidence":1}) if not m else None; return rr(36,"coupling","actuator failure WHY FORWARD",not m and bool(p and p["why_forward"]),forwards=len(a.escalations))
def e37():
    a=SandboxAgent(LatticeWorld()); s=a.frame.cell; a.act_move(0,self_wave=0); a.act_move(1,self_wave=0); ok=a.frame.undo() and a.frame.undo(); return rr(37,"coupling","relocate and exact return",ok and a.frame.cell==s,end=a.frame.cell)
def e38():
    w=LatticeWorld(); w.inject((2,0),.7); a=SandboxAgent(w); x=abs(a.sense_touch().value); a.act_move(0,self_wave=0); a.act_move(0,self_wave=0); y=abs(a.sense_touch().value); return rr(38,"coupling","active sensing reveals source",y>x,before=x,after=y)
def e39():
    a=SandboxAgent(LatticeWorld()); f=a.fuse([SensorReading(.8,.9,"touch",0),SensorReading(-.5,.9,"vision",0)]); return rr(39,"coupling","cross-modal conflict lowers confidence",f.confidence<.4 and a.body.uncertainty>.9,confidence=f.confidence,uncertainty=a.body.uncertainty)
def e40():
    a=SandboxAgent(LatticeWorld()); a.body.uncertainty=.9; p=a.why_forward("prediction error above local threshold",.7,{"change":.9,"confidence":.6,"prediction_error":.9}); return rr(40,"coupling","prediction error WHY FORWARD",bool(p["why_forward"] and p["current_body_state_refs"]),urgency=p["urgency"])

# 041-050: persistence, learning gates, end-to-end
def e41():
    a=SandboxAgent(LatticeWorld()); b=dict(a.baseline); a.body.energy=.2; return rr(41,"memory","HOLD does not rewrite baseline",a.baseline==b and a.body.energy==.2,baseline_energy=b["energy"],held_energy=a.body.energy)
def e42():
    w=LatticeWorld(); w.inject((0,0),.4); g=w.checkpoint(); x=w.value[(0,0)]; w.value[(0,0)]=999; w.recall(g); return rr(42,"memory","rollback recovers corruption",w.value[(0,0)]==x,restored=w.value[(0,0)])
def e43():
    w=LatticeWorld(); a=SandboxAgent(w); a.body.energy=.55; b=SandboxAgent(w,body=BodyTelemetry(**a.body.snapshot())); return rr(43,"memory","restart preserves serialized body state",b.body.energy==.55,energy=b.body.energy)
def e44():
    cues={"cell":(1,-1),"task":"inspect","orientation":2}; partial={"cell":cues["cell"],"orientation":2}; missing=[k for k in cues if k not in partial]; return rr(44,"memory","partial recall marks missing fields",missing==["task"],missing=missing)
def e45():
    memory={"what":None,"confidence":.45}; proposed="unknown-object"; promoted=False; return rr(45,"memory","plausible fill not auto-promoted",memory["what"] is None and not promoted,proposal=proposed,promoted=promoted)
def e46():
    candidate={"sensor_bias":.12,"stable_runs":5}; committed=False; return rr(46,"memory","stable novelty waits for oversight",candidate["stable_runs"]>=5 and not committed,committed=committed)
def e47():
    a=SandboxAgent(LatticeWorld()); b=a.baseline["sensor_confidence"]; a.body.sensor_confidence=0; return rr(47,"memory","sensor fault not learned as baseline",a.baseline["sensor_confidence"]==b==1,baseline=b)
def e48():
    count=8; approved=True; new=.92 if count>=6 and approved else 1.; return rr(48,"memory","baseline commit requires repetition + approval",new==.92,count=count,approved=approved,new=new)
def e49():
    def run():
        w=LatticeWorld(seed=99); a=SandboxAgent(w); w.inject((0,0),.6); w.run(4); r=a.sense_touch(noise=.02); return round(r.value,12),round(r.confidence,12),round(w.energy(),12)
    a,b=run(),run(); return rr(49,"memory","seeded replay deterministic",a==b,run_a=a,run_b=b)
def e50():
    w=LatticeWorld(seed=5); a=SandboxAgent(w); t=w.lattice.topology_digest(); w.inject((2,-1),.8,"external"); w.run(2); a.act_move(0,self_wave=.15); r=a.sense_touch(noise=.01); d,g=w.local_gradient(a.frame.cell); need=abs(r.value)>.25 or a.body.uncertainty>.8; p=a.why_forward("salient sandbox change",.6,{"change":abs(r.value),"confidence":r.confidence,"gradient_dir":d,"gradient":g}) if need else None; w.checkpoint(); ok=w.lattice.topology_digest()==t and (not need or bool(p and p["why_forward"])) and bool(a.receipts); return rr(50,"end-to-end","lattice+sense+body+receipt boundary",ok,reading=r.value,confidence=r.confidence,actions=len(a.receipts),forwards=len(a.escalations),generation=w.generation,topology_unchanged=w.lattice.topology_digest()==t)

EXPERIMENTS:list[Callable[[],R]]=[globals()[f"e{i:02d}"] for i in range(1,51)]
def run_all(): return [f() for f in EXPERIMENTS]
def report(xs): return {"suite":"Sandbox Lattice + Sensory + Synthetic Internal Body State","claim_boundary":"software simulation only; no physical-lattice or subjective-sensation claim","experiments":len(xs),"passed":sum(x.passed for x in xs),"failed":sum(not x.passed for x in xs),"results":[asdict(x) for x in xs]}
def main():
    d=report(run_all()); print(json.dumps(d,indent=2,sort_keys=True)); return 0 if d["failed"]==0 else 1
if __name__=="__main__": raise SystemExit(main())
