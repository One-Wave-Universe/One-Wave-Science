# Nexus Truth Computer Private Install

## Purpose

Install the One-Wave Truth Computer as a real Nexus panel without adding public file-write, code-execution, patch, or deployment commands to the MUD protocol.

The public `/join`, `/api/act`, job board, and station actions remain interaction channels only. Installation is a private filesystem operation inside the local Nexus repository, currently expected under `C:\Users\Scales\MirrorGate`, followed by human review and restart.

## Canonical architecture

- `OG-00` through `OG-21` are the fixed origin-to-beyond trace.
- `OG-13` through `OG-18` are the six active bidirectional wave gates.
- `21` is the recursive position count on one side.
- `42` is `21 Field + 21 Void` around the shared Mirror/Null reference `0`.
- Scale Invariance is a first-class chapter analysis, supported by nodes. It is not demoted to a lonely keyword result.
- Exact repository records, conventional observations, One-Wave interpretations, Yellow candidates, contradictions, and unknowns must remain visibly separate.

## Existing Nexus services to reuse

Do not create a second reality database or a second job system. Bind this panel to the existing Nexus capabilities:

1. Reality Database search, currently exposed through the `one-wave-reality` station search action.
2. Canonical node/definition opening, currently exposed through the station node-lookup action.
3. Durable job creation for missing subjects.
4. Saved run results under the existing run system.
5. Existing room and station navigation.

## Files in this package

- `og-system.json`: canonical Updated 41 OG spine and count distinctions.
- `truth-computer-core.js`: source classification, trace assembly, scale analysis, and truth-status separation.
- `truth-computer-panel.js`: browser panel mounted inside Nexus.
- `truth-computer.css`: scoped presentation styles.
- `acceptance-tests.md`: non-negotiable behavior tests.

## Required private adapter

The Nexus server or existing page must provide this object before mounting the panel:

```js
window.NEXUS_TRUTH_ADAPTER = {
  searchReality: async (query) => {
    // Return an array of repository/knowledge records.
    // Each record should include as many of these as available:
    // id, title, definition, text, sourcePath, kind, gate,
    // lifecycle, truthStatus, score, relationships.
  },
  openDefinition: async (record) => {
    // Open the existing canonical definition view.
  },
  createDescribeJob: async (query) => {
    // Use the existing durable job-board workflow.
    // Returned AI prose remains Candidate until supported by records.
  }
};
```

Do not expose adapter methods through the public MUD protocol as arbitrary write or execution commands.

## Mount

Add the assets to the private Nexus static bundle, then mount inside the Reality Database station or a `Truth Computer` tab:

```html
<link rel="stylesheet" href="/truth-computer/truth-computer.css">
<div id="truth-computer-root"></div>
<script src="/truth-computer/truth-computer-core.js"></script>
<script src="/truth-computer/truth-computer-panel.js"></script>
<script>
  NexusTruthComputer.mount({
    root: document.getElementById('truth-computer-root'),
    adapter: window.NEXUS_TRUTH_ADAPTER,
    ogUrl: '/truth-computer/og-system.json'
  });
</script>
```

## Answer contract

Every result must render these layers instead of one flat paragraph:

1. Stored definition and source status.
2. Feedback origin: `OG-00` through `OG-10`.
3. Awareness and Presence: `OG-11` and `OG-12`.
4. Active six-gate pass: `OG-13` through `OG-18`.
5. Emergence and Beyond: `OG-19` through `OG-21`.
6. Scale Invariance chapter analysis.
7. Contradictions, missing evidence, and unresolved questions.
8. Source records with canonical-definition controls.

## Import rule

Updated 41 is read from the private canonical repository or a generated read-only index. Never let a generated answer overwrite canonical source files. Knowledge jobs may append candidate records to the existing knowledge store, but promotion requires the normal audit and gate process.

## Health check

The Nexus panel is not complete until it reports:

```text
Truth Computer: active
Database: Updated 41 or newer
OG stages: 22
Active gates: 6
Field/Void geometry: 21 + 21 = 42 around 0
Scale chapter: available
Reality search adapter: connected
Definition adapter: connected
Job adapter: connected
Public deployment commands: absent
```
