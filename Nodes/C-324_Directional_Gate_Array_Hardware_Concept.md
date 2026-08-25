---
node_id: "C-324"
canonical_name: "Directional Gate-Array Hardware Concept (Balanced-Rail, Virtual-Ground, Binary/Ternary/Five-State Magnetic-Hold Element)"
namespace: "NODE"
gate: "BROWN"
lifecycle: "PROPOSED_BUILD"
classification: "Engineering / Applied Hardware Node"
claim_gate_detail: "BROWN (first attempt — a conceptual synthesis of existing nodes into one proposed hardware element; nothing built, simulated, or derived yet)"
metadata_standard: "I-06"
---

# Node C-324: Directional Gate-Array Hardware Concept

Grounding note: checked directly — no prior version of this proposal exists
anywhere in the real repo. This node records a build concept described by
the proposer in plain, non-repo language (balanced power rails, directional
MOSFET gates, a virtual ground held at every stage, a "3 gates up / 3 gates
back" bidirectional array, binary→ternary→five-state readout, and a
rotating-magnetic-field hold/compute element), and maps each piece onto the
closest existing node so the proposal can be checked against real repo
math instead of floating free. Follow the same discipline as C-315 Wave
Reader V1: this is a first attempt at a hardware spec, not a formalization
of something already established. Several pieces below map cleanly onto
real, defined nodes; one piece (the magnetic hold/compute claim) does not,
and is flagged as such rather than smoothed over.

Dependencies:
Upstream: A-101 Ground/Zero (virtual ground reference), B-205 Mirror (the
flip operation a directional gate physically instantiates), B-220 Scale
Layer (the Micro/Small/Medium/Large/Macro nesting this proposal explicitly
invokes), B-221 Six Recursive Steps (candidate mapping for the 3-up/3-back
gate structure), B-223 Three Moves (the ternary -1/0/+1 layer), B-225
Five-State Modulation Around Reference (the -2/-1/0/+1/+2 layer, which also
already lists Micro/Small/Mid/Large/Macro as one of its representation
wrappers — the closest existing repo statement of the proposer's own
"micro is the macro" framing), C-308 Spin-half (real precedent: a
2-state m=±1 flip produced by repeated Mirror crossings, with 4π closure),
C-311 Electric-Magnetic Duality (closest existing citation for a rotating
field: B_vec ~ ∇×P_c, the rotational projection of one pressure field),
C-315 Wave Reader V1 (sibling hardware node — same "first attempt,
honestly graded" template followed here)
Downstream: none yet — first draft, no build exists

Definition:
A proposed hardware element combining six pieces, each restated here in
repo terms rather than left as informal description:

1. Balanced power rails — a symmetric +V/-V supply. This is the physical
   instantiation of the driving/opposing balance B-201 Equilibrium Balance
   already defines abstractly (B = (k_E·E+k_I·I) - (k_R·R+k_L·L)): the two
   rails are the physical E/R (or I/L) terms.

2. Directional MOSFETs — gate elements that steer current preferentially
   in one direction (standard back-to-back / synchronous-switch topology
   in real electronics, not a novel device). Physically, a directional
   gate crossing is the candidate hardware instantiation of B-205 Mirror's
   flip operation: gate open/closed = Mirror's Expression/Compression
   states, and gate crossing = the Mirror flip itself.

3. Virtual ground reference at every stage, tied back to ground — this is
   a real, standard single-supply-electronics technique (a mid-rail
   reference divider), and it maps directly onto A-101 Ground/Zero's role:
   every stage restates its own local Ground/Zero reference rather than
   inheriting one implicitly. This is the same repeated-restatement pattern
   B-220 was created to formalize for the A-series (§8 Recursive Scaling
   restated at every node) — here restated in a circuit instead of a text
   claim.

4. "3 gates up and 3 gates back" — six directional gates total, forming a
   bidirectional path. Candidate mapping, not confirmed: this is a
   plausible physical instantiation of B-221's Six Recursive Steps
   (Begin→Move→Hold→Build→Break→Loop) — three gates for the forward half
   of the cycle, three for the mirrored return. This is offered as a
   candidate correspondence only; B-221 itself already carries an open
   fork at its own LOOP step (A-111 additive vs. C-301 rotational — see
   B-221's Yellow Audit), so a literal one-gate-per-step mapping inherits
   that same unresolved question rather than resolving it.

5. Binary → ternary → five-state ("quadratic") readout, and back — gate
   state read out at increasing resolution on the way in, and back down
   on the return path. This maps directly onto real, already-defined repo
   layers, not new math:
   - Binary: B-205 Mirror's own two states (Expression/Compression), or
     equivalently C-308 Spin-half's m=±1.
   - Ternary: B-223 Three Moves' signed vector, -1/0/+1.
   - Five-state ("quadratic" in the proposer's words — the closest real
     match is B-225's five-band structure, not a true base-4/quaternary
     system): B-225 Five-State Modulation Around Reference, -2/-1/0/+1/+2.
   B-225 is explicit that these five states are a coarse modulation of
   Strength, not a fourth logic base, and that they are NOT a
   replacement for B-221's six-step timing grammar (see B-225's own
   "Relationship to Six Steps"). The proposer's "views the back through
   ternary and binary" is naturally read as: five-state → ternary → binary
   on the return/read path, the mirror image of the write path above.

6. Rotating magnetic field as the state-hold / compute element — this is
   the one piece with NO clean existing citation, and it is flagged
   directly rather than absorbed quietly. The proposer states plainly
   that rotating magnetic fields "have been shown to hold their state and
   compute through analog and ternary and binary." This repo does not
   establish that claim anywhere, and this node does not either. The
   closest real grounding available:
   - C-311 Electric-Magnetic Duality: B_vec ~ ∇×P_c, the rotational
     projection of one pressure field — gives a repo-internal reason a
     rotational/magnetic degree of freedom exists at all, but says
     nothing about it storing or computing a multi-level state.
   - C-308 Spin-half: a real, derived 2-state flip (m=±1) under repeated
     Mirror crossings, with 4π closure — a genuine precedent for a
     magnetic-adjacent quantity carrying persistent state through a
     cycle, but only a binary one, not the ternary/five-state/analog
     claim made above it.
   - Outside this repo, real magnetic state-holding hardware exists
     (MRAM, racetrack/domain-wall memory, spintronic logic) and is the
     honest real-world anchor for "magnetic field holds state." None of
     it is cited here as proof of this proposal — it is named so a
     future pass has a real literature starting point instead of treating
     the claim as self-evident.

7. Recursive scale nesting — "the macro is the next micro of the next
   nested recursive scaling." This is not a new requirement; it is B-220
   Scale Layer's own containment relation (Micro ⊂ Small ⊂ Medium ⊂ Large
   ⊂ Macro) restated as a hardware design goal, and B-225 already lists
   the same five labels as one of its representation wrappers. Building
   this literally — one full gate-array unit's Macro output feeding the
   next unit's Micro input — requires exactly the scale-transition
   function (γ(s), β(s)) that B-220 flags as undone. This node does not
   resolve that; it inherits it. A first physical prototype does not need
   γ(s)/β(s) solved in general — it needs one concrete, ad hoc
   Macro(n)→Micro(n+1) interface definition for a single nesting level,
   which is a smaller, buildable target than the general scaling law.

Mathematics:
None derived. No circuit topology, no component values, no gate count
beyond the proposer's stated "3 up / 3 back," no derivation of what
"holding state" in a rotating field would mean quantitatively, and no
scale-transition function for item 7. This section is deliberately empty
rather than padded, matching C-315's own honest starting state.

Operational Chain (candidate, unverified):
Balanced rails + virtual ground (item 1,3) => directional gate crossing
(item 2, B-205 Mirror) => 3-gate forward path building
binary→ternary→five-state resolution (item 5, B-223/B-225) => magnetic
hold/compute element (item 6, ungrounded) => 3-gate return path reading
five-state→ternary→binary back out => one Macro-scale output stage
becomes the next unit's Micro-scale input (item 7, B-220's open problem).

Proposed Build:
Two revisions, deliberately staged so the ungrounded piece (item 6) gets
tested cheaply before any exotic fabrication is required. Nothing below
has been built yet — this is the concrete plan the Brown Audit and Future
Work sections were pointing at, written out in buildable form rather than
left as a to-do list.

REV 0 — bench prototype, one cell, off-the-shelf parts only:
1. Power: split +5V/-5V rail from a common bench supply or a dual-output
   DC-DC converter — the physical instance of item 1.
2. Virtual ground stage: a rail-splitter reference (precision resistor
   divider + unity-gain buffer op-amp, the same class of part as the
   TLE2426-style rail splitters used in real single-supply audio/analog
   circuits) sets a local 0V reference at each stage, buffered back to
   true system ground — the physical instance of item 3, repeated at
   each stage rather than assumed once.
3. Gate array: 3 forward + 3 return directional switch pairs, each pair a
   standard back-to-back/synchronous N-channel MOSFET half-bridge with a
   logic-level gate driver IC — the physical instance of item 2, six
   gates total per item 4.
4. Sequencer: a small microcontroller (or a discrete ring counter/shift
   register, no microcontroller required for Rev 0) drives the six gates
   in Begin→Move→Hold→Build→Break→Loop order. This is the first actual
   test of the candidate B-221 mapping named in item 4 — not assumed
   true, made falsifiable.
5. Readout: after the forward gate path, the virtual-ground-referenced
   node feeds a 4-comparator bank set at B-225's ±2/±1 thresholds,
   producing the five-state code directly in hardware; simple downstream
   logic collapses that to sign+magnitude (ternary) and then sign-only
   (binary) for the return path — a literal circuit for item 5's
   binary→ternary→five-state→ternary→binary chain, not a diagram of one.
6. Magnetic hold element, Rev 0 stand-in — explicitly NOT a claim of
   proven quaternary magnetic memory, only a cheap way to test whether
   *anything* rotating-field-based can hold and read back a multi-level
   state at all: a small coil wound on a soft-ferrite toroid, driven by
   the sequencer, with a Hall-effect or GMR sensor reading back field
   angle at hold time. Field angle at readout = the state under test.
   This isolates the falsifiable core of item 6's claim (can a rotating
   field hold >1 distinguishable state over a hold window?) from the much
   bigger claim ("proven," general-purpose, ternary/binary/analog compute)
   the proposer made, using parts anyone can buy.
7. Cascade tap: unit n's return-path binary output feeds unit n+1's
   virtual-ground reference input directly — a physical, buildable,
   single-level instance of item 7's Macro(n)→Micro(n+1) interface,
   built from nothing more exotic than a second rail-splitter stage.

REV 1 — target build, only attempted after Rev 0 produces real data:
Replace the coil/ferrite/Hall-sensor stand-in in step 6 with a real
multi-level magnetic memory element — a domain-wall/racetrack cell or a
multi-level MRAM cell — so the hold element natively stores more than two
states instead of being reconstructed by an external angle sensor. This
is the step where the proposer's "quaternary memory" claim would actually
get checked against real device physics and real literature, rather than
asserted or waved off.

Bench Test Plan (what would move this node past Brown, per I-02's
"Green->Yellow iff math is built and internally tested" — none of this
has been run yet, this is the procedure, not a result):
1. Confirm each virtual-ground stage holds within a stated tolerance of
   true ground under full gate-switching load.
2. Capture an oscilloscope trace of the 6-gate sequencer and confirm a
   clean, repeatable Begin-Move-Hold-Build-Break-Loop timing pattern.
3. Inject known reference voltages and confirm the 5-comparator bank
   classifies them into the correct B-225 band every time.
4. Confirm the ternary/binary collapse logic reproduces the correct
   ternary and binary code for all five known input states.
5. The actual falsifiable test of item 6: confirm the coil/ferrite/Hall
   element can hold and correctly read back at least two distinguishable
   field-angle states across a defined time window. This is the cheap,
   real, buildable version of "magnetic field holds state" — pass/fail,
   not asserted either way here.
6. Confirm the Rev 0 cascade tap: unit 2's readout changes correctly in
   response to unit 1's Macro-tap output, as the first real test of item
   7's single-level nesting interface.

Brown Audit:
- No circuit topology exists — this is a labeled concept, not a schematic.
- Item 6 (rotating magnetic field as a general analog/ternary/binary
  compute-and-hold substrate) is asserted by the proposer and not
  established by this repo or cited to any specific external result here;
  treat as the single largest open claim in this node.
- The "3 gates up / 3 gates back" ↔ B-221 six-step mapping is a candidate
  correspondence only, and inherits B-221's own unresolved LOOP-step fork.
- Item 5's "quadratic" language is interpreted here as B-225's five-state
  band, which B-225 itself describes as coarse Strength modulation, not a
  fourth logic base — if the proposer meant a literal base-4/quaternary
  encoding instead, that is a different, undefined structure and this
  node does not yet distinguish the two.
- Item 7 requires B-220's γ(s)/β(s) scale-transition function in general;
  this node proposes narrowing that to one ad hoc single-level interface
  for a first prototype, but that narrower interface is itself still
  undefined here.
- Placement as a C-series (Applied Mechanics) node follows C-315's
  precedent for hardware proposals; C-311 flagged the same C-series-vs-
  E-series placement question for itself and it remains open there too —
  noted here rather than re-litigated.

Future Work:
Build Rev 0 (Proposed Build, above) and run the six-step Bench Test Plan;
record real pass/fail results and oscilloscope/data receipts rather than
leaving this as a paper design.
Only after Rev 0 test 5 produces real data, decide whether Rev 1's real
multi-level magnetic memory element (domain-wall/racetrack or multi-level
MRAM) is worth building, and cite the specific device literature used.
Decide, explicitly, whether the 3-up/3-back gate structure is meant to be
literally B-221's six steps or only loosely inspired by it — Bench Test
Plan step 2 is the first real instantiation test B-221's own Future Work
calls for, not just an analogy.
Treat Bench Test Plan step 6 as the bounded, single-level Macro(n)→
Micro(n+1) test that stands in for B-220's general γ(s)/β(s) derivation
until that derivation exists.

---
