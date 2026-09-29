# Shared coding bench

Not the cell. Not Nodes/ write. Not finished-by-vibes.
Lives on branch shared-coding-bench until a section receipt exists.

## Layout

```
PLAN | GOALS | CONSTRAINTS | NO-GO     (always visible, read-only to AIs)

[ Gemini show/tell + sandbox ]   [ MAIN STAGE ]   [ DeepSeek show/tell + sandbox ]
                                 Grok codes here
                                 one SECTION at a time

[ shared chat: packets only ]
```

Each AI:
- sees plan/goals/constraints/no-go
- has its own sandbox directory (cannot write main stage)
- has a show/tell pane (diff + test receipt, not a speech)
- may PROPOSE an alternate into the shared chat

Main stage:
- only Grok (or the appointed coder) applies patches
- only after the section tests pass in the proposer sandbox AND a copy-run on stage
- OWATCH: reference + intention + consequence or HOLD

## Roles

| Seat | Does | Must not |
|---|---|---|
| Grok | main coding on stage | skip section tests |
| Gemini | watch, suggest, test in gemini/sandbox | write stage or Nodes/ |
| DeepSeek | watch, suggest, test in deepseek/sandbox | write stage or Nodes/ |
| Human / Folder Holder | merge section, raise no-go | treat chat as authority |

## Sections (failure isolation)

Work one section. A section has:
- name
- in-scope files
- tests that must pass
- explicit out-of-scope
- fail closed if another section breaks

No “project finished” flag. Status is always:
`SECTIONS_PASSING / SECTIONS_OPEN / NO-GO_HIT`

Best-it-could-be means every open section has a passing receipt and no no-go remains waived.

## Packet

```
reference: file:span or section-id
intention: propose | watch | test | hold
consequence: what breaks if applied
actor: grok|gemini|deepseek|human
```

Missing field → HOLD. Chat text without a packet is noise.

## No-go (starter)

- write Nodes/ from a sandbox
- merge without section tests
- boost route memory on HOLD
- call the bench a cell or a mind
- mark finished while any section is open or untested

## Dirs (when built)

```
One_Wave_Bench/shared_bench/
  PLAN.md
  GOALS.md
  CONSTRAINTS.md
  NOGO.md
  stage/          main project slice
  sandboxes/grok/
  sandboxes/gemini/
  sandboxes/deepseek/
  chat/packets.jsonl
  sections/
```
