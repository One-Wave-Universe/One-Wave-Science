#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass, asdict, replace
from pathlib import Path
import argparse, csv, hashlib, json, math
import numpy as np
import matplotlib.pyplot as plt
SQ3 = math.sqrt(3.0)

@dataclass
class Params:
    grid_radius:int=8; spacing:float=1.0; dt:float=1/240; duration:float=14.0
    node_mass:float=1.0; packet_mass:float=2.4; packet_inertia:float=1.6
    spring:float=12.0; anchor:float=1.6; edge_damp:float=.55; local_damp:float=.18
    well_follow:float=4.2; well_depth:float=1.7; well_radius:float=3.7; gravity:float=1.25
    pressure:float=4.2; compression:float=2.0; packet_radius:float=1.15
    asymmetry:float=.24; spin_coupling:float=1.7; packet_damp:float=.045
    well_x:float=0.0; well_y:float=0.0; sample_stride:int=8
    boundary:str='absorbing'; boundary_damp:float=1.25

@dataclass
class Packet:
    x:float; y:float; vx:float; vy:float; theta:float; omega:float

def lattice(p:Params):
    cells=[]; idx={}
    for q in range(-p.grid_radius,p.grid_radius+1):
        for r in range(max(-p.grid_radius,-q-p.grid_radius),min(p.grid_radius,-q+p.grid_radius)+1):
            idx[q,r]=len(cells); cells.append((q,r,q+r/2,SQ3*r/2))
    base=np.array([[x,y,0.] for _,_,x,y in cells],float); edges=[]; rim=[]
    for q,r,_,_ in cells:
        i=idx[q,r]; rim.append(max(abs(q),abs(r),abs(q+r))==p.grid_radius)
        for dq,dr in ((1,0),(0,1),(-1,1)):
            if (q+dq,r+dr) in idx: edges.append((i,idx[q+dq,r+dr]))
    return base,np.asarray(edges,int),np.asarray(rim,bool)

def target(x,y,p):
    dx=x-p.well_x; dy=y-p.well_y
    return -p.well_depth*np.exp(-(dx*dx+dy*dy)/(2*p.well_radius**2))

def grad(x,y,p):
    z=target(x,y,p)
    return -z*(x-p.well_x)/p.well_radius**2, -z*(y-p.well_y)/p.well_radius**2

def shell_force(q,p,N=32):
    a=p.packet_radius*(1+p.asymmetry); b=p.packet_radius*(1-.55*p.asymmetry)
    ct,st=math.cos(q.theta),math.sin(q.theta); fx=fy=tau=0.
    for k in range(N):
        ang=2*math.pi*k/N; bx=a*math.cos(ang); by=b*math.sin(ang)
        rx=ct*bx-st*by; ry=st*bx+ct*by; gx,gy=grad(q.x+rx,q.y+ry,p)
        sx,sy=-p.gravity*gx,-p.gravity*gy; fx+=sx; fy+=sy; tau+=rx*sy-ry*sx
    return fx/N-p.packet_damp*q.vx, fy/N-p.packet_damp*q.vy, p.spin_coupling*tau/N-.045*q.omega

def forces(base,u,v,edges,rim,q,p):
    pos=base+u; F=-p.anchor*u-p.local_damp*v
    ia,ib=edges[:,0],edges[:,1]; d=pos[ib]-pos[ia]; L=np.linalg.norm(d,axis=1)
    h=d/np.where(L<1e-12,1,L)[:,None]; stretch=L-p.spacing
    rv=np.einsum('ij,ij->i',v[ib]-v[ia],h)
    fv=(p.spring*stretch+p.edge_damp*rv)[:,None]*h
    np.add.at(F,ia,fv); np.add.at(F,ib,-fv)
    strain=np.zeros(len(base)); np.maximum.at(strain,ia,np.abs(stretch)); np.maximum.at(strain,ib,np.abs(stretch))
    comp=np.zeros(len(base)); cc=np.maximum(-stretch,0); np.add.at(comp,ia,cc); np.add.at(comp,ib,cc)
    x,y=pos[:,0],pos[:,1]; z=target(x,y,p); gx,gy=grad(x,y,p)
    F[:,2]+=p.well_follow*(z-pos[:,2]); F[:,0]-=.22*p.well_follow*gx; F[:,1]-=.22*p.well_follow*gy
    dx=x-q.x; dy=y-q.y; rr=np.hypot(dx,dy)+1e-12; sp=math.hypot(q.vx,q.vy)
    hx,hy=(q.vx/sp,q.vy/sp) if sp>1e-8 else (math.cos(q.theta),math.sin(q.theta))
    g=np.exp(-rr*rr/(2*(p.packet_radius*1.35)**2)); front=np.clip((dx*hx+dy*hy)/rr,-1,1); skew=1+.5*front
    F[:,2]-=p.pressure*g*skew; pull=-p.compression*g*skew; F[:,0]+=pull*dx/rr; F[:,1]+=pull*dy/rr
    if p.boundary=='fixed': F[rim]=0
    elif p.boundary=='absorbing': F[rim]-=p.boundary_damp*v[rim]
    spring_e=float(np.sum(.5*p.spring*stretch*stretch)); anchor_e=float(.5*p.anchor*np.sum(u*u))
    damping_power=float(p.local_damp*np.sum(v*v)+p.edge_damp*np.sum(rv*rv)+p.boundary_damp*np.sum(v[rim]**2) if p.boundary=='absorbing' else p.local_damp*np.sum(v*v)+p.edge_damp*np.sum(rv*rv))
    return F,strain,comp,spring_e,anchor_e,damping_power

def simulate(name,p,q0,out):
    base,edges,rim=lattice(p); u=np.zeros_like(base); v=np.zeros_like(base); q=Packet(**asdict(q0))
    rows=[]; dissipated=0.; initial_energy=None; max_strain=0.; max_comp=0.
    steps=round(p.duration/p.dt)
    for step in range(steps+1):
        F,s,c,se,ae,dp=forces(base,u,v,edges,rim,q,p)
        # kick-drift-kick (symplectic with damping forces evaluated twice)
        v += .5*(F/p.node_mass)*p.dt; u += v*p.dt
        fx,fy,tau=shell_force(q,p); q.vx+=.5*fx/p.packet_mass*p.dt; q.vy+=.5*fy/p.packet_mass*p.dt; q.omega+=.5*tau/p.packet_inertia*p.dt
        q.x+=q.vx*p.dt; q.y+=q.vy*p.dt; q.theta+=q.omega*p.dt
        F2,s,c,se,ae,dp2=forces(base,u,v,edges,rim,q,p); v += .5*(F2/p.node_mass)*p.dt
        fx,fy,tau=shell_force(q,p); q.vx+=.5*fx/p.packet_mass*p.dt; q.vy+=.5*fy/p.packet_mass*p.dt; q.omega+=.5*tau/p.packet_inertia*p.dt
        if p.boundary=='fixed': u[rim]=0; v[rim]=0
        dissipated += .5*(dp+dp2)*p.dt; max_strain=max(max_strain,float(s.max(initial=0))); max_comp=max(max_comp,float(c.max(initial=0)))
        if step%p.sample_stride==0:
            dx=q.x-p.well_x; dy=q.y-p.well_y; speed=math.hypot(q.vx,q.vy)
            lattice_ke=float(.5*p.node_mass*np.sum(v*v)); packet_ke=.5*p.packet_mass*speed**2+.5*p.packet_inertia*q.omega**2
            well_pe=float(p.packet_mass*p.gravity*target(q.x,q.y,p)); mechanical=lattice_ke+se+ae+packet_ke+well_pe
            if initial_energy is None: initial_energy=mechanical
            balance=mechanical+dissipated-initial_energy
            rows.append(dict(t=step*p.dt,x=q.x,y=q.y,well_distance=math.hypot(dx,dy),speed=speed,spin=q.omega,orientation=q.theta,orbital_L=dx*q.vy-dy*q.vx,max_strain=float(s.max(initial=0)),max_compression=float(c.max(initial=0)),rms_displacement=float(np.sqrt(np.mean(np.sum(u*u,axis=1)))),mechanical_energy=mechanical,dissipated_energy=dissipated,energy_balance_error=balance))
    csvp=out/f'{name}.csv';
    with csvp.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    dist=np.array([r['well_distance'] for r in rows]); spin=np.array([r['spin'] for r in rows]); bal=np.array([r['energy_balance_error'] for r in rows])
    tail=max(2,len(rows)//5); recovery=float(np.mean(dist[-tail:]));
    return rows,dict(case=name,parameters=asdict(p),initial=asdict(q0),samples=len(rows),distance_min=float(dist.min()),distance_max=float(dist.max()),tail_mean_distance=recovery,max_abs_spin=float(np.abs(spin).max()),final_spin=float(spin[-1]),max_strain=max_strain,max_compression=max_comp,max_abs_energy_balance_error=float(np.abs(bal).max()),csv_sha256=hashlib.sha256(csvp.read_bytes()).hexdigest())

def plot(results,out):
    fig,ax=plt.subplots(2,3,figsize=(15,9))
    for name,(rows,_) in results.items():
        t=[r['t'] for r in rows]; ax[0,0].plot([r['x'] for r in rows],[r['y'] for r in rows],label=name)
        ax[0,1].plot(t,[r['well_distance'] for r in rows],label=name); ax[0,2].plot(t,[r['spin'] for r in rows],label=name)
        ax[1,0].plot(t,[r['max_strain'] for r in rows],label=name); ax[1,1].plot(t,[r['mechanical_energy'] for r in rows],label=name); ax[1,2].plot(t,[r['energy_balance_error'] for r in rows],label=name)
    titles=['Center path','Distance to well','Axial spin','Maximum strain','Mechanical energy','Energy balance error']
    for a,title in zip(ax.flat,titles): a.set_title(title); a.grid(alpha=.25); a.legend(fontsize=7)
    ax[0,0].axis('equal'); fig.tight_layout(); fig.savefig(out/'d413_case_comparison.png',dpi=170); plt.close(fig)

def run_suite(out):
    p=Params(); r=p.well_radius; ov=math.sqrt(max(.05,p.gravity*p.well_depth/(r*1.5)))
    cases={
      'off_axis_drop':(p,Packet(-r*1.6,r*.72,1.05,-.08,.6,0)),
      'orbit_asymmetric':(p,Packet(r*1.25,0,0,ov,.35,.08)),
      'orbit_symmetric_ablation':(replace(p,asymmetry=0.),Packet(r*1.25,0,0,ov,.35,0)),
      'free_boundary':(replace(p,boundary='free'),Packet(r*1.25,0,0,ov,.35,.08)),
      'fixed_boundary':(replace(p,boundary='fixed'),Packet(r*1.25,0,0,ov,.35,.08)),
      'no_well_control':(replace(p,well_depth=0.,gravity=0.,well_follow=0.),Packet(-4,1,.7,0,.2,0)),
      'zero_input_drift':(replace(p,well_depth=0.,gravity=0.,well_follow=0.,pressure=0.,compression=0.),Packet(0,0,0,0,0,0)),
    }
    results={}; summaries=[]
    for n,(pp,q) in cases.items(): results[n]=simulate(n,pp,q,out); summaries.append(results[n][1])
    # timestep and spatial convergence
    conv=[]
    q=Packet(r*1.25,0,0,ov,.35,.08)
    for dt in (1/120,1/240,1/480):
        pp=replace(p,dt=dt,duration=6.,sample_stride=max(1,round((1/30)/dt)))
        _,s=simulate(f'convergence_dt_{round(1/dt)}',pp,q,out); conv.append({'dt':dt,'final_distance':s['tail_mean_distance'],'max_strain':s['max_strain']})
    spatial=[]
    for gr in (6,8,10):
        pp=replace(p,grid_radius=gr,duration=6.)
        _,s=simulate(f'convergence_grid_{gr}',pp,q,out); spatial.append({'grid_radius':gr,'final_distance':s['tail_mean_distance'],'max_strain':s['max_strain']})
    plot(results,out); by={s['case']:s for s in summaries}
    dt_rel=abs(conv[-1]['final_distance']-conv[-2]['final_distance'])/max(1e-9,abs(conv[-1]['final_distance']))
    checks={
      'zero_input_drift_below_1e-10':by['zero_input_drift']['distance_max']<1e-10 and by['zero_input_drift']['max_strain']<1e-10,
      'asymmetric_shell_generates_more_spin':by['orbit_asymmetric']['max_abs_spin']>by['orbit_symmetric_ablation']['max_abs_spin']+1e-5,
      'well_changes_path':by['off_axis_drop']['distance_min']<by['off_axis_drop']['distance_max']-.2,
      'pressure_deforms_lattice':by['orbit_asymmetric']['max_strain']>1e-4,
      'timestep_convergence_under_8_percent':dt_rel<.08,
      'absorbing_boundary_reduces_reflection_proxy':by['orbit_asymmetric']['max_strain']<=by['free_boundary']['max_strain']*1.15,
    }
    payload={'model':'D-413 enhanced triangular Ground lattice + imposed well + bounded displacement shell','status':'YELLOW reduced model','integrator':'kick-drift-kick symplectic step with explicit damping work ledger','limitations':['Curvature well is imposed, not derived.','Bounded displacement is a collective shell coordinate, not a derived particle.','Energy balance is diagnostic, not a closed-system proof, because the imposed well-follow force can do work.','Finite tests do not establish gravity, charge, proton structure, or Mass Effect.'],'checks':checks,'all_checks_pass':all(checks.values()),'timestep_convergence':conv,'spatial_convergence':spatial,'cases':summaries}
    (out/'d413_summary.json').write_text(json.dumps(payload,indent=2)); return payload

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',default='results'); args=ap.parse_args(); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    payload=run_suite(out); print(json.dumps({'all_checks_pass':payload['all_checks_pass'],'checks':payload['checks']},indent=2)); raise SystemExit(0 if payload['all_checks_pass'] else 1)
if __name__=='__main__': main()
