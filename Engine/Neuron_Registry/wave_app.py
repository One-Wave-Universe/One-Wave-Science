#!/usr/bin/env python3
"""Desktop wave manipulator. Two opposing +5/-5 walks. Writes cell STATE only."""
from __future__ import annotations

import json
import math
import tkinter as tk
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CELLS = ROOT / "cells"
W, H, CX, CY, R = 520, 560, 260, 260, 180


def label(p: int) -> int:
    r = p % 12
    return r - 12 if r > 6 else r


def seat_xy(seat: int):
    # map -5..6 onto a circle; 0 at top, 6 at bottom
    if seat == 6:
        ang = math.pi
    elif seat >= 0:
        ang = -math.pi / 2 + seat * (math.pi / 6)
    else:
        ang = -math.pi / 2 + seat * (math.pi / 6)
    return CX + R * math.cos(ang), CY + R * math.sin(ang)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("One-Wave manipulator")
        self.geometry("520x600")
        self.configure(bg="#1a1612")
        self.f = self.b = 0
        self.running = False
        self.canvas = tk.Canvas(self, width=W, height=H - 80, bg="#1a1612", highlightthickness=0)
        self.canvas.pack()
        bar = tk.Frame(self, bg="#1a1612")
        bar.pack(fill="x")
        tk.Button(bar, text="Go", command=self.go).pack(side="left", padx=8)
        tk.Button(bar, text="Hold", command=self.hold).pack(side="left")
        tk.Button(bar, text="Reset", command=self.reset).pack(side="left", padx=8)
        self.msg = tk.Label(bar, text="0 pivot  ±5 walks  6 half-cycle", fg="#d9c8a0", bg="#1a1612")
        self.msg.pack(side="left", padx=12)
        self.draw()

    def go(self):
        self.running = True
        self.tick()

    def hold(self):
        self.running = False

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
            p.write_text(json.dumps({"id": name, "seat": seat, "step": step, "choice": choice}, indent=2))

    def draw(self):
        c = self.canvas
        c.delete("all")
        c.create_oval(CX - R, CY - R, CX + R, CY + R, outline="#8a7a55")
        for s in list(range(-5, 6)) + [6]:
            x, y = seat_xy(s)
            c.create_text(x, y, text=str(s), fill="#d9c8a0")
        lf, lb = label(self.f), label(self.b)
        xf, yf = seat_xy(lf)
        xb, yb = seat_xy(lb)
        c.create_oval(xf - 8, yf - 8, xf + 8, yf + 8, fill="#c4a35a", outline="")
        c.create_oval(xb - 8, yb - 8, xb + 8, yb + 8, fill="#6a8f6a", outline="")
        meet = lf == 6 and lb == 6
        home = lf == 0 and lb == 0
        self.msg.config(text=f"fwd {lf}  back {lb}  |  6 begin-close={meet}  0 closed={home}")


if __name__ == "__main__":
    App().mainloop()
