from __future__ import annotations
import importlib.util, json
from pathlib import Path

def _load(path: Path):
    spec=importlib.util.spec_from_file_location("parser_"+path.stem,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def registry_snapshot(root: Path):
    out=[]
    for p in sorted(root.glob("*.py")):
        if p.name.startswith("_"): continue
        try:
            m=_load(p); meta=getattr(m,"PLUGIN",None)
            if isinstance(meta,dict): out.append(meta)
        except Exception as e: out.append({"id":p.stem,"error":str(e)})
    return out
def get_parser(root: Path, parser_id: str):
    for p in root.glob("*.py"):
        if p.name.startswith("_"): continue
        m=_load(p)
        if getattr(m,"PLUGIN",{}).get("id")==parser_id: return m
    raise KeyError(parser_id)
