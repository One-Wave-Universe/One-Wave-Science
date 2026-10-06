#!/usr/bin/env python3
"""Fresh bounded archive checks. No daemon or scientific interpretation."""
import argparse, concurrent.futures, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MISSIONS=['mars2020','mars_science_laboratory','mars_exploration_rover','voyager','cassini-huygens','juno','new_horizons','insight','maven','mars_reconnaissance_orbiter','orex']
def jobs():
    native=str(ROOT/'scripts/archive_metadata_query.py'); relay=str(ROOT/'scripts/science_archive_search.py')
    result=[]
    for mission in ['HST','JWST','TESS','GALEX','Kepler','K2']:
        args=['--inventory'] if mission in ('Kepler','K2') else ['--radius-deg','0.1']
        if mission=='GALEX':args+=['--coordinates','10.6847 41.269']
        result.append((mission,[sys.executable,native,'mast','--mission',mission]+args))
    for name,cat in [('NuSTAR','numaster'),('Chandra','chanmaster'),('Swift','swiftmastr'),('XMM','xmmmaster'),('Fermi','fermilasp'),('NICER','nicermastr'),('IXPE','ixmaster'),('XRISM','xrismmastr')]:
        result.append((name,[sys.executable,native,'heasarc','--catalog',cat,'--radius-deg','0.1']))
    for source in ['gaia-archive','eso','alma','desi','sdss','gwosc','gwosc-snapshot']:
        result.append((source,[sys.executable,relay,source]))
    for mission in MISSIONS:result.append(('pds-'+mission,[sys.executable,relay,'pds','--query',mission]))
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--only',nargs='+');a=p.parse_args()
    selected=[j for j in jobs() if not a.only or j[0] in a.only]
    if a.only and set(a.only)-{j[0] for j in selected}:p.error('Unknown route; use names in jobs()')
    a.output=a.output.resolve();a.output.mkdir(parents=True,exist_ok=True)
    def run(job):
        name,argv=job;dest=a.output/name;dest.mkdir(exist_ok=True)
        result={'route':name,'argv':argv,'cwd':str(ROOT),'timestamp':datetime.now(timezone.utc).isoformat()}
        try:
            process=subprocess.run(argv+['--output',str(dest)],cwd=ROOT,capture_output=True,text=True,timeout=90)
            (dest/'execution.log').write_text(process.stdout+'\n'+process.stderr)
            result.update(exit_code=process.returncode,receipt=json.loads((dest/'receipt.json').read_text()))
        except Exception as e:result.update(exit_code=1,error=str(e))
        print(name,result['exit_code'],flush=True);return result
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(run,selected))
    summary={'schema':'one-wave-astronomy-health-v1','repo_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'routes':results}
    (a.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return int(any(x['exit_code'] for x in results))
if __name__=='__main__':raise SystemExit(main())
