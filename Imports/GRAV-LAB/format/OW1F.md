# OW1F — One Wave lattice file

Digital lattice space. Two packs in one header. D-408 native. D-409 opt-in.

## Packs (do both)

| pack | code | neighbors | honest name |
|---|---|---|---|
| stacked-hex | `0` | 6 in-plane + 2 sheet = 8 | D-408 sheets. Default. |
| fcc-12 | `1` | 12 | close pack. Yellow until a print prefers it. |

HCP is pack `1` with odd-sheet in-plane shift; v1 implements FCC via XYZ distance `a`.

## Basis (D-408)

```
a1 = a (1, 0, 0)
a2 = a (1/2, sqrt(3)/2, 0)
a3_stacked = (0, 0, h)
```

Site `r = m a1 + n a2 + p a3`.
Primary key is integers `(m,n,p)`. XYZ is derived.

In-plane neighbor offsets (k=0..5):

```
(+1,0,0) (-1,0,0) (0,+1,0) (0,-1,0) (+1,-1,0) (-1,+1,0)
```

Three axis pairs: 0+-, 1+-, 2+-. D-411: do not merge this 3:1 with GCAC 3:1.

Stacked extra: `(0,0,+1) (0,0,-1)`.

FCC-12: all other sites whose embedded |r'-r| is within `1.01 a`.

## Header

```
magic     4s   OW1F
version   u16  1
a         f64
h         f64
Nm Nn Np  i32
m4_pair   u8   0=P0-P3  1=P1-P4  2=P2-P5
pack      u8   0 stacked  1 fcc-12
bath      f32
```

Then `Nm*Nn*Np` sites, row-major `id = m + Nm*(n + Nn*p)`.

## Site

```
psi psi_last spin align   f32
q0 q1 q2 q3               f32   unit quaternion + sheet
P                         f32   occupancy
trit                      i8    -1 0 +1
field_void                u8    1=Field 0=Void
```

`field_void` is binary state. `trit` is resolved orientation of the 7-cluster, not a third stored voltage.

## Ground

Undisplaced: u=0 v=0. Lattice sits. Child facing walks. Parent writes.
Camera is not in the update law (D-412).
