"""Opt-in smooth Mirror experiment for G-760; never changes legacy E4.
Requires numpy and scipy. All energies are dimensionless; no mass calibration.
"""
from dataclasses import asdict
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from e4_seven_cell import Coeff, State, dipole, e4

def energy(x, c, mu, m):
    """13 physical coordinates: seven positive amplitudes, six phases; pc=0."""
    state = State(a=list(x[:7]), phi=[0.0] + list(x[7:]))
    rec = e4(state, c)
    C, S, _ = dipole(state.a[1:])
    mirror = c.aM*S*S + mu*(C*C+S*S-m*m)**2
    # Sum directly: subtracting singular legacy M causes cancellation near C=S=0.
    return rec["K"] + rec["E"] + rec["T"] + rec["x"] + mirror

def reduced(c, mu, m):
    k = (c.bK+c.bT)/3.0
    r2 = max(0.0, m*m-k/(2*mu))
    return {"k": k, "mu_critical": k/(2*m*m),
            "C_abs": math.sqrt(r2), "origin_C_curvature": 2*k-4*mu*m*m}

def finite_gradient(f, x, h=1e-5):
    eye = np.eye(len(x))*h
    return np.array([(f(x+d)-f(x-d))/(2*h) for d in eye])

def finite_hessian(f, x, h=1e-4):
    eye = np.eye(len(x))*h
    H = np.zeros((len(x),len(x)))
    f0 = f(x)
    for i, d in enumerate(eye):
        H[i,i] = (f(x+d)-2*f0+f(x-d))/(h*h)
        for j in range(i):
            e = eye[j]
            H[i,j] = H[j,i] = (f(x+d+e)-f(x+d-e)-f(x-d+e)+f(x-d-e))/(4*h*h)
    return H

def solve(c, mu, m, sign):
    if mu <= 0 or m <= 0:
        raise ValueError("mu and m must be positive")
    x = np.zeros(13)
    x[:7] = 1
    # Seed on both sides of the predicted bifurcation, even below threshold.
    radius = max(0.15, reduced(c,mu,m)["C_abs"])
    for k in range(6):
        x[k+1] += sign*radius/3*math.cos(2*math.pi*k/6)
    f = lambda v: energy(v,c,mu,m)
    opt = minimize(f,x,method="L-BFGS-B",
                   bounds=[(1e-4,None)]*7+[(None,None)]*6,
                   options={"ftol":1e-14,"gtol":1e-9,"maxiter":2000,"maxls":50})
    ev = np.linalg.eigvalsh(finite_hessian(f,opt.x))
    ev2 = np.linalg.eigvalsh(finite_hessian(f,opt.x,h=5e-5))
    C,S,_ = dipole(opt.x[1:7])
    grad = float(np.linalg.norm(finite_gradient(f,opt.x),ord=np.inf))
    interior = bool(np.min(opt.x[:7])>1e-3)
    stable = bool(opt.success and interior and grad<1e-5 and min(ev[0],ev2[0])>1e-5)
    return {"success":bool(opt.success),"message":str(opt.message),
            "x":opt.x.tolist(),"C":C,"S":S,"energy":float(opt.fun),
            "gradient_inf":grad,"interior":interior,
            "eigenvalues_h1e4":ev.tolist(),"eigenvalues_h5e5":ev2.tolist(),
            "stable_physical_slice":stable}

def scan():
    rows=[]
    for bK in (0.1,0.4,1.0):
        for bT in (0.05,0.2,0.8):
            for chi in (0.0,0.05):
                c=Coeff(bK=bK,bT=bT,chi=chi)
                crit=reduced(c,1.0,1.0)["mu_critical"]
                for ratio in (0.5,0.9,1.1,2.0,5.0):
                    mu=ratio*crit
                    wells=[solve(c,mu,1.0,s) for s in (-1,1)]
                    survive=bool(all(w["stable_physical_slice"] for w in wells)
                                 and wells[0]["C"] < -1e-3 and wells[1]["C"]>1e-3)
                    rows.append({"coeff":asdict(c),"mu":mu,"m":1.0,"mu_over_critical":ratio,
                                 "reduced":reduced(c,mu,1.0),"wells":wells,
                                 "two_basins_survive":survive})
    return {"schema":"one-wave.mirror-basin-scan.v1",
            "model":"G-757 K/E/T/x with opt-in G-760 smooth quartic M",
            "slice":"Gamma=0, pc=0; seven amplitudes plus six relative phases",
            "units":"dimensionless","numpy":np.__version__,
            "rows":rows,"cases":len(rows),
            "surviving_pairs":sum(r["two_basins_survive"] for r in rows),
            "limitations":["Not a proof across circulation sectors or phase-wrap boundaries.",
                           "Finite-difference Hessians are numerical, not rigorous certificates.",
                           "No NEB barrier, carry metric W, physical mass, or full G-762 hold established."]}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    rec=scan()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(rec,indent=2)+"\n")
    print(json.dumps({"cases":rec["cases"],"surviving_pairs":rec["surviving_pairs"]}))
