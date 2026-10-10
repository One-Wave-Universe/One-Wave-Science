"""G-770 planar field-rotation kinematic control; no novel physics asserted."""
import math

def wrap(theta):
    return math.atan2(math.sin(theta), math.cos(theta))

def field_angle(bx, by, eps=1e-12):
    if math.hypot(bx, by) <= eps:
        raise ValueError("Undefined field orientation: vanishing transverse field")
    return math.atan2(by, bx)

def compose(field, path, point):
    """SO(2) nested-frame orientation in a common planar convention."""
    return wrap(field + path + point)

def rotate(theta, x, y):
    c, s = math.cos(theta), math.sin(theta)
    return (c*x-s*y, s*x+c*y)

def laboratory_child_vector(field, path, point, vector=(1.0, 0.0)):
    v = vector
    for angle in (point, path, field):
        v = rotate(angle, *v)
    return v

def field_rate(bx, by, dbx, dby, eps=1e-12):
    norm2 = bx*bx+by*by
    if norm2 <= eps*eps:
        raise ValueError("Undefined field rotation rate at zero transverse field")
    return (bx*dby-by*dbx)/norm2
