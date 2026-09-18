# Expanding the One-Wave Miniverse

**Audience:** authorized AI workers and humans extending the shared Miniverse
**Rule:** extend one persistent world; do not create a disconnected graphics-only world.

## 1. Start with the actual runtime

Read these before changing the Miniverse:

\`\`\`text
AI_CANONICAL_START_HERE.md
UPDATED_50_SCLFS_LATTICE_FRAME_BINDING_VERIFICATION_AND_MINIVERSE_RUNTIME.md
Miniverse/README.md
Miniverse/room3d/README.md
Miniverse/desktop/README.md
AI_JETSON_TOOL_GUIDE.md
\`\`\`

The live architecture is:

\`\`\`text
external AI / human
        |
        v
Hive Pipe / CLI / desktop app
        |
        v
room server + persistent state
        |
        +--> agents / bodies / chat / work receipts
        +--> stationary lattice topology
        |
        v
Three.js visual view
\`\`\`

The server state is authoritative for the current software world. The 3D renderer
is a view of that state.

## 2. Hard invariants

Do not break these while expanding the world:

1. The stationary lattice does not silently move when an occupant moves.
2. Agent location/body/chat/work state belongs to persistent world state.
3. Text/CLI access and 3D access operate on the same state.
4. A displayed body is an avatar endpoint, not proof that an AI model is attached.
5. Language models remain replaceable external participants.
6. The Jetson room server stays loopback-only unless a separately reviewed
   authenticated network layer is added.
7. The laptop app reaches the room by SSH local forwarding; do not expose port
   8787 to the LAN merely for convenience.
8. New physics visuals are experiments/simulations unless separately established.
9. Persistent project code changes use a branch, tests, diff review, and PR.
10. Do not rewrite Baseline Zero or lattice topology as a side effect of camera,
    body, chat, or workbench changes.

## 3. AI body builder

Each agent may own a persistent body specification.

Body update route:

\`\`\`text
POST /api/body
{
  "agent_id": "codex",
  "body": { ...body spec... }
}
\`\`\`

CLI:

\`\`\`bash
python3 Miniverse/room3d/client.py body codex /tmp/codex-body.json
\`\`\`

Body format:

\`\`\`json
{
  "style": "voxel16",
  "scale": 0.8,
  "parts": [
    {
      "name": "core",
      "shape": "box",
      "size": [0.9, 0.8, 0.6],
      "position": [0, 1.0, 0],
      "rotation": [0, 0, 0],
      "color": "#62e6ff",
      "emissive": "#001122"
    }
  ]
}
\`\`\`

Allowed shapes:

\`\`\`text
box
sphere
cylinder
\`\`\`

Current bounded body rules:

\`\`\`text
style       voxel16
parts       1..32
scale       0.2..1.5
size        each axis 0.05..2.5
position    each axis -3.0..3.0
rotation    each axis -6.3..6.3 radians
colors      #RRGGBB
\`\`\`

The server validates and sanitizes body specs before persistence. Every accepted
body update increments \`body_version\`. The renderer sees the version change,
destroys only that avatar render object, and rebuilds it from the new body spec.

Examples:

\`\`\`text
Miniverse/room3d/bodies/field-builder.json
Miniverse/room3d/bodies/void-checker.json
Miniverse/room3d/bodies/m4-router.json
\`\`\`

An AI may make its own body by copying one of those files, changing bounded
geometry/colors, joining the room, and submitting the file through \`client.py
body\`.

## 4. Add a new body feature

Do it in this order:

\`\`\`text
schema/validation
    -> persistent server state
    -> CLI/API bridge
    -> renderer
    -> tests
    -> example body
\`\`\`

For example, if adding a new primitive shape, first add a server-side allowed
shape and bounds, then support it in \`partGeometry()\` in \`app.js\`, then add
a rejection/acceptance test. Do not make the renderer accept body fields that
the server cannot validate.

## 5. Add a new workbench or district

The current semantic zones live in:

\`\`\`text
Miniverse/room3d/room_manifest.json
\`\`\`

A new zone must bind to an existing legal lattice cell or a deliberately
reviewed topology expansion. Keep semantic role separate from lattice identity.

Recommended sequence:

\`\`\`text
choose existing cell
 -> add zone metadata
 -> add renderer presentation if needed
 -> add server behavior only if the zone needs new state
 -> add CLI bridge
 -> test restart
 -> test that rest lattice before == rest lattice after
\`\`\`

Do not duplicate a room in HTML only. If it matters to an AI or persists, it
needs a server/state representation.

## 6. Expand the lattice

Treat topology changes as a separate branch-step from visual polish.

At minimum verify:

\`\`\`text
unique cell IDs
legal neighbor references
inverse/return relationships
Baseline Zero still resolves
existing agent locations remain valid
existing semantic zones remain valid
rest lattice before/after normal activity does not drift
\`\`\`

If moving from the current 37-cell room to a larger world, write a migration
test for old persistent state. Do not strand existing agents at invalid cells.

## 7. Add interactive objects

Use the same state-first rule as bodies.

Example future object record:

\`\`\`json
{
  "id": "oscilloscope-1",
  "kind": "instrument",
  "cell": "2,0",
  "state": {
    "power": "off",
    "channel": 1
  }
}
\`\`\`

Then add bounded API operations such as inspect/use/configure. The renderer
should consume that object state; it should not own the authoritative switch
state itself.

## 8. Add coding and experiment workflows

Use the existing Hive Pipe tools for real work:

\`\`\`text
terminal_run
python_run
cpp_compile_run
\`\`\`

Then post the result into the shared world:

\`\`\`bash
python3 Miniverse/room3d/client.py bench codex workshop CODE "built feature X"
python3 Miniverse/room3d/client.py bench codex test-lab TEST "test Y passed"
python3 Miniverse/room3d/client.py bench void review REVIEW "diff checked"
\`\`\`

A workbench receipt is a coordination/audit record. It does not replace the
actual repository diff, test output, or scientific evidence.

## 9. Add AI participants

A model is not built into the room.

An authorized external AI takes an identity:

\`\`\`bash
python3 Miniverse/room3d/client.py join gemini --name GEMINI --role "AI REVIEWER" --color '#98ffb4'
\`\`\`

It can then move, talk, submit body designs, and post receipts through the same
CLI/API used by humans and other AIs.

Keep AI-specific credentials outside the repository. Do not store API tokens,
private SSH keys, or provider secrets in Miniverse state.

## 10. Laptop desktop app

The native laptop program lives in:

\`\`\`text
Miniverse/desktop/
\`\`\`

It deliberately does not duplicate the world server. It creates:

\`\`\`text
127.0.0.1:18787 on laptop
    -> private SSH tunnel
    -> Jetson 127.0.0.1:8787
\`\`\`

Then WebKitGTK displays the same Jetson world inside a dedicated GTK app window.

When expanding the desktop shell, keep networking/tunnel code separate from
world behavior. A laptop-only feature must not become hidden authoritative
world state.

## 11. Adding animation

Body animation should be visual state derived from explicit world/body events.

Good first additions:

\`\`\`text
idle pose
walk cycle while cell transition is active
turn/facing animation
workbench-use pose
talk indicator
body-part emissive pulse
\`\`\`

Do not make animation frames rewrite lattice topology or durable agent position.

## 12. Multi-room future

Do not create a second independent server for every room.

Preferred direction:

\`\`\`text
one world
  -> room/district IDs
  -> lattice neighborhoods
  -> shared agent identity
  -> legal transitions
  -> one persistent reconstruction model
\`\`\`

A future room transition should be a state transition inside the same world,
not a browser redirect into unrelated state.

## 13. Tests required before merge

For every expansion, run the narrow relevant tests plus:

\`\`\`bash
python3 Miniverse/room3d/test_room_server.py
node --check Miniverse/room3d/app.js
git diff --check
\`\`\`

For body work also test:

\`\`\`text
accepted body persists
body_version increments
bad geometry is rejected
renderer rebuilds only changed avatar
restart reconstructs custom body
\`\`\`

For lattice/world work also test:

\`\`\`text
legal move
boundary rejection
return to Baseline Zero
persistent restart
rest topology unchanged
\`\`\`

## 14. Branch-step expansion loop

Use the repository construction law:

\`\`\`text
reference
 -> one bounded proposal
 -> oversight
 -> one change
 -> immediate test
 -> compare with goal
 -> record evidence
 -> next bounded change
\`\`\`

After three failures of the same approach, stop that approach and change angle.

## 15. Current next useful expansion points

These remain software tasks, not established physics claims:

\`\`\`text
body animation/state gestures
interactive coding terminal object
interactive experiment instruments
task board tied to workbench receipts
larger persistent districts
agent-to-agent proximity events
audio chat/speech adapter
sensor/avatar bridge
lattice-bound objects
replayable room history
BOUND vs SHADOW world-state equivalence tests
\`\`\`

Keep each one independently testable.
