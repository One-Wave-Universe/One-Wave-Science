#!/usr/bin/env python3
"""G-767 spectral lattice phase-map scaffold.

Uses only stdlib. CSV columns: scale[,width,uncertainty,label].
Labels are metadata and never enter the statistic.
"""
import argparse,csv,math,random,statistics

def read(path):
    out=[]
    with open(path,newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):
            x=float(r["scale"])
            if x>0:
                out.append((x,float(r["width"]) if r.get("width") else None))
    return out

def phases(xs,x0):
    return [(math.log2(x/x0)%1.0) for x,_ in xs]

def coherence(ph):
    if not ph:return 0.0
    z=sum(complex(math.cos(2*math.pi*p),math.sin(2*math.pi*p)) for p in ph)
    return abs(z)/len(ph)

def null_test(xs,x0,trials,seed):
    rng=random.Random(seed); real=coherence(phases(xs,x0))
    logs=[math.log2(x) for x,_ in xs]; lo,hi=min(logs),max(logs)
    null=[]
    for _ in range(trials):
        fake=[(2**rng.uniform(lo,hi),None) for _ in xs]
        null.append(coherence(phases(fake,x0)))
    p=(1+sum(v>=real for v in null))/(trials+1)
    return real,statistics.mean(null),p

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--x0",type=float,required=True,help="predeclared positive reference scale")
    ap.add_argument("--trials",type=int,default=10000)
    ap.add_argument("--seed",type=int,default=767)
    a=ap.parse_args()
    if a.x0<=0: raise SystemExit("x0 must be positive")
    xs=read(a.csv)
    if len(xs)<3: raise SystemExit("need >=3 positive scales")
    real,mean,p=null_test(xs,a.x0,a.trials,a.seed)
    print(f"N={len(xs)} x0={a.x0:g} coherence={real:.8f} null_mean={mean:.8f} permutation_p={p:.8g}")
    print("STATUS=EXPLORATORY_ONLY")
if __name__=="__main__": main()
