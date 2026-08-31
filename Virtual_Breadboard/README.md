# Virtual Breadboard Simulator

A real, from-scratch electronics breadboard simulator: a full-size 63-column
solderless breadboard rendered hole-by-hole, a palette of real parts
(resistors, LEDs, diodes, capacitors, a power supply, a switch, a momentary
pushbutton, a real 6-pin potentiometer, a virtual-ground rail splitter, and
jumper wires), and a live circuit-physics engine underneath — not a toy
animation. Click any hole to wire something into it, and the simulator
solves the actual circuit every frame.

## What makes the physics "real"

The engine (`js/circuit.js`) uses **Modified Nodal Analysis** — the same
linear-algebra method SPICE-class simulators use:

- **Ohm's Law + Kirchhoff's Current Law** for every resistor and node.
- **LEDs** use the standard "constant voltage drop" large-signal diode
  model: below the forward voltage they're an open circuit; above it,
  they conduct through a small series resistance. Wire one backwards and
  it correctly stays dark. Skip the resistor and it correctly warns you
  the LED will draw dangerous current.
- **Capacitors** use a backward-Euler companion model, so they actually
  charge and discharge over real time — hook one to a battery through a
  resistor and watch it climb toward the supply voltage on the real `RC`
  time constant, live, frame by frame.
- **Batteries** have a small internal resistance (like a real cell or bench
  supply), so shorting one out gives a large but finite current — and the
  simulator flags it as a short circuit instead of silently doing nothing.
- **Diodes** are the same one-way-conduction model as LEDs (just a different
  forward voltage, ~0.7V, and no glow) — a shared `forwardVoltage()`/
  `forwardRon()` pair in `circuit.js` drives both.
- **Switches and pushbuttons** both close a node when `closed` is true; a
  pushbutton is just momentary — held closed only while the mouse/finger is
  down, both on the board and in the Inspector.
- **Potentiometers** are modeled as a real 6-pin trimmer: 3 legs in one
  terminal-strip row, 3 mirrored legs in the corresponding row of the other
  bank (straddling the center channel, always exactly 5 rows apart — e.g.
  row `c` mirrors to row `h`). Electrically the mirrored legs are just wired
  to their partners (a real trimmer's two rows are joined internally for
  mechanical stability), modeled as three ordinary jumper connections rather
  than touching the resistor-divider math itself. In Select mode, click and
  drag the knob directly on the canvas to turn it (a 270-degree sweep, like
  a real trimmer), or use the Inspector's slider — it moves in 0.1% steps
  (1000 positions) rather than a coarse 1%, fine enough to dial in a
  specific millivolt-scale lean for asymmetric-voltage testing.
- **Virtual Ground** is a rail-splitter: a 3-terminal part whose output node
  is forced to the exact midpoint voltage between the two rails/nodes it's
  connected to — e.g. split a single 9V supply into a `+4.5V` / `V0 (0V
  reference)` / `-4.5V` bipolar rail set, the way a real op-amp voltage-
  divider "virtual ground" buffer does. It's modeled as its own ideal
  constraint in the MNA solver (an extra equation forcing `V(out) =
  (V(A)+V(B))/2`) through a small internal resistance, the same technique
  used for the battery's ideal-voltage-source row — not just a resistor
  divider, so it holds the midpoint under load instead of sagging.
- The breadboard's electrical grouping is modeled exactly like a real
  board: each column's five holes in the top bank (rows a-e) are one node,
  each column's five holes in the bottom bank (rows f-j) are a separate
  node, and the four power rails each run the full length as one node.
  Hovering any hole highlights every other hole that's electrically the
  same point — a good way to actually see how a breadboard is wired.
  Hovering a placed part fades it to see-through and rings its occupied
  holes in blue, so you can still target a hole hidden under a component's
  body; hovering with a placement tool active also rings the hole it'll
  snap to next.

This is deliberately a simplified analog model (piecewise-linear diodes,
not a full Shockley exponential; no AC/frequency analysis) — accurate
enough to design and debug real low-voltage hobby circuits, not a
replacement for SPICE on precision analog design.

## Running it

**Zero-install, in any browser (including on Ubuntu):**

```bash
xdg-open index.html
# or serve it locally:
python3 -m http.server 8000   # then open http://localhost:8000
```

Everything is plain HTML/CSS/JS with no build step and no external
dependencies — it works fully offline.

**As a downloadable desktop app for Ubuntu (Electron + AppImage):**

```bash
npm install
npm start              # run it as a desktop app directly

npm run dist:appimage  # build dist/Virtual Breadboard Simulator-*.AppImage
# or
npm run dist:deb       # build a .deb package
```

The AppImage is a single portable executable — `chmod +x` it and
double-click (or run it) on any Ubuntu machine, no installation required.

**To add a proper desktop/app-menu shortcut** (an AppImage on its own
doesn't register one):

```bash
./install-linux.sh /path/to/VirtualBreadboardSimulator.AppImage
```

This copies the AppImage to `~/.local/bin/`, installs `icon.svg` to
`~/.local/share/icons/`, and writes a `.desktop` entry to
`~/.local/share/applications/` (and to `~/Desktop/` if you have one) —
all per-user, no `sudo` needed. Afterwards, "Virtual Breadboard Simulator"
shows up in your applications menu/launcher with its own icon, and if you
have a Desktop folder, a matching icon appears there too (GNOME may mark it
untrusted the first time — right-click it and choose "Allow Launching").
Run the script with no arguments and it will look for the AppImage next to
itself or in `~/Downloads` automatically.

**As a downloadable Android app:**

`android/VirtualBreadboardSimulator.apk` is a real, signed APK — install it
by copying it to an Android phone/tablet and opening it (you'll need to
allow "install unknown apps" for whatever app you used to open it, since
it isn't from the Play Store). It's a native app with a single Activity
that hosts a `WebView` loading the same `index.html`/`js` bundled into its
assets, so it runs fully offline — no native runtime bundled, so it's only
~29KB.

To rebuild it after changing the web app:

```bash
sudo apt-get install --no-install-recommends \
  aapt zipalign apksigner android-sdk-platform-23 libsmali-java
cd android
./build-apk.sh   # -> android/build/VirtualBreadboardSimulator.apk
```

This build path deliberately avoids Android Studio/Gradle and Google's SDK
downloads entirely — it uses only `aapt` (manifest + asset packaging),
`smali` (assembles `smali/.../MainActivity.smali`, a hand-written Dalvik
bytecode equivalent of `src/.../MainActivity.java`, into `classes.dex`),
`zipalign`, and `apksigner`, all available from Ubuntu/Debian's own apt
repos. If you have Android Studio, it's simpler to just create a new
project, drop `src/.../MainActivity.java` in, point its assets at this
folder's `index.html`/`style.css`/`js/`, and build normally — the smali
file exists only because this environment has no Java-to-Dalvik compiler
(`dx`/`d8`) packaged, and Google's own SDK servers weren't reachable to
fetch one.

## Using the simulator

1. Pick a tool from the left palette (Jumper Wire, Y-Split Wire, Resistor,
   LED, Diode, Capacitor, Power Supply, Switch, Pushbutton, Potentiometer,
   Virtual Ground).
2. Click a hole to start placing; click a second hole to drop most parts —
   the wire's other end snaps wherever you click next, so click the first
   hole then move to wherever you want the far end and click again.
   - The **Potentiometer** is different — it's a real 6-pin trimmer, so one
     click on an anchor hole (any strip row, not a rail) places all 6 legs,
     straddling the center channel automatically.
   - The **Y-Split Wire** is a standalone part bridging two rows, forked to
     2 holes at each end (a V/Y shape) — good for carrying a ground/rail
     node from 2 points on one side to 2 more points on the other, in one
     piece. Click 2 holes for one end's fork, then 2 holes for the other
     end's fork; all 4 holes end up as one electrical node.
   - **Virtual Ground** takes 3 clicks: 2 holes for the rails you want to
     split (e.g. a `+` and `-` power rail), then 1 hole for its `V0` output
     — that output always reads the exact midpoint voltage between the two
     rails, letting you breadboard a proper `-`/`0`/`+` split-supply layout
     from a single single-ended battery.
3. Switch to **Select / Toggle** to click a placed switch to open/close it,
   hold down a pushbutton to close it only while held, click and drag a
   potentiometer's knob to turn it, or click any part to inspect it — its
   live voltage, current, and an editable value dropdown appear in the
   right-hand Inspector, with a Delete button.
4. **Right-click any placed part** for a quick floating menu with the same
   options as the Inspector (value, color, style) plus **Remove part** —
   right-click a wire to pick its color or switch it between **Looped**
   (a flexible wire arcing up and over — the default) and **Flat** (a rigid
   pre-formed jumper lying straight against the board).
5. Hover any hole at any time to read its voltage and see every other hole
   sharing that electrical node highlighted. Hover a placed part to fade it
   see-through (with its occupied holes ringed in blue) so you can still
   reach a hole hidden under its body; with a placement tool active,
   hovering also rings the hole your next click will snap to.
6. The status bar along the bottom reports live warnings: short circuits,
   resistors dissipating more than their rating, LEDs that need a
   current-limiting resistor.
7. Try the **Example builds** in the sidebar (LED + resistor, RC charging
   with a switch, and a short-circuit danger demo) to see the physics in
   action immediately.
8. **Save** / **Load** keep a build in the browser's local storage;
   **Clear** wipes the board.

## Ask AI to build it

The right-hand panel has a dialogue box: describe a circuit in plain
English ("build a 9V circuit with a green LED and a current-limiting
resistor") and click **Build it**. Click **settings** above it first to
pick a provider and paste in your own API key:

- **Anthropic (Claude)** — calls the Messages API directly from the
  browser using Anthropic's documented `anthropic-dangerous-direct-browser-access`
  header (meant for exactly this: a client-side app with no backend).
- **OpenAI** — calls the Chat Completions API the same way.
- **Custom (OpenAI-compatible)** — any endpoint that speaks the same
  `POST { model, messages }` shape: a local Ollama/LM Studio server, a
  self-hosted proxy, another vendor. The endpoint must send CORS headers
  (`Access-Control-Allow-Origin`) since the request comes straight from
  the page — most local LLM servers do this by default.

Your key is stored only in this browser's local storage and sent only to
the provider you picked, directly from the page — it never passes through
anything else. Whatever the AI returns is checked against the board's real
rules (`js/ai.js`'s `validateSpec`) before anything is placed — bad row
names, wrong terminal counts, unknown part types, or invalid values are
rejected with a specific error instead of silently breaking the board. A
build that passes validation is applied through the exact same code path
as the hardcoded example presets (`applyPreset()`), so it's held to the
same live physics: a bad design still shows up as a short-circuit or
over-current warning in the status bar.

Adding another provider is one function in `js/ai.js`'s `PROVIDERS` map —
anything that can take a system prompt + user text and return text works.

Note: this only works in the real app (opened directly, the Ubuntu
AppImage, or the Android APK) — the in-chat Artifact preview's sandbox
blocks calls to external AI APIs, so the dialogue box won't be able to
reach a provider from there.

## Project layout

```
index.html          shell + layout
style.css            styling
js/circuit.js         circuit-physics engine (MNA solver, component models)
js/board.js           breadboard geometry, hole layout, hit-testing
js/components.js      part definitions, defaults, canvas drawing
js/app.js             toolbox, placement, simulation loop, UI wiring
js/ai.js               pluggable AI provider layer + circuit-spec validator
test/circuit.test.js  standalone physics tests (`npm test` / `node test/circuit.test.js`)
main.js               Electron desktop wrapper
package.json          npm scripts + electron-builder config for Linux
android/               native Android app (WebView wrapper around the same web app)
  AndroidManifest.xml
  src/.../MainActivity.java     canonical source
  smali/.../MainActivity.smali  hand-assembled equivalent (see android section above)
  build-apk.sh                  reproducible build script
  VirtualBreadboardSimulator.apk  the built, signed APK
```

## Running the physics tests

```bash
node test/circuit.test.js
```

Covers Ohm's law, LED/diode forward conduction and reverse blocking,
short-circuit detection, over-current warnings, real RC charging curves,
switch/pushbutton open-closed behavior, a Y-split wire tying 4 holes
(2 forked at each end) to one electrical node, and a virtual-ground rail
splitter holding its output at the exact midpoint of two rails, both
unloaded and loaded, for a symmetric and an asymmetric supply voltage.
