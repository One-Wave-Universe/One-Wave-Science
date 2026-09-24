from __future__ import annotations
import json, tempfile
from pathlib import Path
from provider_registry import get_provider
from parser_registry import get_parser

def run_once(root: Path, request: dict, config: dict):
    field=get_provider(root/"providers",config["field_provider"])
    void=get_provider(root/"providers",config["void_provider"])
    parser=get_parser(root/"parsers",config["parser"])
    inp=parser.parse_input(request.get("input",""))
    state={"goal":request.get("goal",""),"reference":request.get("reference",""),"world":{"input":inp},"protected":request.get("protected",[])}
    field_seen=field.call("FIELD_PERCEIVE",state)
    state["field"]=field_seen
    void_seen=void.call("VOID_ADMIN",state)
    state["void"]=void_seen
    if str(void_seen.get("decision","HOLD")).upper() in ("HOLD","ESCALATE"):
        return {"ok":True,"state":state,"output":void_seen.get("outward_instruction") or void_seen.get("reason","HOLD"),"acted":False}
    field_out=field.call("FIELD_ACT",state)
    state["action"]=field_out.get("action",{})
    state["output"]=field_out.get("speech","")
    result={"ok":True,"sandbox":bool(config.get("sandbox",True)),"action":state["action"]}
    state["result"]=result
    state["void_commit"]=void.call("VOID_COMMIT",state)
    return {"ok":True,"state":state,"output":state["output"],"acted":True}
