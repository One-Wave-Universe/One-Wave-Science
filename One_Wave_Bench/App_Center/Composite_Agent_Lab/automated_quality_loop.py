#!/usr/bin/env python3
"""Reference -> build -> evidence -> review -> quality -> repair loop."""
from __future__ import annotations
from dataclasses import asdict
from typing import Any, Callable
from quality_gate import evaluate

class AutomatedQualityLoop:
    def __init__(self, builder: Callable, reviewer: Callable, validator: Callable, max_cycles: int = 6, threshold: float = 0.95):
        self.builder=builder; self.reviewer=reviewer; self.validator=validator
        self.max_cycles=max_cycles; self.threshold=threshold

    def run(self, task: dict[str,Any]) -> dict[str,Any]:
        state={"task":task,"cycle":0,"repairs":[],"candidate":None,"validation":None,"review":None}
        for cycle in range(1,self.max_cycles+1):
            state["cycle"]=cycle
            candidate=self.builder(task,state["repairs"],state)
            validation=self.validator(task,candidate,state)
            review=self.reviewer(task,candidate,validation,state)
            payload={
                "references":candidate.get("references",[]),
                "claims":candidate.get("claims",[]),
                "requirements":validation.get("requirements",[]),
                "tests":validation.get("tests",[]),
                "void_review":review,
                "usable":validation.get("usable",False),
                "drift":validation.get("drift",{}),
            }
            report=evaluate(payload,self.threshold)
            state.update({"candidate":candidate,"validation":validation,"review":review,"quality":asdict(report)})
            if report.accepted:
                return {"ok":True,"status":"ACCEPTED","state":state}
            state["repairs"]=report.repair_tasks
        return {"ok":False,"status":"HARD_STOP","state":state}
