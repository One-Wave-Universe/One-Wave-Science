# Chromatic circle symmetries

The 12-rail is \(\mathbb{Z}/12\mathbb{Z}\). Two symmetry layers, both Yellow algebra.

## 1. Rigid motions of the clock (dihedral \(D_{12}\))

- Rotation \(R(n)=n+1\). Order 12. Hour-step.
- Reflection through 0–6: \(S(n)=-n\). Fixes 0 and 6 only.
- 180° turn: \(I(n)=n+6=R^6\). No fixed points. Six pairs.
- Relation: \(S R S = R^{-1}\).

S is a *flip* (axis through 6 o'clock). I is a *turn* (same 6, but spin not mirror).

## 2. Relabelings that keep addition (Aut(\(\mathbb{Z}/12\)))

Units mod 12:

$$
\{1,5,7,11\}\cong C_2\times C_2
$$

| Map | Action on +1 | Rail name |
|---|---|---|
| \(\times 1\) | +1 | identity |
| \(\times 5\) | +5 | −7 the other way |
| \(\times 7\) | +7 | fifth rail |
| \(\times 11=-1\) | +11 | same as S on the group |

Each of 5,7,11 has order 2. So \(\times 7\) twice is home: two fifth-circles of six land on the diameter (\(T^6=I\)).

\(\times 7\) does **not** add a new generator outside the clock. It is how you *read* the same 12 points as a fifth-walk instead of an hour-walk.

## 3. Chords under S

- Major `{0,4,7}` → `{0,5,8}` under S.
- Minor `{0,3,7}` → `{0,5,9}` under S.
Reflection swaps the lean of -5(0)4+ versus -5(0)3+.

Augmented `{0,4,8}` is a 3-cycle of +4. S sends it to itself as a set (balanced, no lean).

## 4. What this is not

Not T6. Not Mass Effect. Not a claim that hours are quarks. Semitone talk stays Gray SM; the rail only has +7/−5 and the 6-diameter.
