"""Looper body. Chooses only from the room's switches."""

from __future__ import annotations


class LooperBody:
    def __init__(self, goal="stand on the mark with the switch on"):
        self.goal = goal
        self.path = ["toggle the switch", "walk to the mark", "hold"]
        self.last_action = None
        self.last_result = None
        self.memory = []
        self.done = False

    def decide(self, perception, choices):
        if perception["goal_open"]:
            self.done = True
            self.path = ["hold"]
            action = "wait" if "wait" in choices else choices[0]
            return action, "on the open mark; hold", list(self.path)
        if perception["on_switch"] and (not perception["switch_on"]) and "toggle" in choices:
            self.done = False
            self.path = ["toggle the switch", "walk to the mark", "hold"]
            return "toggle", "switch is underfoot and off", list(self.path)
        self.done = False
        if not perception["switch_on"]:
            self.path = ["reach the switch", "toggle the switch", "walk to the mark", "hold"]
            target = perception["switch_at"]
            why = "switch is off; walk to it"
        else:
            self.path = ["walk to the mark", "hold"]
            target = perception["goal_at"]
            why = "switch is on; walk to the mark"
        return _toward(perception["avatar"], target, choices), why, list(self.path)

    def to_dict(self):
        return {
            "goal": self.goal,
            "path": list(self.path),
            "last_action": self.last_action,
            "last_result": self.last_result,
            "memory": list(self.memory),
            "done": self.done,
        }

    @classmethod
    def from_dict(cls, data):
        body = cls(goal=data["goal"])
        body.path = list(data["path"])
        body.last_action = data["last_action"]
        body.last_result = data["last_result"]
        body.memory = list(data["memory"])
        body.done = bool(data["done"])
        return body


def _toward(origin, target, choices):
    ox, oy = origin
    tx, ty = target
    prefer = []
    if tx > ox:
        prefer.append("east")
    elif tx < ox:
        prefer.append("west")
    if ty > oy:
        prefer.append("south")
    elif ty < oy:
        prefer.append("north")
    for name in prefer:
        if name in choices:
            return name
    for name in ("look", "wait"):
        if name in choices:
            return name
    return choices[0]
