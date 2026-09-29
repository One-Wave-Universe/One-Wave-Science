#!/usr/bin/env python3
"""Desktop wave manipulator + logic-web map.

Sandbox only. Writes cell STATE only. Nodes/ stays OWATCH canon.
The UI is drawn in code; there are no generated/static art assets.
"""
from __future__ import annotations

import json
import math
import tkinter as tk
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CELLS = ROOT / "cells"
LINKAGE = ROOT / "LINKAGE.json"
CALIBRATION = ROOT / "CALIBRATION.json"
W, H, CX, CY, R = 1040, 720, 300, 305, 205

BG = "#10131a"
PANEL = "#171c26"
TEXT = "#f2f5fa"
MUTED = "#a9b4c6"
EDGE = "#52637c"
EDGE_HOT = "#f7b84b"

COLORS = {
    "canon": "#1469ff",
    "science": "#00c6ff",
    "watcher": "#ff8a00",
    "holder": "#ff334e",
    "sandbox": "#ffd21f",
    "runtime": "#8f5cff",
    "simulation": "#19d36b",
    "evidence": "#ff4fc3",
    "cell_f": "#ffb347",
    "cell_b": "#58d68d",
    "pivot": "#66a3ff",
    "closure": "#ef6c6c",
}


def label(p: int) -> int:
    r = p % 12
    return r - 12 if r > 6 else r


def seat_xy(seat: int):
    ang = -math.pi / 2 + seat * (math.pi / 6)
    return CX + R * math.cos(ang), CY + R * math.sin(ang)


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("One-Wave Neuron Sandbox")
        self.geometry("1040x780")
        self.minsize(900, 680)
        self.configure(bg=BG)
        self.f = self.b = 0
        self.running = False
        self.view = "wave"

        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=14, pady=(12, 6))
        tk.Label(
            header,
            text="NEURON REGISTRY SANDBOX",
            fg=TEXT,
            bg=BG,
            font=("TkDefaultFont", 15, "bold"),
        ).pack(side="left")
        tk.Label(
            header,
            text="  OWATCH canon stays read-only",
            fg=COLORS["science"],
            bg=BG,
        ).pack(side="left")

        nav = tk.Frame(header, bg=BG)
        nav.pack(side="right")
        self.wave_btn = tk.Button(nav, text="Wave", command=lambda: self.set_view("wave"))
        self.map_btn = tk.Button(nav, text="Logic Web", command=lambda: self.set_view("map"))
        self.wave_btn.pack(side="left", padx=4)
        self.map_btn.pack(side="left", padx=4)

        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=12, pady=6)

        bar = tk.Frame(self, bg=PANEL, padx=10, pady=8)
        bar.pack(fill="x", padx=12, pady=(0, 12))
        tk.Button(bar, text="Go", command=self.go, width=8).pack(side="left", padx=(0, 6))
        tk.Button(bar, text="Hold", command=self.hold, width=8).pack(side="left", padx=6)
        tk.Button(bar, text="Reset", command=self.reset, width=8).pack(side="left", padx=6)
        self.msg = tk.Label(
            bar,
            text="0 pivot  ±5 walks  6 half-cycle",
            fg=TEXT,
            bg=PANEL,
            anchor="w",
        )
        self.msg.pack(side="left", padx=14, fill="x", expand=True)

        self.canvas.bind("<Configure>", lambda _e: self.draw())
        self.draw()

    def set_view(self, view: str):
        self.view = view
        self.draw()

    def go(self):
        self.running = True
        self.tick()

    def hold(self):
        self.running = False
        self.draw()

    def reset(self):
        self.running = False
        self.f = self.b = 0
        self.write_cells()
        self.draw()

    def tick(self):
        if not self.running:
            return
        self.f += 5
        self.b -= 5
        self.write_cells()
        self.draw()
        self.after(400, self.tick)

    def write_cells(self):
        lf, lb = label(self.f), label(self.b)
        for name, seat, step, choice in (
            ("Nf", lf, 5, 1 if lf not in (0, 6) else 0),
            ("Nb", lb, -5, -1 if lb not in (0, 6) else 0),
            ("N0", 0, 0, 0),
            ("N6", 6, 0, 0),
        ):
            p = CELLS / name / "STATE.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            old = load_json(p, {})
            old.update({"id": name, "seat": seat, "step": step, "choice": choice})
            p.write_text(json.dumps(old, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def draw(self):
        if self.view == "map":
            self.draw_logic_web()
        else:
            self.draw_wave()

    def draw_wave(self):
        c = self.canvas
        c.delete("all")
        cw = max(900, c.winfo_width())
        ch = max(560, c.winfo_height())

        # adaptive wave center
        global CX, CY
        CX, CY = int(cw * 0.33), int(ch * 0.48)

        c.create_text(
            22, 18, anchor="nw", text="WAVE / WALK VIEW",
            fill=TEXT, font=("TkDefaultFont", 14, "bold"),
        )
        c.create_text(
            22, 44, anchor="nw",
            text="Two mirrored rotations. Meet at 6 = begin-close. Finish at 0 = closed.",
            fill=MUTED,
        )

        c.create_oval(CX - R, CY - R, CX + R, CY + R, outline="#61718a", width=3)
        c.create_oval(CX - R + 18, CY - R + 18, CX + R - 18, CY + R - 18, outline="#2a3548")

        for s in list(range(-5, 6)) + [6]:
            x, y = seat_xy(s)
            col = COLORS["pivot"] if s == 0 else COLORS["closure"] if s == 6 else MUTED
            c.create_oval(x - 15, y - 15, x + 15, y + 15, fill=PANEL, outline=col, width=2)
            c.create_text(x, y, text=str(s), fill=col, font=("TkDefaultFont", 10, "bold"))

        lf, lb = label(self.f), label(self.b)
        xf, yf = seat_xy(lf)
        xb, yb = seat_xy(lb)
        c.create_oval(xf - 10, yf - 10, xf + 10, yf + 10, fill=COLORS["cell_f"], outline=TEXT)
        c.create_oval(xb - 10, yb - 10, xb + 10, yb + 10, fill=COLORS["cell_b"], outline=TEXT)

        self.draw_cell_card(c, int(cw * .65), 120, "N0", COLORS["pivot"], "pivot / balance", 0)
        self.draw_cell_card(c, int(cw * .65), 220, "N6", COLORS["closure"], "half-cycle / closure begins", 0)
        self.draw_cell_card(c, int(cw * .65), 320, "Nf", COLORS["cell_f"], "+5 forward walk", 1 if lf not in (0, 6) else 0)
        self.draw_cell_card(c, int(cw * .65), 420, "Nb", COLORS["cell_b"], "−5 back walk", -1 if lb not in (0, 6) else 0)

        meet = lf == 6 and lb == 6
        home = lf == 0 and lb == 0
        self.msg.config(text=f"fwd {lf}  back {lb}  |  6 begin-close={meet}  0 closed={home}")

    def draw_cell_card(self, c, x, y, name, color, role, choice):
        c.create_rectangle(x, y, x + 280, y + 72, fill=PANEL, outline=color, width=2)
        c.create_rectangle(x, y, x + 12, y + 72, fill=color, outline=color)
        c.create_text(x + 26, y + 18, anchor="w", text=name, fill=TEXT, font=("TkDefaultFont", 12, "bold"))
        c.create_text(x + 26, y + 40, anchor="w", text=role, fill=MUTED)
        c.create_text(x + 245, y + 36, text=f"choice {choice:+d}", fill=color, font=("TkDefaultFont", 10, "bold"))

    def draw_logic_web(self):
        c = self.canvas
        c.delete("all")
        cw = max(900, c.winfo_width())
        ch = max(560, c.winfo_height())

        c.create_text(
            22, 18, anchor="nw", text="LOGIC WEB / LATTICE MAP",
            fill=TEXT, font=("TkDefaultFont", 14, "bold"),
        )
        c.create_text(
            22, 44, anchor="nw",
            text="Canon → reference → sandbox linkage → runtime state. Path pressure is navigation, not truth.",
            fill=MUTED,
        )

        # Canon wall / source side
        wall_x = int(cw * .34)
        c.create_rectangle(22, 82, wall_x - 18, ch - 36, fill="#101c32", outline=COLORS["canon"], width=3)
        c.create_text(42, 98, anchor="nw", text="OWATCH CANON", fill=COLORS["science"], font=("TkDefaultFont", 13, "bold"))
        c.create_text(42, 124, anchor="nw", text="Nodes/  •  source markdown authoritative", fill=TEXT)

        canon_nodes = [
            ("G-719", "network / analogy", COLORS["science"]),
            ("A-111", "neighbor-average linkage", COLORS["science"]),
            ("G-722", "local {-1,0,+1} choice", COLORS["science"]),
        ]
        yy = 170
        for nid, role, col in canon_nodes:
            self.draw_folder(c, 50, yy, 210, 62, nid, role, col, "canon")
            yy += 88

        c.create_text(
            46, ch - 96, anchor="nw",
            text="HARD WALL\nSandbox may read references.\nSandbox does not write Nodes/.",
            fill="#ff8b98", font=("TkDefaultFont", 10, "bold"),
        )

        # separator / wall
        c.create_line(wall_x, 80, wall_x, ch - 32, fill=COLORS["holder"], width=5, dash=(10, 6))
        c.create_text(wall_x + 8, 94, anchor="nw", text="REFERENCE GATE", fill=COLORS["holder"], font=("TkDefaultFont", 10, "bold"))

        # Runtime / sandbox side positions
        x0 = wall_x + 70
        x1 = int(cw * .63)
        x2 = int(cw * .80)

        nodes = {
            "registry": (x0, 150, "REGISTRY.json", "who exists", COLORS["sandbox"], "sandbox"),
            "linkage": (x1, 130, "LINKAGE.json", "who connects to whom", COLORS["watcher"], "watcher"),
            "hysteresis": (x1, 300, "hysteresis.py", "q path = memory", COLORS["runtime"], "runtime"),
            "wave": (x0, 360, "wave_manipulator", "two opposing walks", COLORS["simulation"], "simulation"),
            "app": (x2, 250, "wave_app.py", "Go / Hold / Reset", COLORS["holder"], "holder"),
            "cells": (x2, 430, "cells/*/STATE.json", "meter / runtime state", COLORS["evidence"], "runtime"),
        }

        for _, (x, y, title, role, col, kind) in nodes.items():
            self.draw_folder(c, x, y, 190, 70, title, role, col, kind)

        # canonical reference arrows crossing the wall
        self.draw_edge(c, 260, 200, x0, 182, COLORS["canon"], "reference", 3)
        self.draw_edge(c, 260, 288, x1, 162, COLORS["canon"], "A-111 link rule", 3)
        self.draw_edge(c, 260, 376, x0, 392, COLORS["canon"], "choice law", 3)

        # runtime graph edges
        self.draw_edge(c, x0 + 190, 185, x1, 165, EDGE_HOT, "NODE→LINKAGE", 4)
        self.draw_edge(c, x0 + 95, 220, x0 + 95, 360, EDGE, "walk", 2)
        self.draw_edge(c, x0 + 190, 395, x1, 335, COLORS["simulation"], "choice", 3)
        self.draw_edge(c, x1 + 190, 335, x2, 465, COLORS["runtime"], "q / pressure", 4)
        self.draw_edge(c, x1 + 190, 165, x2, 465, COLORS["watcher"], "neighbors", 3)
        self.draw_edge(c, x2 + 95, 320, x2 + 95, 430, COLORS["holder"], "UI step", 3)

        # miniature registered cell lattice
        mini_cx, mini_cy = x1 + 95, ch - 95
        c.create_text(mini_cx, mini_cy - 72, text="REGISTERED CELLS", fill=TEXT, font=("TkDefaultFont", 10, "bold"))
        pts = {
            "N0": (mini_cx - 72, mini_cy),
            "N6": (mini_cx + 72, mini_cy),
            "Nf": (mini_cx, mini_cy - 36),
            "Nb": (mini_cx, mini_cy + 36),
        }
        links = load_json(LINKAGE, {}).get("links", [])
        for edge in links:
            a, b = edge.get("a"), edge.get("b")
            if a in pts and b in pts:
                width = 4 if float(edge.get("weight", 1)) >= 1 else 2
                c.create_line(*pts[a], *pts[b], fill=EDGE_HOT, width=width)
        cell_cols = {"N0": COLORS["pivot"], "N6": COLORS["closure"], "Nf": COLORS["cell_f"], "Nb": COLORS["cell_b"]}
        for nid, (x, y) in pts.items():
            c.create_oval(x - 18, y - 18, x + 18, y + 18, fill=PANEL, outline=cell_cols[nid], width=3)
            c.create_text(x, y, text=nid, fill=TEXT, font=("TkDefaultFont", 9, "bold"))

        self.draw_legend(c, 30, ch - 26)
        self.msg.config(text="Logic Web: OWATCH canon is blue/cyan • sandbox yellow • watchers orange • runtime purple/magenta")

    def draw_folder(self, c, x, y, w, h, title, role, color, kind):
        # folder geometry with tab; variants get distinct badge marks
        tab_w = min(78, int(w * .4))
        pts = [
            x, y + 14,
            x + tab_w, y + 14,
            x + tab_w + 14, y,
            x + w, y,
            x + w, y + h,
            x, y + h,
        ]
        c.create_polygon(pts, fill=PANEL, outline=color, width=3)
        c.create_rectangle(x + 8, y + 22, x + 19, y + h - 10, fill=color, outline=color)
        c.create_text(x + 28, y + 28, anchor="w", text=title, fill=TEXT, font=("TkDefaultFont", 10, "bold"))
        c.create_text(x + 28, y + 50, anchor="w", text=role, fill=MUTED, font=("TkDefaultFont", 8))

        # coded folder variation badge
        badge = {
            "canon": "C",
            "watcher": "W",
            "holder": "H",
            "sandbox": "S",
            "runtime": "R",
            "simulation": "Σ",
            "evidence": "E",
        }.get(kind, "•")
        c.create_oval(x + w - 28, y + h - 28, x + w - 8, y + h - 8, fill=color, outline="")
        c.create_text(x + w - 18, y + h - 18, text=badge, fill="#0d1117", font=("TkDefaultFont", 8, "bold"))

    def draw_edge(self, c, x1, y1, x2, y2, color, label_text, width):
        c.create_line(x1, y1, x2, y2, fill=color, width=width, arrow=tk.LAST, smooth=True)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        c.create_text(mx, my - 8, text=label_text, fill=color, font=("TkDefaultFont", 8, "bold"))

    def draw_legend(self, c, x, y):
        items = [
            ("canon", COLORS["canon"]),
            ("watcher", COLORS["watcher"]),
            ("holder", COLORS["holder"]),
            ("sandbox", COLORS["sandbox"]),
            ("runtime", COLORS["runtime"]),
            ("simulation", COLORS["simulation"]),
            ("evidence", COLORS["evidence"]),
        ]
        cx = x
        for name, color in items:
            c.create_rectangle(cx, y - 10, cx + 12, y + 2, fill=color, outline="")
            c.create_text(cx + 17, y - 4, anchor="w", text=name, fill=MUTED, font=("TkDefaultFont", 8))
            cx += 100


if __name__ == "__main__":
    App().mainloop()
