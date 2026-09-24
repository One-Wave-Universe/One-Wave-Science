from __future__ import annotations
import json
from pathlib import Path
from provider_registry import get_provider
from parser_registry import get_parser
from m4_body import load_body, save_body

def run_once(root: Path, request: dict, config: dict):
    field=get_provider(root/"providers",config["field_provider"])
    void=get_provider(root/"providers",config["void_provider"])
    parser=get_parser(root/"parsers",config["parser"])
    m4=load_body()

    inp=parser.parse_input(request.get("input",""))
    stimulus={
        "magnitude": float(request.get("magnitude",0.5)),
        "novelty": float(request.get("novelty",0.0)),
        "conflict": float(request.get("conflict",0.0)),
    }
    m4.ingest(stimulus)

    state={
        "goal":request.get("goal",""),
        "reference":request.get("reference",""),
        "world":{"input":inp},
        "protected":request.get("protected",[]),
        "m4":m4.snapshot(),
    }

    field_seen=field.call("FIELD_PERCEIVE",state)
    state["field"]=field_seen

    void_seen=void.call("VOID_ADMIN",state)
    state["void"]=void_seen

    field_signal={
        "drive": float(field_seen.get("drive",0.65)),
        "friction": float(field_seen.get("friction",0.0)),
    }
    void_signal={
        "brake": float(void_seen.get("brake",1.0 if str(void_seen.get("decision","HOLD")).upper() in ("HOLD","ESCALATE") else 0.0)),
        "support": float(void_seen.get("support",0.65 if str(void_seen.get("decision","HOLD")).upper()=="ALLOW" else 0.0)),
        "contradiction": float(void_seen.get("contradiction",0.0)),
    }

    gate=m4.integrate(field_signal,void_signal)
    state["m4_gate"]=gate
    state["m4"]=m4.snapshot()

    if not gate["action_open"]:
        result={"ok":False,"evidence_strength":0.0,"expected_match":0.0,"reason":"M4 action gate held"}
        reinjection=m4.reinject(result)
        save_body(m4)
        state["m4_reinjection"]=reinjection
        state["m4"]=m4.snapshot()
        return {
            "ok":True,
            "state":state,
            "output":void_seen.get("outward_instruction") or void_seen.get("reason") or "M4 HOLD",
            "acted":False,
        }

    field_out=field.call("FIELD_ACT",state)
    state["action"]=field_out.get("action",{})
    state["output"]=field_out.get("speech","")

    result={
        "ok":True,
        "sandbox":bool(config.get("sandbox",True)),
        "action":state["action"],
        "evidence_strength":1.0,
        "expected_match":1.0,
    }
    state["result"]=result

    void_commit=void.call("VOID_COMMIT",state)
    state["void_commit"]=void_commit
    if not bool(void_commit.get("commit",False)):
        result["ok"]=False
        result["expected_match"]=0.0

    reinjection=m4.reinject(result)
    save_body(m4)
    state["m4_reinjection"]=reinjection
    state["m4"]=m4.snapshot()

    return {
        "ok":True,
        "state":state,
        "output":state["output"],
        "acted":True,
        "committed":reinjection["committed"],
    }
