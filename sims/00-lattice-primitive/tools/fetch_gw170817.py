#!/usr/bin/env python3
import json, hashlib, urllib.request
from pathlib import Path
import h5py

GPS_EVENT=1187008882.4
GPS_START=1187007040
RATE=4096
WINDOW_S=2.0
START=GPS_EVENT-WINDOW_S
N=int(WINDOW_S*RATE)
OUT=Path("sims/00-lattice-primitive/data")
OUT.mkdir(parents=True,exist_ok=True)

URLS={
"H1":"https://gwosc.org/eventapi/json/O1_O2-Preliminary/GW170817/v2/H-H1_LOSC_CLN_4_V1-1187007040-2048.hdf5",
"L1":"https://gwosc.org/eventapi/json/O1_O2-Preliminary/GW170817/v2/L-L1_LOSC_CLN_4_V1-1187007040-2048.hdf5",
"V1":"https://gwosc.org/eventapi/json/O1_O2-Preliminary/GW170817/v2/V-V1_LOSC_CLN_4_V1-1187007040-2048.hdf5",
}

def dataset_info(h):
    ds=h["strain/Strain"]
    meta=h["meta"]
    gps=float(meta["GPSstart"][()]) if "GPSstart" in meta else GPS_START
    dur=float(meta["Duration"][()]) if "Duration" in meta else len(ds)/RATE
    rate=len(ds)/dur
    return ds,gps,rate

payload={"schema":"gwosc-strain-window-v1","event":"GW170817","event_gps":GPS_EVENT,
"window":{"start_gps":START,"duration_s":WINDOW_S,"sample_rate_hz":RATE,"samples_per_detector":N},
"source":{"catalog":"O1_O2-Preliminary","version":"v2 cleaned","doi":"10.7935/K5B8566F","license":"CC BY 4.0"},
"detectors":{}}

for det,url in URLS.items():
    fn=OUT/f"{det}_GW170817_4k.hdf5"
    urllib.request.urlretrieve(url,fn)
    sha=hashlib.sha256(fn.read_bytes()).hexdigest()
    with h5py.File(fn,"r") as h:
        ds,gps0,rate=dataset_info(h)
        if abs(rate-RATE)>1e-6:
            raise RuntimeError(f"{det}: expected {RATE}, got {rate}")
        i0=round((START-gps0)*RATE)
        vals=ds[i0:i0+N]
        if len(vals)!=N:
            raise RuntimeError(f"{det}: short slice {len(vals)}")
        payload["detectors"][det]={
          "download_url":url,"source_sha256":sha,
          "source_gps_start":gps0,"values":[float(x) for x in vals]
        }
    fn.unlink()

out=OUT/"gw170817_v2_4khz_last2s.json"
out.write_text(json.dumps(payload,separators=(",",":")))
print(out, out.stat().st_size)
