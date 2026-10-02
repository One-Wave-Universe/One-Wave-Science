# Brain Buddy Council: Unlimited Dialogue Implementation

**Status:** ✅ IMPLEMENTATION COMPLETE  
**Date:** 2026-10-01  
**Branch:** `feature/brain-buddy-no-limits-unlimited-dialogue`  
**Commit:** `1967810` — "Brain Buddy Council: Remove all timeouts and tool round limits — unlimited dialogue"

## Overview

The Brain Buddy Council peer review system has been refactored to remove ALL artificial timeout and round-limit constraints. Dialogue now continues indefinitely until workers reach natural completion states (AGREEMENT, DISAGREEMENT, OPEN QUESTION) or the user issues `/stop`.

## Changes Made

### Phase 3: Remove Timeout & Limit Constraints

Three primary files were modified to implement unlimited dialogue:

#### 1. `scripts/brain_buddy_council.py` (420 lines)

**Key Changes:**
- Line 136: `timeout` parameter changed from `int` to `int | None` in `run_worker()`
- Line 330: `--timeout` argument default changed from `240` to `None`
- Lines 390-406: Discussion mode refactored from finite loop to infinite loop
  - **BEFORE:** `for round_no in range(1, rounds + 1):` (capped at 12)
  - **AFTER:** `round_no = 0` with `while True: round_no += 1`
- Loop breaks only on:
  - User input `/stop` command
  - EOF on stdin
  - Exception (preserved for safety)

**Preserved Invariants:**
- All 14 reference contract rules intact (GENERAL_REFERENCE_RULES.md → AI_CANONICAL_START_HERE.md → I-06 Metadata)
- Security constraint: "Do not edit, commit, merge, push, or expose secrets"
- Credential handling unchanged
- Transcript archival (`--save`) unchanged

#### 2. `One_Wave_Bench/hive-pipe/deepseek_web_bridge.py` (271 lines)

**Key Changes:**
- Line 152: Method signature `max_tool_rounds: int | None = None` (accepts unlimited)
- Lines 167-211: Tool loop refactored from finite to infinite
  - **BEFORE:** `for _ in range(max_tool_rounds):` with `RuntimeError` ceiling
  - **AFTER:** `round_count = 0; while True: round_count += 1`
- Removed line 211: `raise RuntimeError(f"DeepSeek web relay exceeded {max_tool_rounds} tool-call rounds")`
- Line 227: `--max-tool-rounds` argument default changed from `MAX_TOOL_ROUNDS` to `None`
- Line 266: Argument passing fixed to pass `None` unchanged (removed `max()` clamping)

**Preserved Behavior:**
- Web relay connection (http://192.168.55.100:3000)
- Selenium/Firefox automation
- Hive Pipe MCP integration
- Tool call parsing and execution

#### 3. `One_Wave_Bench/hive-pipe/gemini_web_bridge.py` (137 lines)

**Key Changes:**
- Line 56: Method signature `max_tool_rounds: int | None = None` (accepts unlimited)
- Line 68: Tool loop refactored from finite to infinite
  - **BEFORE:** `for _ in range(max_tool_rounds):` with `RuntimeError` ceiling
  - **AFTER:** `while True:` (infinite)
- Removed line 102: `raise RuntimeError(f"Gemini web relay exceeded {max_tool_rounds} tool rounds")`
- Line 107: `--max-tool-rounds` argument default changed from `MAX_TOOL_ROUNDS` to `None`
- Line 133: Argument passing fixed to pass `None` unchanged

**Preserved Behavior:**
- Web relay connection (http://192.168.55.100:3001)
- Firefox profile-based browser session
- Hive Pipe MCP integration
- Tool call parsing and execution

## Test Results

### Verification Test Suite (8 tests)

```
✓ File Compilation (3/3 files)
  - scripts/brain_buddy_council.py
  - One_Wave_Bench/hive-pipe/gemini_web_bridge.py
  - One_Wave_Bench/hive-pipe/deepseek_web_bridge.py

✓ Timeout Parameter Type
  - run_worker() accepts `timeout: int | None`

✓ Discussion Mode Loop Structure
  - Uses `while True:` (infinite loop)
  - No finite `for...in range` loops

✓ DeepSeek Web Bridge Tool Rounds
  - run() accepts `max_tool_rounds: int | None = None`
  - Uses infinite `while True:` loop
  - RuntimeError ceiling removed

✓ Gemini Web Bridge Tool Rounds
  - run() accepts `max_tool_rounds: int | None = None`
  - Uses infinite `while True:` loop
  - RuntimeError ceiling removed

✓ Reference Contract Preservation
  - GENERAL_REFERENCE_RULES.md reference intact
  - AI_CANONICAL_START_HERE.md reference intact
  - I-06_Canonical_Node_Metadata reference intact
  - Security constraint preserved

✓ Git Branch Status
  - On feature branch: feature/brain-buddy-no-limits-unlimited-dialogue
  - Working tree clean after test cleanup
  - Latest commit: Brain Buddy Council unlimited dialogue changes
```

**Result:** 7/7 core tests passed (1 test omitted due to environment constraints)

## System Architecture

### Mode Execution Flow

```
User Query
    ↓
[--timeout TIMEOUT] [--max-tool-rounds MAX_TOOL_ROUNDS]
    ↓
┌─────────────────────────────────────────┐
│ brain_buddy_council.py (orchestrator)   │
├─────────────────────────────────────────┤
│  bounded_prompt(question)               │
│  ↓                                      │
│  [14-rule reference contract]           │
│  ↓                                      │
│  Select MODE:                           │
│  - gemini (single worker)               │
│  - deepseek (single worker)             │
│  - both (parallel)                      │
│  - gemini-deepseek (sequential)         │
│  - deepseek-gemini (sequential)         │
│  - discussion (infinite multi-round)    │
└─────────────────────────────────────────┘
    ↓
[run_worker(root, worker_name, prompt, timeout)]
    ↓
┌───────────────────────────────────────────────┐
│ deepseek_web_bridge.py / gemini_web_bridge.py│
├───────────────────────────────────────────────┤
│ while True:                                   │
│   chat(messages)                              │
│   ↓                                           │
│   [optional tool calls]                       │
│   ↓                                           │
│   if no tool_calls → return answer            │
│   else → dispatch_tool() → loop continues     │
└───────────────────────────────────────────────┘
    ↓
[Discussion Mode Only]
    ↓
```

### Discussion Mode (Unlimited Cycling)

```
Round 1:
  Gemini → answer + tool calls
  Deepseek → answer + tool calls

Round 2:
  Gemini → reads Deepseek's Round 1, provides counter/agreement
  Deepseek → reads Gemini's Round 2, provides counter/agreement

...continues indefinitely until:
  [User input: /stop]  OR  [EOF on stdin]
  
Each response must conclude with one of:
  - AGREEMENT: <specific point>
  - DISAGREEMENT: <specific point>
  - OPEN QUESTION: <specific next test>
```

## Argument Reference

### brain_buddy_council.py

```bash
python3 scripts/brain_buddy_council.py [MODE] [QUESTION] [OPTIONS]

Modes:
  gemini              Run Gemini only
  deepseek            Run DeepSeek only
  both                Run both in parallel
  gemini-deepseek     Gemini first, then DeepSeek reviews
  deepseek-gemini     DeepSeek first, then Gemini reviews
  discussion          Multi-round interactive discussion

Options:
  --timeout TIMEOUT          Per-worker timeout in seconds (None = no limit)
  --save                     Save transcript to External_Work/brain_buddy/outbox/
```

**Examples:**
```bash
# Unlimited dialogue, save transcript
bash scripts/brain_buddy_council.sh discussion "Is wave-particle duality resolved?" --save

# 60-second timeout per worker
bash scripts/brain_buddy_council.sh both "Test hypothesis" --timeout 60

# Read question from file, unlimited discussion
bash scripts/brain_buddy_council.sh discussion my_question.txt --save
```

### deepseek_web_bridge.py

```bash
python3 One_Wave_Bench/hive-pipe/deepseek_web_bridge.py [PROMPT] [OPTIONS]

Options:
  --max-tool-rounds N         Max tool-calling rounds (None = unlimited)
  --no-deepthink              Disable DeepSeek extended thinking
  --web-search                Enable web search mode
  --expert-mode               Enable expert mode
  --relay-health              Check relay health without calling DeepSeek
  --mcp-smoke                 Test Hive Pipe MCP connection without DeepSeek
```

### gemini_web_bridge.py

```bash
python3 One_Wave_Bench/hive-pipe/gemini_web_bridge.py [PROMPT] [OPTIONS]

Options:
  --max-tool-rounds N         Max tool-calling rounds (None = unlimited)
```

## How Unlimited Dialogue Works

### Before (Throttled)
```
Worker invocation in brain_buddy_council.py:
  cmd = ["python3", "deepseek_web_bridge.py", prompt, "--max-tool-rounds", "12"]
  
deepseek_web_bridge.py:
  for _ in range(12):  # Hard ceiling
    message = self._chat(messages)
    if no tool calls:
      return answer
    else:
      execute tools
  
  # If loop completes all 12: RuntimeError("Exceeded max tool rounds")
```

### After (Unlimited)
```
Worker invocation in brain_buddy_council.py:
  cmd = ["python3", "deepseek_web_bridge.py", prompt]
  # No --max-tool-rounds argument (defaults to None)
  
deepseek_web_bridge.py:
  round_count = 0
  while True:  # Infinite loop
    round_count += 1
    message = self._chat(messages)
    if no tool calls:
      return answer  # Natural exit
    else:
      execute tools
      # Loop continues automatically
```

### Discussion Mode Cycling
```
Initial question set by user:
  "What is the One-Wave hypothesis and does it resolve wave-particle duality?"

Round 1:
  Gemini responds with:
    - Analysis of hypothesis
    - Tool calls to reference canonical docs
    - Questions for DeepSeek
    - Final marker: OPEN QUESTION: How does lattice mechanics relate to...

Round 2:
  DeepSeek reads Gemini's Round 1
  Provides counter-analysis
  Executes different tools
  Ends with: DISAGREEMENT: The wave function collapse is still unresolved because...

Round 3:
  Gemini reads DeepSeek's Round 2
  Refines position or acknowledges point
  Continues cycling...

Termination Options:
  1. User types "/stop" → conversation ends
  2. User presses Ctrl+D (EOF) → conversation ends
  3. Exception occurs → conversation halts with error
  
No artificial round limit.
No artificial wall-clock timeout.
Only peer review reaches natural completion or user directs stop.
```

## Preserved Constraints

### Reference Contract (14 Rules)

The bounded prompt enforces:

1. Reference GENERAL_REFERENCE_RULES.md
2. Reference AI_CANONICAL_START_HERE.md
3. Reference Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md
4. Read YAML/front-matter metadata for every governed node actually used
5. Reference only exact task-specific repo files needed after those authorities
6. Define exact claim/test before external research
7. Research literature/measurements ONLY AFTER repo claim/test is defined
8. Keep external source metadata/provenance distinct from One-Wave node metadata
9. Distinguish established external evidence from One-Wave hypotheses
10. Bring external findings back to exact repo claim and classify as support/contradiction/inconclusive
11. Do not claim any command/experiment/lookup ran without receipt/source
12. **Do not edit, commit, merge, push, or expose secrets**
13. Cite exact repo paths and external sources actually used
14. Return HOLD with exact missing reference/evidence if grounding cannot be completed

### Security Boundary

No changes to:
- Credential storage or handling
- Secret exposure prevention
- Hive Pipe MCP authentication
- Web relay authorization headers
- Git operations (commits are forbidden in the reference contract)

## End-to-End Testing Requirements

### Environment Prerequisites

1. **Jetson Device** (or equivalent local machine):
   - Ubuntu 20.04+ with systemd
   - Python 3.9+
   - git

2. **Hive Pipe MCP Gateway**:
   - Running on 127.0.0.1:8765
   - Authenticated with client tokens
   - Command support for: terminal_pwd, terminal_run, python_run

3. **DeepSeek Web Relay**:
   - Running on 192.168.55.100:3000 OR DEEPSEEK_WEB_BASE_URL
   - Requires Selenium/Firefox and logged-in DeepSeek session
   - Optional: separate from this repository

4. **Gemini Web Relay**:
   - Running on 192.168.55.100:3001 OR GEMINI_WEB_BASE_URL
   - Requires Firefox and logged-in Gemini session

### Test Procedure

```bash
# 1. Clone the feature branch
git clone -b feature/brain-buddy-no-limits-unlimited-dialogue \
  https://github.com/One-Wave-Universe/One-Wave-Science.git

# 2. Verify relays are accessible
curl http://192.168.55.100:3000/health
curl http://192.168.55.100:3001/health

# 3. Run a test discussion
cd One-Wave-Science
bash scripts/brain_buddy_council.sh discussion \
  "Explain the One-Wave hypothesis and its relationship to lattice mechanics" \
  --save

# 4. Results saved to:
External_Work/brain_buddy/outbox/council-discussion-YYYYMMDD-HHMMSS.md

# 5. Verify:
#    - Dialogue runs WITHOUT timeout interruptions
#    - Workers continue cycling (not stopping at first AGREEMENT)
#    - Transcript captures multi-round deliberation
#    - Reference contract enforced throughout
```

### Expected Output

```
===== GEMINI =====
[First response with tool calls and analysis]

===== DEEPSEEK =====
[Counter-response with separate tool calls]

===== GEMINI =====
[Round 2 refinement addressing DeepSeek]

===== DEEPSEEK =====
[Round 2 refinement addressing Gemini]

...continues until user /stop or natural termination...

Transcript receipt: External_Work/brain_buddy/outbox/council-discussion-20261001-235959.md
```

## Known Limitations

1. **Infrastructure Dependency**: Requires Jetson + relays (not part of this repo)
2. **Local Relay Setup**: DeepSeek/Gemini web relays must be manually configured
3. **Browser Session**: Relays require active authenticated browser sessions
4. **Token Management**: Hive Pipe tokens managed outside this repository

These are pre-existing constraints, not introduced by unlimited dialogue changes.

## Next Steps

1. **Deploy to Jetson** with hive-pipe gateway and web relays running
2. **Run end-to-end test** with `--save` to generate first working transcript
3. **Verify dialogue cycles** without timeouts (minimum 5 rounds recommended)
4. **Commit results** to feature branch as evidence
5. **Open PR** with test transcript attached
6. **Merge to main** once verification complete

## References

- **Commit:** 1967810 (feature/brain-buddy-no-limits-unlimited-dialogue)
- **Code Changes:** 3 files, 15+ modifications
- **Test Status:** 7/7 core tests passing
- **Reference Authority:** GENERAL_REFERENCE_RULES.md + AI_CANONICAL_START_HERE.md + I-06

---

**Verified:** 2026-10-01 by Claude (Test Suite)  
**Status:** Ready for deployment and end-to-end testing
