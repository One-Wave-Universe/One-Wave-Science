"""Rooms: named places, each with their own chat/council and project
directory -- "a council chamber and a chatroom, with workbenches so AI
can build, see the code, suggest edits, and test it on side rooms"
(the user's own words).

A Room is just a Council (chat + patch_worker + project directory) with
a name -- everything already built (seats, ask, propose_change,
approve_and_apply, TestWorker) works unchanged inside a room. A World
holds many rooms. branch_room() makes a "side room": a fresh copy of a
parent room's files with a brand new, independent chat, so a seat can
try something risky there -- edit, run tests, break things -- without
touching the parent room's files or transcript at all. Nothing here
adds spatial coordinates, avatars, or physics; this is deliberately
just "named places with their own code and chat," the smallest real
slice of the bigger vision.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from council_chamber.models import CouncilChat
from council_chamber.orchestrator import Council
from council_chamber.workers.patch_worker import PatchWorker


class RoomAlreadyExistsError(ValueError):
    pass


class RoomNotFoundError(KeyError):
    pass


class Room:
    def __init__(self, name: str, project_dir: str | Path, council: Council | None = None):
        self.name = name
        self.project_dir = Path(project_dir)
        self.council = council or Council(CouncilChat(), PatchWorker(self.project_dir))


class World:
    def __init__(self):
        self.rooms: dict[str, Room] = {}

    def create_room(self, name: str, project_dir: str | Path, council: Council | None = None) -> Room:
        if name in self.rooms:
            raise RoomAlreadyExistsError(f"room {name!r} already exists")
        Path(project_dir).mkdir(parents=True, exist_ok=True)
        room = Room(name, project_dir, council=council)
        self.rooms[name] = room
        return room

    def get_room(self, name: str) -> Room:
        if name not in self.rooms:
            raise RoomNotFoundError(name)
        return self.rooms[name]

    def branch_room(self, parent_name: str, side_name: str) -> Room:
        """Make a "side room": a fresh copy of parent's project files
        under a sibling directory named after the side room, with a
        brand new chat (never the parent's transcript or open seats --
        a side room starts empty and whoever's testing there opens
        whatever seats they need). Nothing written in the side room
        touches the parent until someone re-applies a proven change
        there via the parent room's own propose_change/approve_and_apply."""
        if side_name in self.rooms:
            raise RoomAlreadyExistsError(f"room {side_name!r} already exists")
        parent = self.get_room(parent_name)
        side_dir = parent.project_dir.parent / side_name
        shutil.copytree(parent.project_dir, side_dir, dirs_exist_ok=True)
        room = Room(side_name, side_dir)
        self.rooms[side_name] = room
        return room

    def room_names(self) -> list[str]:
        return list(self.rooms)
