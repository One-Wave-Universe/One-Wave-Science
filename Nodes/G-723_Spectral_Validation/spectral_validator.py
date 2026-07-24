#!/usr/bin/env python3
"""Reference spectral receipts for G-723.

Uses exact polynomial coefficients and numerical roots. This is an audit example,
not an android safety threshold.
"""
from pathlib import Path
import csv,json,math
import numpy as np
OUT=Path(__file__).resolve().parent

def audit(name,coeffs):
    roots=np.roots(coeffs)
    mods=np.abs(roots)
    mahler=abs(coeffs[0])*float(np.prod(np.maximum(1.0,mods)))
    return {
      'name':name,'coefficients':coeffs,'roots':[{'real':float(z.real),'imag':float(z.imag),'modulus':float(abs(z)),'angle':float(np.angle(z))} for z in roots],
      'spectral_radius':float(max(mods)),'mahler_measure':mahler,
      'contracting_count':int(np.sum(mods<1-1e-7)),'unit_circle_count':int(np.sum(np.abs(mods-1)<=1e-7)),'expanding_count':int(np.sum(mods>1+1e-7))
    }

cases=[
 audit('fibonacci_pisot',[1,-1,-1]),
 audit('plastic_pisot',[1,0,-1,-1]),
 audit('tribonacci_pisot',[1,-1,-1,-1]),
 audit('lehmer_salem_reference',[1,1,0,-1,-1,-1,-1,-1,0,1,1])
]
(OUT/'reference_validation.json').write_text(json.dumps({'cases':cases,'scope':'Algebraic reference spectra only; Lehmer is not a motor threshold.'},indent=2),encoding='utf-8')
rows=[]
for c in cases:
  for i,r in enumerate(c['roots']): rows.append({'case':c['name'],'root_index':i,**r})
with (OUT/'root_spectra.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print(json.dumps({'cases':[{'name':c['name'],'spectral_radius':c['spectral_radius'],'mahler_measure':c['mahler_measure'],'counts':[c['contracting_count'],c['unit_circle_count'],c['expanding_count']]} for c in cases]},indent=2))
