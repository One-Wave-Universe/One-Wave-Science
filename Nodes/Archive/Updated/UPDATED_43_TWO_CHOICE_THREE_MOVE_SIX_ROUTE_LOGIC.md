# Updated 43 — Two-Choice, Three-Move, Six-Route Logic

**Status:** Canonical primitive correction and executable reference  
**Gate:** YELLOW (finite logic and tests) / BROWN (physical carrier)

## 1. Permanent count correction

The primitive choice count is two, not three:

```text
(1,0) = YES / AGREE
(0,1) = NO / DISAGREE
```

`(0,0)` is Ground/no committed binary choice. It is not a third binary choice.
`(1,1)` is conflicting dual assertion and is invalid unless a later hardware
node derives a diagnostic use for it.

The movement count is three:

```text
-1 = movement in one orientation
 0 = active HOLD at the shared center
+1 = movement in the opposite orientation
```

Therefore the combined primitive logic contains

`2 choices x 3 movements = 6 routes`.

Ground remains outside the six-route choice set.

## 2. Exact finite set

Let

`B2={(1,0),(0,1)}`

and

`T3={-1,0,+1}`.

Then

`L6=B2 x T3`

contains exactly:

```text
YES/DOWN, YES/HOLD, YES/UP,
NO/DOWN,  NO/HOLD,  NO/UP.
```

This is a six-route address space. It does not mean that YES/HOLD and NO/HOLD
are physically stationary in every internal variable. They retain different
binary relations while their net movement is Hold.

## 3. Five commitment states are downstream

The five commitment/readout states are:

```text
-3(0)3+ = full disagree
-2(0)2+ = partial disagree
1:1      = unity / ultimate compression / Hold reference
+2(0)2- = partial agree
+3(0)3- = full agree
```

These five states are not multiplied into the primitive choice count. They are
a later amplitude/commitment interpretation of a route and its history.

The unresolved derivation is a map

`K : (route, prior_state, differential, thresholds, phase) -> {-3,-2,0,+2,+3}`.

No arbitrary lookup table is canonical until this map is derived or calibrated.

## 4. Asymmetric oscillation

Ternary movement is not three frozen labels. It is a readout of motion around
an active center. The two oriented traces are written:

```text
+1(0)1-
-1(0)1+
```

They preserve which side approaches, crosses, and leaves the center. Hold is
the active switching/reference region, not absence.

A minimal continuous candidate for mathematical testing is

`x_ddot + 2*zeta*omega0*x_dot + dV(x;h)/dx = u(t)`

with a biased double-well candidate

`V(x;h)=a*x^4/4-b*x^2/2-h*x`.

`h` supplies asymmetry/differential. This equation is a proposed test bench,
not yet the One-Wave physical law. Required outputs are center residence,
crossing direction, partial/full excursion, hysteresis, return, and phase.

## 5. DC, AC, and phase-memory sequence

The proposed physical control sequence is:

```text
DC Field/reference
-> one-hot binary YES/NO choice
-> ternary DOWN/HOLD/UP movement
-> asymmetric phase/orientation resolution
-> downstream phase-memory preparation
-> modulation
-> readout
-> phase correction
-> return to current Field/reference
```

The DC layer defines bias/reference. The AC layer supplies oscillation, timing,
and phase modulation. A four-level quantum device may be called a ququart only
after coherent four-level control is demonstrated. Before that, use
`four-state phase memory`.

The exact mapping from six routes to four active phase-memory states remains
open. Earlier conversational guesses are not canonical mathematics.

## 6. Magnonic carrier candidate

Quadrature drive may synthesize a rotating magnetic field:

`B_rot=B0[cos(omega*t)*x_hat+sin(omega*t)*y_hat]`.

Candidate local magnetization dynamics use the Landau-Lifshitz-Gilbert model.
Spin-wave phase, magnetic vortex polarity/circulation, MTJ readout, and ISHE
readout are hardware candidates.

Required correction: magnon transport may reduce charge motion along a
waveguide, but total energy includes RF generation, damping, injection,
conversion, readout, clocking, and thermal error. `No Joule heating` is not a
valid whole-system claim.

## 7. Cube hierarchy held as hypothesis

```text
9 ternary cube chips -> 1 Rubix
9 Rubix -> 1 Rudies cube
1 Rudies cube = 81 ternary cube chips
```

Vascular folding is the candidate routing method that carries planar ternary
relationships through a filled volume. The geometry of each group of nine is
not yet locked. No file may silently choose a 3x3 sheet, 3x3x1 slab, or another
nine-position geometry without declaring it as an experiment.

## 8. Programmed Dream World boundary

G-726 remains a non-cognitive programmed dream world in native 2D space. It has
no Administrator. Ternary `3` describes local state, not spatial dimension.
Rendered depth does not promote the authoritative world state to 3D.

## 9. Executable authority

Reference implementation:

- `One_Wave_Bench/logic_core/six_route_logic.py`
- `One_Wave_Bench/logic_core/test_six_route_logic.py`

The reference implementation owns only the finite count and validation rules.
It does not pretend to solve commitment dynamics, qudits, magnetic hardware,
or consciousness.

## 10. Failure conditions

- `(0,0)` is counted as a binary choice;
- five commitment states are multiplied into the primitive choice count;
- the route count differs from six;
- Ground is confused with YES/HOLD or NO/HOLD;
- ternary state is misread as spatial dimension;
- quantum terminology is used without coherence measurements;
- a physical carrier is promoted without energy, noise, and readout budgets.

## 11. Relationship to recursive Point–Path–Field

The six-route primitive updates a relation; it does not replace geometry.
Every scale can carry a recursive Point–Path–Field state:

```text
Point rotation = intrinsic/local orientation about a center
Path rotation  = turning or circulation of that center along a route
Field rotation = circulation/curl of the enclosing carrier or boundary
```

A Point, Path, or Field may itself contain lower-scale PPF states. Separate
frames and receipts must prevent internal rotation from being mistaken for
orbital rotation or enclosing-Field circulation. The calculation program is
specified in `MATH_ATTACK_MAP_UPDATED_43.md`.

## 12. Gray-physics guardrail

One Wave supplies candidate mechanisms and additional state definition. It
does not erase Newtonian or Einsteinian results that already measure orbital
behavior. Every orbital extension must run against Newtonian and appropriate
relativistic controls, recover them when One-Wave couplings go to zero, and
show whether the added mechanism improves held-out observations rather than
only redescribing them.
