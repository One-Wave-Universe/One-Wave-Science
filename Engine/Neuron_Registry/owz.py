#!/usr/bin/env python3
"""Pack the sandbox as a .owz = zip + One-Wave manifest. Not a new codec."""
from __future__ import annotations

import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent

MANIFEST = {
    "format": "owz-1",
    "brick": "YELLOW",
    "what": "sandbox wave manipulator + registered cells",
    "not": [".git", "Nodes/ write", "clone", "new compression"],
    "seats": [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6],
    "nodes_ref": ["G-719", "G-722", "E-514"],
    "packed_utc": None,
}

INCLUDE = [
    "REGISTRY.json",
    "README.md",
    "wave_app.py",
    "wave_manipulator.py",
    "one-wave-manipulator.desktop",
    "install_linux_desktop.sh",
    "DESKTOP.md",
    "OWZ.md",
    "owz.py",
]


def pack(dest: Path | None = None) -> Path:
    dest = dest or (ROOT / "one-wave-manipulator.owz")
    man = dict(MANIFEST)
    man["packed_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("MANIFEST.json", json.dumps(man, indent=2))
        for name in INCLUDE:
            p = ROOT / name
            if p.is_file():
                z.write(p, name)
        for state in (ROOT / "cells").glob("*/STATE.json"):
            z.write(state, state.relative_to(ROOT).as_posix())
    return dest


def peek(path: Path) -> dict:
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        man = json.loads(z.read("MANIFEST.json"))
    return {
        "job": "owz_peek",
        "format": man.get("format"),
        "files": names,
        "has_git": any(n.startswith(".git") for n in names),
        "has_nodes_md": any(n.startswith("Nodes/") for n in names),
        "pass": man.get("format") == "owz-1" and not any(n.startswith(".git") for n in names),
        "honest": "Zip with a manifest. Open with unzip. Not a new algorithm.",
    }


if __name__ == "__main__":
    out = pack()
    print(json.dumps(peek(out), indent=2))
