# Branch Step — Full Multi-Radix Wave Computing Node

## MAIN GOAL
Build a falsifiable software primitive for the working One-Wave computing sequence without collapsing binary, ternary, Actions, Views, return evaluation, or scale-local differential memory into one state.

## WHY THIS STEP EXISTS
The original prototype synchronized the octave nodes too strongly, discarded ternary direction with `abs()`, and stopped at the forward 2→3→4 half instead of completing the return cycle.

## CURRENT STEP GOAL
Implement and verify the full experimental cycle:

`BC-DC -> TC-AC -> 4 Actions -> 4 Views -> TC Return -> BC Closure`

## HARD START
Start from the user-provided NumPy prototype and the established Actions-first order.

## ACTIVE BRANCH
`simulation/full-multiradix-wave-node`

## ALLOWED FILES
Only `Experiments/Wave_Computing_Node_v1/`.

## PROTECTED WORKING FEATURES
- Binary directional seed remains two-state.
- Ternary forward state remains -1/0/+1.
- Actions occur before Views.
- Actions and Views remain separate four-state layers.
- Ternary return can HOLD at 0.
- Binary closure does not gain a third state; HOLD means the closure gate does not engage.
- Each octave keeps a local moving reference.
- Next octave receives a signed differential packet.

## EXACT ACTION
1. Preserve ternary sign during quadratic rotation.
2. Split four Actions from four Views.
3. Add local moving reference per octave.
4. Add explicit ternary return evaluation.
5. Add explicit binary closure.
6. Pass bounded signed differential output to the next scale.
7. Run a 12-step / three-octave demonstration.

## TESTS / CHECKS
- `python -m py_compile wave_computing_node.py` -> exit 0.
- `python wave_computing_node.py` -> exit 0.
- Output shows octave divergence and HOLD cases.
- Example divergence: Step 06 Scale 2 reaches `BCc:-1` while Scale 0 is `+1` and Scale 1 is HOLD.
- Example HOLD: Step 07 Scale 0 has `TCr:0` and `BCc:HOLD`.

## FIELD NOTES
The scales now carry independent references and can disagree. Ternary sign is no longer erased before the Action layer.

## VOID OVERSIGHT / OVERRIDE NOTES
Treat all coefficients, thresholds, scalarization weights, and phase offsets as experimental parameters. The successful software run demonstrates internal behavior only; it does not establish that a physical circuit implements the same dynamics.

## PROGRESS REPORT
PASS for syntax and executable demonstration.

## ATTEMPT / STRIKE COUNT
Approach 1, Attempt 1/3 — PASS.

## LOOK-BACK REFLECTION
The full 2→3→4→4→3→2 structure is now explicit. Independent local references are sufficient to stop the three example octave nodes from being simple synchronized copies. HOLD is represented as closure inactivity rather than inventing a third binary value.

## HARD STOP
Stop after storing the verified v1 experiment and its output. Do not infer physical validation and do not add mirrored node pairs in this branch.

## HANDOFF / NEXT PERMITTED STEP
A separate branch may test two complete nodes as a mirrored pair with a shared differential center and independent local state.
