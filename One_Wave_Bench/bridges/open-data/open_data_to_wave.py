#!/usr/bin/env python3
"""Convert provenance-bearing measurement/metadata JSON into One-Wave wave-state JSON."""
import argparse, json, math
from pathlib import Path

REQUIRED_MAPPING = ('state_identity','coupling_rule','timing_relationship','propagation_behavior')

def norm(values):
    lo, hi = min(values), max(values)
    if hi == lo: return [0.0 for _ in values]
    return [2.0*(v-lo)/(hi-lo)-1.0 for v in values]

def transform(doc):
    mode=doc.get('mode')
    mapping=doc.get('mapping',{})
    missing=[k for k in REQUIRED_MAPPING if not mapping.get(k)]
    if missing: raise ValueError('missing mapping fields: '+', '.join(missing))
    provenance=doc.get('provenance',{})
    if not provenance.get('source') or not provenance.get('record_id'):
        raise ValueError('provenance.source and provenance.record_id are required')
    states=[]
    if mode=='measurement_series':
        samples=doc.get('samples',[])
        if not samples: raise ValueError('measurement_series requires samples')
        vals=[float(s['value']) for s in samples]
        amps=norm(vals)
        for i,(s,a) in enumerate(zip(samples,amps)):
            t=float(s.get('t',i)); x=float(s.get('x',0.0))
            dt=(t-float(samples[i-1].get('t',i-1))) if i else 0.0
            freq=(1.0/abs(dt)) if i and dt else 0.0
            states.append({'A':a,'f':freq,'phi':0.0,'x':x,'t':t,'m':{'raw_value':vals[i],'raw':s}})
        kind='source_measurement_wave'
        physical=True
    elif mode=='metadata_sequence':
        meta=doc.get('metadata',{})
        numeric=[(k,float(v)) for k,v in sorted(meta.items()) if isinstance(v,(int,float)) and not isinstance(v,bool)]
        if not numeric: raise ValueError('metadata_sequence requires numeric metadata fields')
        amps=norm([v for _,v in numeric])
        for i,((k,v),a) in enumerate(zip(numeric,amps)):
            prev=amps[i-1] if i else a
            delta=a-prev
            phi=math.atan2(delta,a if a else 1e-15)
            states.append({'A':a,'f':0.0,'phi':phi,'x':float(i),'t':float(i),'m':{'field':k,'raw_value':v}})
        kind='derived_metadata_wave'
        physical=False
    else:
        raise ValueError('mode must be measurement_series or metadata_sequence')
    return {'schema':'one-wave-wave-data-v1','representation_kind':kind,'source_physical_wave_or_series':physical,
            'provenance':provenance,'mapping':mapping,'states':states,
            'warning':None if physical else 'Derived analysis encoding of metadata; not a claim that the source metadata is a physical waveform.'}

def main():
    p=argparse.ArgumentParser(); p.add_argument('input'); p.add_argument('-o','--output')
    a=p.parse_args(); out=transform(json.loads(Path(a.input).read_text()))
    text=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if a.output: Path(a.output).write_text(text)
    else: print(text,end='')
if __name__=='__main__': main()
