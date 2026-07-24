#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass,asdict
from pathlib import Path
import argparse,csv,hashlib,json,math
import numpy as np
import matplotlib.pyplot as plt
SQ3=math.sqrt(3)
@dataclass
class P:
 grid_radius:int=6; spacing:float=1.; dt:float=1/180; duration:float=12.; node_mass:float=1.; packet_mass:float=2.4; packet_inertia:float=1.6; spring:float=12.; anchor:float=1.6; edge_damp:float=.55; local_damp:float=.18; well_follow:float=4.2; well_depth:float=1.7; well_radius:float=3.7; gravity:float=1.25; pressure:float=4.2; compression:float=2.; packet_radius:float=1.15; asymmetry:float=.24; spin_coupling:float=1.7; packet_damp:float=.045; well_x:float=0.; well_y:float=0.; sample_stride:int=6
@dataclass
class Q: x:float;y:float;vx:float;vy:float;theta:float;omega:float

def lattice(p):
 c=[]; idx={}
 for q in range(-p.grid_radius,p.grid_radius+1):
  for r in range(max(-p.grid_radius,-q-p.grid_radius),min(p.grid_radius,-q+p.grid_radius)+1):
   idx[q,r]=len(c);c.append((q,r,q+r/2,SQ3*r/2))
 base=np.array([[x,y,0.] for _,_,x,y in c]);e=[]
 for q,r,_,_ in c:
  i=idx[q,r]
  for dq,dr in ((1,0),(0,1),(-1,1)):
   if (q+dq,r+dr) in idx:e.append((i,idx[q+dq,r+dr]))
 return base,np.array(e,dtype=int)
def target(x,y,p):
 dx=x-p.well_x;dy=y-p.well_y;return -p.well_depth*np.exp(-(dx*dx+dy*dy)/(2*p.well_radius**2))
def grad(x,y,p):
 z=target(x,y,p);return -z*(x-p.well_x)/p.well_radius**2,-z*(y-p.well_y)/p.well_radius**2
def shell_force(q,p,N=24):
 a=p.packet_radius*(1+p.asymmetry);b=p.packet_radius*(1-.55*p.asymmetry);ct=math.cos(q.theta);st=math.sin(q.theta);fx=fy=tau=0.
 for k in range(N):
  ang=2*math.pi*k/N;bx=a*math.cos(ang);by=b*math.sin(ang);rx=ct*bx-st*by;ry=st*bx+ct*by;gx,gy=grad(q.x+rx,q.y+ry,p);sx=-p.gravity*gx;sy=-p.gravity*gy;fx+=sx;fy+=sy;tau+=rx*sy-ry*sx
 return fx/N-p.packet_damp*q.vx,fy/N-p.packet_damp*q.vy,p.spin_coupling*tau/N-.045*q.omega
def lattice_force(base,u,v,edges,q,p):
 pos=base+u;F=-p.anchor*u-p.local_damp*v;ia=edges[:,0];ib=edges[:,1];d=pos[ib]-pos[ia];L=np.linalg.norm(d,axis=1);h=d/np.where(L<1e-12,1,L)[:,None];stretch=L-p.spacing;rv=np.einsum('ij,ij->i',v[ib]-v[ia],h);fv=(p.spring*stretch+p.edge_damp*rv)[:,None]*h;np.add.at(F,ia,fv);np.add.at(F,ib,-fv);strain=np.zeros(len(base));np.maximum.at(strain,ia,np.abs(stretch));np.maximum.at(strain,ib,np.abs(stretch));comp=np.zeros(len(base));cc=np.maximum(-stretch,0);np.add.at(comp,ia,cc);np.add.at(comp,ib,cc);x=pos[:,0];y=pos[:,1];z=target(x,y,p);gx,gy=grad(x,y,p);F[:,2]+=p.well_follow*(z-pos[:,2]);F[:,0]-=.22*p.well_follow*gx;F[:,1]-=.22*p.well_follow*gy;dx=x-q.x;dy=y-q.y;rr=np.hypot(dx,dy)+1e-12;sp=math.hypot(q.vx,q.vy);hx,hy=(q.vx/sp,q.vy/sp) if sp>1e-8 else (math.cos(q.theta),math.sin(q.theta));g=np.exp(-rr*rr/(2*(p.packet_radius*1.35)**2));front=np.clip((dx*hx+dy*hy)/rr,-1,1);sk=1+.5*front;F[:,2]-=p.pressure*g*sk;pull=-p.compression*g*sk;F[:,0]+=pull*dx/rr;F[:,1]+=pull*dy/rr;springE=float(np.sum(.5*p.spring*stretch*stretch));return F,strain,comp,springE
def sim(name,p,q0,out):
 base,edges=lattice(p);u=np.zeros_like(base);v=np.zeros_like(base);q=Q(**asdict(q0));rows=[];mxs=0
 for step in range(round(p.duration/p.dt)+1):
  F,s,c,se=lattice_force(base,u,v,edges,q,p);v+=F/p.node_mass*p.dt;u+=v*p.dt;fx,fy,tau=shell_force(q,p);q.vx+=fx/p.packet_mass*p.dt;q.vy+=fy/p.packet_mass*p.dt;q.x+=q.vx*p.dt;q.y+=q.vy*p.dt;q.omega+=tau/p.packet_inertia*p.dt;q.theta+=q.omega*p.dt;mxs=max(mxs,float(s.max(initial=0)))
  if step%p.sample_stride==0:
   dx=q.x-p.well_x;dy=q.y-p.well_y;speed=math.hypot(q.vx,q.vy);rows.append(dict(t=step*p.dt,x=q.x,y=q.y,well_distance=math.hypot(dx,dy),speed=speed,spin=q.omega,orientation=q.theta,orbital_L=dx*q.vy-dy*q.vx,max_strain=float(s.max(initial=0)),max_compression=float(c.max(initial=0)),rms_displacement=float(np.sqrt(np.mean(np.sum(u*u,axis=1)))),lattice_energy_proxy=float(.5*np.sum(v*v)+se),packet_energy_proxy=.5*p.packet_mass*speed**2+.5*p.packet_inertia*q.omega**2))
 csvp=out/f'{name}.csv';w=csv.DictWriter(csvp.open('w',newline=''),fieldnames=rows[0].keys());w.writeheader();w.writerows(rows);spin=np.array([r['spin'] for r in rows]);dist=np.array([r['well_distance'] for r in rows]);orb=np.array([r['orbital_L'] for r in rows]);return rows,dict(case=name,parameters=asdict(p),initial=asdict(q0),samples=len(rows),distance_min=float(dist.min()),distance_max=float(dist.max()),max_abs_spin=float(np.abs(spin).max()),final_spin=float(spin[-1]),mean_abs_orbital_L=float(np.abs(orb).mean()),max_strain=mxs,csv_sha256=hashlib.sha256(csvp.read_bytes()).hexdigest())
def plot(res,out):
 fig,ax=plt.subplots(2,2,figsize=(12,9))
 for name,(r,_) in res.items():
  t=[x['t'] for x in r];ax[0,0].plot([x['x'] for x in r],[x['y'] for x in r],label=name);ax[0,1].plot(t,[x['well_distance'] for x in r],label=name);ax[1,0].plot(t,[x['spin'] for x in r],label=name);ax[1,1].plot(t,[x['max_strain'] for x in r],label=name)
 titles=['Displacement-center path','Distance from curvature-well center','Axial spin from shell torque','Maximum lattice edge strain']
 for a,title in zip(ax.flat,titles):a.set_title(title);a.grid(alpha=.25);a.legend(fontsize=8)
 ax[0,0].axis('equal');fig.tight_layout();fig.savefig(out/'d413_case_comparison.png',dpi=170);plt.close(fig)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='results');a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);p=P();r=p.well_radius;ov=math.sqrt(max(.05,p.gravity*p.well_depth/(r*1.5)));cases={'off_axis_drop':(p,Q(-r*1.6,r*.72,1.05,-.08,.6,0)),'orbit_asymmetric':(p,Q(r*1.25,0,0,ov,.35,.08)),'orbit_symmetric_ablation':(P(**{**asdict(p),'asymmetry':0.}),Q(r*1.25,0,0,ov,.35,0)),'no_well_control':(P(**{**asdict(p),'well_depth':0.,'gravity':0.,'well_follow':0.}),Q(-4,1,.7,0,.2,0)),'zero_input_drift':(P(**{**asdict(p),'well_depth':0.,'gravity':0.,'well_follow':0.,'pressure':0.,'compression':0.}),Q(0,0,0,0,0,0))};res={};summ=[]
 for n,(pp,q) in cases.items():res[n]=sim(n,pp,q,out);summ.append(res[n][1])
 plot(res,out);by={x['case']:x for x in summ};checks={'zero_input_drift_below_1e-12':by['zero_input_drift']['distance_max']<1e-12 and by['zero_input_drift']['max_strain']<1e-12,'asymmetric_shell_generates_more_spin_than_symmetric_ablation':by['orbit_asymmetric']['max_abs_spin']>by['orbit_symmetric_ablation']['max_abs_spin']+1e-5,'well_changes_path_relative_to_no_well_control':by['off_axis_drop']['distance_min']<by['off_axis_drop']['distance_max']-.2,'lattice_deforms_when_pressure_is_active':by['orbit_asymmetric']['max_strain']>1e-4};payload={'model':'D-413 reduced triangular Ground lattice + imposed curvature well + bounded displacement shell','status':'YELLOW reduced model','limitations':['Curvature well is imposed, not derived.','Bounded displacement is a collective shell coordinate, not a derived quark.','Energy values are proxies because external well-follow and damping terms exchange work.','Finite tests do not establish gravity, charge, proton structure, or Mass Effect.'],'checks':checks,'all_checks_pass':all(checks.values()),'cases':summ};(out/'d413_summary.json').write_text(json.dumps(payload,indent=2));print(json.dumps({'all_checks_pass':payload['all_checks_pass'],'checks':checks},indent=2));raise SystemExit(0 if payload['all_checks_pass'] else 1)
if __name__=='__main__':main()
