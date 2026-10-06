"""Field, Void, and the parser between them. One loop. Save and reload."""

from __future__ import annotations

import json

from .body import LooperBody
from .room import Room

PACKET_KEYS = (
    "what_is_happening_now",
    "what_changed_since_last_loop",
    "active_goal",
    "current_path_or_plan",
    "last_action",
    "last_action_result",
    "relevant_memory_or_reference",
    "conflict_or_drift_detected",
    "available_choices",
    "chosen_next_action",
    "why_this_action",
    "new_state_after_action",
)


class Looper:
    def __init__(self, room=None, body=None):
        self.room = room if room is not None else Room()
        self.body = body if body is not None else LooperBody()
        self.step_index = 0

    def step(self, action=None):
        before = self.room.perceive()
        choices = self.room.available_actions()
        changed = "first loop" if self.body.last_action is None else "after " + str(self.body.last_action)
        conflict = "none"
        if self.body.last_result and str(self.body.last_result).startswith("rejected"):
            conflict = "last action was rejected by the room"
        memory = "no prior loop"
        if self.body.memory:
            memory = self.body.memory[-1]["why_this_action"]
        field = {
            "what_is_happening_now": "at %s on %s; switch %s" % (
                before["avatar"], before["here"], "on" if before["switch_on"] else "off"
            ),
            "what_changed_since_last_loop": changed,
            "perception": before,
            "available_choices": list(choices),
        }
        void = {
            "active_goal": self.body.goal,
            "current_path_or_plan": list(self.body.path),
            "last_action": self.body.last_action,
            "last_action_result": self.body.last_result,
            "relevant_memory_or_reference": memory,
            "conflict_or_drift_detected": conflict,
        }
        if action is None:
            action, why, plan = self.body.decide(before, choices)
        else:
            plan = list(self.body.path)
            if action in choices:
                why = "caller selected a bounded switch"
            else:
                why = "caller asked for a switch the room does not offer"
        if action not in choices:
            self.body.path = plan
        outcome = self.room.act(action)
        after = outcome["after"]
        self.body.last_action = action
        self.body.last_result = outcome["result"]
        if after["goal_open"]:
            self.body.done = True
            self.body.path = ["hold"]
        packet = {
            "what_is_happening_now": field["what_is_happening_now"],
            "what_changed_since_last_loop": field["what_changed_since_last_loop"],
            "active_goal": void["active_goal"],
            "current_path_or_plan": plan,
            "last_action": void["last_action"],
            "last_action_result": void["last_action_result"],
            "relevant_memory_or_reference": void["relevant_memory_or_reference"],
            "conflict_or_drift_detected": void["conflict_or_drift_detected"],
            "available_choices": field["available_choices"],
            "chosen_next_action": action,
            "why_this_action": why,
            "new_state_after_action": {
                "avatar": after["avatar"],
                "switch_on": after["switch_on"],
                "on_goal": after["on_goal"],
                "goal_open": after["goal_open"],
                "result": outcome["result"],
                "accepted": outcome["accepted"],
            },
            "step_index": self.step_index,
            "field": field,
            "void": void,
        }
        missing = [key for key in PACKET_KEYS if key not in packet]
        if missing:
            raise RuntimeError("packet missing %s" % missing)
        self.body.memory.append({key: packet[key] for key in PACKET_KEYS})
        self.step_index += 1
        return packet

    def run_until_done(self, limit=16):
        packets = []
        for _ in range(limit):
            packets.append(self.step())
            if self.body.done and packets[-1]["new_state_after_action"]["goal_open"]:
                break
        return packets

    def save(self, path):
        payload = {
            "step_index": self.step_index,
            "room": self.room.to_dict(),
            "body": self.body.to_dict(),
        }
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
        return payload

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8") as handle:
            payload = json.load(handle)
        loop = cls(room=Room.from_dict(payload["room"]), body=LooperBody.from_dict(payload["body"]))
        loop.step_index = payload["step_index"]
        return loop
