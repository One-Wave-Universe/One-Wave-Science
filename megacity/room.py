"""Authoritative one-room world. The body does not own this state."""

from __future__ import annotations

WALL = "#"
FLOOR = "."
SWITCH = "S"
GOAL = "G"

MAP = (
    "#####",
    "#A.S#",
    "#...#",
    "#..G#",
    "#####",
)

DELTAS = {
    "north": (0, -1),
    "south": (0, 1),
    "east": (1, 0),
    "west": (-1, 0),
}


class Room:
    def __init__(self):
        self.w = len(MAP[0])
        self.h = len(MAP)
        self.switch_on = False
        self.avatar = None
        self.switch = None
        self.goal = None
        self.walls = set()
        for y, row in enumerate(MAP):
            for x, ch in enumerate(row):
                if ch == WALL:
                    self.walls.add((x, y))
                elif ch == "A":
                    self.avatar = [x, y]
                elif ch == SWITCH:
                    self.switch = (x, y)
                elif ch == GOAL:
                    self.goal = (x, y)
        if self.avatar is None or self.switch is None or self.goal is None:
            raise RuntimeError("room map is missing avatar, switch, or goal")

    def tile(self, x, y):
        if (x, y) in self.walls:
            return WALL
        if (x, y) == self.switch:
            return SWITCH
        if (x, y) == self.goal:
            return GOAL
        return FLOOR

    def blocked(self, x, y):
        return (x, y) in self.walls or not (0 <= x < self.w and 0 <= y < self.h)

    def available_actions(self):
        x, y = self.avatar
        actions = ["look", "wait"]
        for name, (dx, dy) in DELTAS.items():
            if not self.blocked(x + dx, y + dy):
                actions.append(name)
        if (x, y) == self.switch:
            actions.append("toggle")
        return actions

    def perceive(self):
        x, y = self.avatar
        neighbors = {}
        for name, (dx, dy) in DELTAS.items():
            nx, ny = x + dx, y + dy
            neighbors[name] = "wall" if self.blocked(nx, ny) else self.tile(nx, ny)
        return {
            "avatar": [x, y],
            "here": self.tile(x, y),
            "switch_on": self.switch_on,
            "switch_at": [self.switch[0], self.switch[1]],
            "goal_at": [self.goal[0], self.goal[1]],
            "on_switch": (x, y) == self.switch,
            "on_goal": (x, y) == self.goal,
            "goal_open": self.switch_on and (x, y) == self.goal,
            "neighbors": neighbors,
        }

    def act(self, action):
        before = self.perceive()
        legal = self.available_actions()
        if action not in legal:
            return {
                "accepted": False,
                "result": "rejected:" + str(action),
                "before": before,
                "after": self.perceive(),
            }
        x, y = self.avatar
        if action in DELTAS:
            dx, dy = DELTAS[action]
            self.avatar = [x + dx, y + dy]
            result = "moved:" + action
        elif action == "toggle":
            self.switch_on = not self.switch_on
            result = "switch:" + ("on" if self.switch_on else "off")
        elif action == "look":
            result = "looked"
        else:
            result = "waited"
        return {
            "accepted": True,
            "result": result,
            "before": before,
            "after": self.perceive(),
        }

    def to_dict(self):
        return {"avatar": list(self.avatar), "switch_on": self.switch_on}

    @classmethod
    def from_dict(cls, data):
        room = cls()
        room.avatar = list(data["avatar"])
        room.switch_on = bool(data["switch_on"])
        return room
