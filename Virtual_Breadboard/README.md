# Virtual Breadboard Simulator

A real, from-scratch electronics breadboard simulator: a full-size 63-column
solderless breadboard rendered hole-by-hole, a palette of real parts
(resistors, LEDs, capacitors, a power supply, a switch, a potentiometer, and
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
- The breadboard's electrical grouping is modeled exactly like a real
  board: each column's five holes in the top bank (rows a-e) are one node,
  each column's five holes in the bottom bank (rows f-j) are a separate
  node, and the four power rails each run the full length as one node.
  Hovering any hole highlights every other hole that's electrically the
  same point — a good way to actually see how a breadboard is wired.

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

1. Pick a tool from the left palette (Jumper Wire, Resistor, LED,
   Capacitor, Power Supply, Switch, Potentiometer).
2. Click a hole on the board to start placing; click a second hole (a
   third for the potentiometer's wiper) to drop the part.
3. Switch to **Select / Toggle** to click a placed switch to open/close it,
   or click any part to inspect it — its live voltage, current, and an
   editable value dropdown appear in the right-hand Inspector, with a
   Delete button.
4. Hover any hole at any time to read its voltage and see every other hole
   sharing that electrical node highlighted.
5. The status bar along the bottom reports live warnings: short circuits,
   resistors dissipating more than their rating, LEDs that need a
   current-limiting resistor.
6. Try the **Example builds** in the sidebar (LED + resistor, RC charging
   with a switch, and a short-circuit danger demo) to see the physics in
   action immediately.
7. **Save** / **Load** keep a build in the browser's local storage;
   **Clear** wipes the board.

## Project layout

```
index.html          shell + layout
style.css            styling
js/circuit.js         circuit-physics engine (MNA solver, component models)
js/board.js           breadboard geometry, hole layout, hit-testing
js/components.js      part definitions, defaults, canvas drawing
js/app.js             toolbox, placement, simulation loop, UI wiring
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

Covers Ohm's law, LED forward conduction and reverse blocking, short-circuit
detection, over-current warnings, real RC charging curves, and switch
open/close behavior.
