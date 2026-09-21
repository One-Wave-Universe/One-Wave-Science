#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np

@dataclass
class Q:
    w: float
    x: float
    y: float
    z: float
    def as_arr(self):
        return np.array([self.w, self.x, self.y, self.z], dtype=float)
    @staticmethod
    def from_arr(a):
        n = np.linalg.norm(a)
        a = a / n if n else np.array([1.0, 0.0, 0.0, 0.0])
        return Q(*a.tolist())
    def conj(self):
        return Q(self.w, -self.x, -self.y, -self.z)
    def __mul__(self, other):
        a, b = self, other
        return Q.from_arr(np.array([
            a.w*b.w - a.x*b.x - a.y*b.y - a.z*b.z,
            a.w*b.x + a.x*b.w + a.y*b.z - a.z*b.y,
            a.w*b.y - a.x*b.z + a.y*b.w + a.z*b.x,
            a.w*b.z + a.x*b.y - a.y*b.x + a.z*b.w,
        ]))

def axis_angle(axis, radians):
    axis = np.asarray(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    h = 0.5 * radians
    return Q(math.cos(h), *(math.sin(h) * axis))

def trip_receipt():
    z = np.array([0.0, 0.0, 1.0])
    q = Q(1.0, 0.0, 0.0, 0.0)
    step = axis_angle(z, math.pi / 3)
    print("POINT-SPIN 4pi trip")
    for i in range(13):
        print(i, i*60, round(q.w,4), round(q.x,4), round(q.y,4), round(q.z,4), "+" if q.w>=0 else "-")
        q = step * q

if __name__ == "__main__":
    trip_receipt()
