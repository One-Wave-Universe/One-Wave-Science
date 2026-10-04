# Mirror basin boundary branch-step
MAIN GOAL: advance the reliable software construction engine through a bounded, reproducible science solver.
WHY: W1 in NOTES_2026-10-03_SM_ATTACK_VECTORS_AND_OW_WEAK_SPOTS.md reports collapse of both Mirror seeds under weave.
CURRENT STEP GOAL: derive the smooth quartic bifurcation; scan beta_K, beta_T, mu with cross on/off and inspect the 13-coordinate Hessian.
HARD START: verified main 5a6dba0e340edbe12b11b9fad682817ce7c68963, clean task worktree.
LOCAL REPO ROOT: /tmp/one-wave-mirror-20261004, linked to verified /home/Scales/One-Wave-Science on localhost.localdomain.
ACTIVE BRANCH: science/mirror-basin-boundary-20261004.
REFERENCE FILES: GENERAL_REFERENCE_RULES.md, AGENTS.md, JETSON_OPENCLAW_RUNTIME.md, BRANCH_STEP_PROJECT_TEMPLATE.md, G-757, G-760, G-762, science attack notes.
ALLOWED FILES: this packet, mirror_basin_scan.py, test_mirror_basin_scan.py, mirror_basin_scan_receipt.json, MIRROR_BASIN_RESULT.md in this directory.
PROTECTED: legacy e4_seven_cell.py and all existing nodes/metadata; original checkout dirty relay and inbox/outbox; main.
EXACT ACTION: opt-in solver replacing only M in the experimental energy; phase gauge pc=0, positive amplitudes, Gamma=0 local branch.
SUCCESS: reduced-energy identity, below/above threshold controls, cross-on minima, two Hessian step sizes, 90-case receipt.
TESTS: python3 -m unittest -v test_mirror_basin_scan; python3 mirror_basin_scan.py --output mirror_basin_scan_receipt.json; git diff --check.
FIELD PROPOSAL: isolate experiment so legacy M and existing results cannot silently change.
VOID PRE-OVERSIGHT: deterministic scope check ALLOW; do not claim physical mass, barrier or full G-762 hold.
ATTEMPT: 1/3.
HARD STOP: tested basin scan and review-ready PR; no NEB or W derivation in this step.
HANDOFF: barrier computation on surviving endpoints, then independently justified W. Scientific gate remains YELLOW.

PROGRESS REPORT: six focused tests pass; 90-case scan complete; 45 pairs accepted, 9 above-threshold optimizer warnings retained. Inherited legacy test: 2 pass, 1 fail.
VOID POST-OVERSIGHT: deterministic CPU checks support basin result only; ALLOW review of experiment, HOLD broader physics claims and merge readiness until inherited baseline disposition/review.
WORKING FEATURE: explicit smooth Mirror solver; legacy source unchanged.
FAILED APPROACH LEDGER: no correction attempts; L-BFGS-B warnings recorded raw, not relabeled.
LOOK-BACK: analytic competition explains collapse; selected twice-threshold pairs survive. Full G-762 hold and W remain open. This supplies executable evidence and a testable handoff for the construction engine.
HARD STOP STATUS: basin step complete; original broad theory goal PARTIAL. DO NOT SCALE to mass claims.
