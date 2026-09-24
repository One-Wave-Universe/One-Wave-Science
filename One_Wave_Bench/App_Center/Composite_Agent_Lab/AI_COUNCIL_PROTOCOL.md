# AI Council Protocol

The Miniverse room is the council chamber. The council is structured, not an unrestricted group chat.

## Core seats
- **M4** — chair/body state; owns thresholds, hysteresis, retained memory, and whether the system is ready to act.
- **Void** — admin/inner voice; can ALLOW, CORRECT, OVERRIDE, HOLD, or ESCALATE.
- **Field** — senses and sole outward voice/action.
- **Reference Goblin** — source/evidence gate.
- **Parser Goblin** — normalizes inputs and proposed actions.
- **Doctor Goblin** — diagnoses failed routes/results.
- **Goblin Raccoon** — seeks materially different approaches when the council gets stuck.
- additional AI specialists may occupy bounded advisory seats.

## Council cycle
```text
REFERENCE
 -> specialist evidence/proposals
 -> bounded DELIBERATION
 -> VOID ADMIN REVIEW
 -> M4 BODY/GATE
 -> FIELD outward response/action
 -> result/evidence
 -> REFERENCE RETURN
 -> next round or close
```

## Speech law
Only Field speaks outward for the composite agent. Other council members write structured evidence, objections, proposals, or votes into shared state. This avoids token-heavy multi-agent chatter.

## Disagreement
Disagreement is preserved as structured differentials. Void does not decide by majority vote alone; it evaluates references/evidence and protected state. M4 still gates the resulting action.

## Specialist seats
Examples: coding, science/reference, hardware, UX, testing, security, local-model specialist, cloud-model specialist. Seats are temporary and task-scoped.

## Token economy
Each seat receives the same compact council packet plus only the evidence it needs. No seat gets full transcript replay by default.

## Room mapping
- HOME / BASELINE ZERO = reference opening/closing
- WORKSHOP = proposal/build
- TEST LAB = validation
- REVIEW = Void/council review
- RECALL = memory/evidence retrieval
- TRANSIT / M4 = routing/body integration
- WAREHOUSE = artifacts/results

This council protocol is a software coordination design. It does not imply independent consciousness or literal merger of models.
