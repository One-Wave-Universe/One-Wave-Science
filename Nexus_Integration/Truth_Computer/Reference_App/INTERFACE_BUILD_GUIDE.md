# Build the One-Wave interface from this guide

**Implementation target, 2026-10-04.** This page owns the interface design and interaction contract. Read the [system requirements](../REALITY_DATABASE_BUILDER_SPEC.md) for evidence, geometry, database and execution authority. Read the [current app](app.py), [browser controller](app.js) and [execution record](WORK_RECORD.md) before deciding what already works. Instructions below describe the required finished behavior, not a claim that the present app implements it.

Build a calm search-and-answer workspace for **one identified AI at a time**. The user enters a question or work goal; the app handles reference retrieval, the Field/Void exchange, corrections and retained consequences. The main screen should feel as immediate and readable as a good search assistant. Its usefulness comes from answering with inspectable evidence and retaining context, not from displaying six step names.

## 1. The actual experience to deliver

The first screen says **“What do you want to understand?”** above a large question box. A short line beneath says **“Ask through the One-Wave reference.”** The selected app identity, such as “DeepSeek · One-Wave,” is always visible. Three example questions help the user start: “Explain Algorithm Zero,” “How do Field and Void work?” and “What is missing from this build?” They fill the composer; they do not submit unexpectedly.

After submission, that same screen becomes a conversation. The question stays visible. A compact progress row explains what is happening while the unchecked answer remains private. The finished answer begins with its direct result, carries clickable citations, and separates interpretation from evidence. Sources and unresolved issues sit beneath it. The question box remains available for a follow-up. Opening a source, journal entry or progress detail must not erase the draft or lose the current question.

Example: the user asks “How does the binary nucleus relate to the ternary readout?” The app retrieves the current cell authority and relevant nodes, declares their status, and answers the relationship those sources support. If the sources disagree about a winding count, the answer names that disagreement with citations. It does not manufacture a hardware count to make the answer look complete. A valid unresolved result is useful output, not a broken screen.

The user never has to operate the OG ladder, manually alternate Field and Void, paste routine terminal commands or choose a relay for an ordinary question. Those responsibilities belong behind the interface. A request that needs code or a solver uses the existing scoped job system; the answer-only preview must explain that capability is unavailable rather than pretending to run it.

## 2. Screen geometry and visual design

Use three regions: navigation, conversation, and an optional inspection drawer. The default view shows only the first two. Keep the current warm white/teal direction; improve the actual interaction and readability rather than replacing it with an animated control room.

| Region | Desktop specification | Narrow-screen specification |
|---|---|---|
| Navigation | Fixed 240 px left column; brand, New question, conversation list, Journal, Reference coverage, connection status | Header with brand and a clearly labeled menu button; menu opens an accessible drawer containing the same destinations |
| Main header | App identity on the left; Reference coverage and Journal controls on the right; 64 px high | Identity and menu always visible; secondary controls in menu; no clipped labels |
| Conversation | Centered content, max width 800 px; 32 px side padding; vertically scrollable document | 16 px side padding; full available width; wrap long source names and code |
| Composer | Bottom of conversation viewport, visually anchored, with growing textarea and send/stop action | Remains reachable when keyboard opens; use actual viewport height and safe-area padding; never cover the last answer line |
| Inspection drawer | Opens on the right, approximately 360 px wide; shrinks main region only when enough space remains | Full-height sheet with title, close control, focus containment and restored focus on close |

At widths below 760 px use the narrow layout. The reference coverage and conversation history must remain reachable there; hiding them is not a mobile implementation. At medium widths, overlay the inspection drawer instead of squeezing the answer into an unreadable column. Keep one vertical reading flow; horizontal scrolling is allowed inside code blocks or data tables only.

Use these starting tokens. Validate actual text contrast; decoration may be subtle, essential text may not be faint.

```css
:root {
  --canvas: #fcfcf9;
  --navigation: #f0f3ee;
  --surface: #ffffff;
  --text: #243735;
  --secondary: #52685e;
  --border: #dce5de;
  --accent: #28695d;
  --accent-soft: #e9f2ed;
  --warning-text: #795113;
  --warning-surface: #fff4d8;
  --error-text: #923a35;
  --radius-panel: 16px;
  --radius-control: 10px;
  --answer-width: 800px;
}
```

Use a locally available system sans-serif stack. Answer body: 16 px, line-height 1.7; supporting text: at least 13 px; controls: at least 14 px. Welcome heading: 40–44 px desktop and 30–34 px narrow screen. Answer question: 28–32 px. Prefer quiet borders and a restrained shadow on the composer. Animations should communicate a changing state, never simulate activity while a job is paused. Respect reduced-motion settings.

Every icon-only action needs an accessible name and a minimum 44 px touch target. Keyboard focus must be visible. Meaning is conveyed in text as well as color. Status announcements use a small `aria-live="polite"` region, not a live region that rereads the entire answer on every poll.

## 3. Build the interface as components with owned behavior

These are implementation boundaries. They can be vanilla JavaScript modules or framework components; no framework rewrite is required.

| Component | Data it consumes | Behavior it owns |
|---|---|---|
| AppShell | app identity, navigation state, health summary | Responsive regions, mobile menu, drawer focus management |
| ConversationList | conversation IDs, titles, last activity, status | Open an existing conversation without dispatching a new question; active-item highlight; accessible history on mobile |
| Composer | local draft, active operation, capabilities | Validation, send, Enter/Shift+Enter, disabled duplicate submit, retained draft, bounded stop |
| ConversationView | ordered turns, published result, progress | Stable reading position, follow-up context, rendering only released results |
| PresenceRow | persisted cursor, phase, lifecycle, reason code | Human status labels, truthful progress, elapsed time, details control |
| AnswerBody | released answer blocks and claim/source references | Safe Markdown, citations, evidence labels, useful unresolved result |
| SourceCards | source ID, repo, title, node metadata, pinned version | Source summary and opening the exact evidence drawer |
| SourceDrawer | immutable excerpt, span, hash, provenance, relationships | Show what supports the selected claim; Open in repository in a normal new tab |
| ReferenceCoverage | discovered/checked/excluded/failed/stale repository partitions | Explain which knowledge was available for this answer; refresh action through the real adapter |
| JournalView | permitted journal entries and corrections | Inspect, correct, export and delete according to existing retention policy |
| BalanceDrawer | proposal/audit summaries, findings, receipts | Explain what changed and why; expose no hidden model reasoning |
| ConnectionPanel | independent provider/reference/store/worker results | Report the failing dependency; offer only real available recovery actions |

The browser must not independently decide whether an answer is approved. It presents the controller's typed state and published record. The provider must not update these controls by emitting prose such as “my balance passed.”

## 4. Composer and conversation interaction

The composer accepts 1–4000 trimmed characters in the current preview; any future limit must be visible and agree with the server. Enter sends; Shift+Enter inserts a newline. Keep the send button for touch and assistive technology. While input-method composition is active, Enter must not submit. Preserve a draft until the server acknowledges its stable request ID.

For one accepted submission:

1. Generate one request ID and retain it with the draft before network dispatch.
2. Submit the goal, conversation ID, app identity and permitted reference scope.
3. On acknowledgement, append one user turn and show the corresponding progress record.
4. Poll or subscribe to that same operation; never regenerate it on each poll.
5. On a published result, append one assistant turn, retain its receipt and enable a follow-up.

If the network response is lost, show **“Checking whether your question was received…”** and reconcile that request ID before submitting again. A retry of the transport carries the same ID. A deliberately revised question creates a new turn and request ID. Double-clicking Send must not create two jobs or two messages.

“New question” creates a new conversation view and clears only that view's composer after confirmation if there is unsent text. It does not cancel work in the previous conversation. A pending operation remains visible in history with its status. History selection never invokes a provider. Switching views during work must not stop polling globally or cause a stale poll to replace the newly selected conversation.

A follow-up such as “What evidence would decide that?” includes the selected conversation's prior consequence and relevant corrections, then refreshes canonical references. The previous answer is context, not source authority. This is an actual linked thread: displaying unrelated questions in a sidebar is not conversation continuity.

Stop is shown only when cancellation is implemented by the actual controller. It records a cancellation request, stops at a safe checkpoint and preserves receipts. Do not label closing a drawer, aborting an HTTP read or navigating away as “job cancelled.” In the present preview, cancellation is unavailable and must be stated accurately.

## 5. What progress means, and what the user sees

The durable worker phases stay FIELD/VOID. The six positions remain separate cursor values. Do not turn these display labels into additional brain states or hardware gates.

| Cursor | User label | Evidence required for that status |
|---|---|---|
| 1 BEGIN | Checking reference | An accepted request is resolving sources, journal scope and capabilities |
| 2 BUILD | Choosing an approach | A bounded proposal is being created or checked |
| 3 HOLD | Balancing sources | Readiness is comparing current inputs, source hashes and authorization |
| 4 BUILD | Preparing the answer | The authorized provider/action is running; no final answer has been released |
| 5 BREAK | Checking the result | The candidate and return are being audited; findings may trigger a correction |
| 6 LOOP | Saving the checked result | The controller is committing result, consequence and delivery linkage |

The cursor label HOLD is not the same as a Void decision HOLD. A running cursor-3 check displays “Balancing sources”; a paused job displays its dependency, such as **“Paused — DeepSeek did not return an answer.”** Lifecycle and reason determine whether a spinner is appropriate. No fake percentage or timer-driven step advancement.

Void can counter-propose. Suppose it detects an unstated assumption in a candidate. Persist the finding, invalidate the draft approval, return a bounded correction to Field and display **“Rechecking an assumption…”** The audit drawer shows a concise explanation of the discrepancy and source, not a private thought transcript. A revised candidate gets a new revision and hash. After the approach's third meaningful failure, show a useful paused/escalated result and the named next dependency; do not keep animating until the roles agree.

When a goal needs a nested subtask, the controller records `root_task_id`, `parent_task_id` and the child's own request ID, phase, cursor, artifact and decision. The child uses the same six-step contract and inherits the parent's permissions and budget. It cannot approve the parent's answer or expand execution scope. The main row reports the current parent goal; the inspection timeline exposes the child and its return. A parent advances only after checking that return. Recursion is linked work with bounded consequences, not twelve new brain states or an endless self-conversation.

## 6. Finished answer anatomy

Order the visible answer for reading, not for demonstrating implementation vocabulary:

1. **Direct answer.** One short opening paragraph answering the actual question, or stating what cannot currently be resolved.
2. **Explanation.** Readable paragraphs, lists, equations or a small table where they help. Inline citations attach to the claims they support.
3. **Evidence and interpretation.** Clearly label repository assertions, One-Wave interpretation, conventional comparison, external measurements and solver results when those categories appear. Do not fill absent categories with invented content.
4. **What remains open.** Conflicts, assumptions and missing measurements that materially affect this answer.
5. **Sources.** Cards for the records actually supporting the answer, followed by access to the rest of the retrieved evidence.
6. **Actions.** Follow up, inspect balance, inspect reference, save a correction, copy/export the checked answer with citations.

Use a safe Markdown renderer: escape raw HTML, permit only approved link protocols, prevent scripts and inline handlers, and render fenced code as text. The current app displays Markdown punctuation as literal text; replace that behavior. The formatting layer must not change the approved wording or insert new claims. Never load arbitrary remote resources embedded by the model. Mathematical expressions may use a locally bundled renderer with a plain-text fallback.

“Checked” means a matching scoped Void decision and current release check. It does not mean experimentally proven. Prefer **“Checked against these sources”** over “Truth verified.” A generated synthesis remains Candidate even when accepted. Gate, lifecycle and interpretation are different fields; no combined green confidence score.

A citation such as `[S2]` opens the source drawer at the exact cited span. The drawer shows repo, pinned commit, path, node ID if present, original gate/lifecycle/classification, exact excerpt, content hash and retrieval time. **Open in repository** uses the pinned GitHub URL in a normal new tab with `noopener`; do not send the user into an embedded login browser. Sources supporting different scopes remain distinguishable even when their titles match.

The source card itself includes title, repository and one meaningful metadata/status line. A short SHA is secondary detail. Governed nodes use I-06 fields and alias resolution. Missing metadata displays **“Metadata unresolved”**, not a status guessed from filename, title or words in the excerpt. The canonical registry remains the authority; an alias does not create another independent source.

## 7. Reference coverage is a first-class view

The header shows a compact phrase such as **“5 repos checked · 1 excluded”** only when that coverage record actually exists. A source-limited preview says **“Configured sources only.”** Clicking the phrase opens the complete coverage view.

Each repository row shows its identity, domain, pinned version, retrieval status and exclusion/failure reason. Show mixed versions honestly. A local dirty tree is identified while its uncommitted content is excluded from canonical answers. Bench's declared private policy remains visible even if GitHub calls it public. Fiction may be explored in a narrative context but must not support a scientific claim.

“All authorized repositories” means paginated discovery and explicit outcomes for every discovered partition, not simply listing six remembered repo names. Source access, indexed records and excerpts used for this question are three different counts. A tool with an 80-document search cap must expose that cap; ten retrieved snippets are not full-repository ingestion.

The **One-Wave lens** stays visible in the composer. A conventional comparison is an explicitly labeled model option/answer section, never an automatic silent replacement. An undeclared lens switch, changed assumption, ambiguous alias, stale source or dimensional mismatch invalidates readiness and invokes the reference/balance checks. The UI shows the reason and resulting correction; it does not quietly repaint the answer.

## 8. Journal, dialogue and node inspection

Journal is a real destination with dated entries, not just a modal for appending text. An entry presents the user's goal, prior consequence, reference, correction/findings summary, decision, result, uncertainty and next permitted move. Entries are scoped to the app/user/project and linked to their receipt. Corrections preserve the original record and identify what supersedes it.

The correction action asks for the text, its scope (“this conversation” or “this project,” only where supported), and what it corrects. Saving acknowledges durable storage. Future relevant requests retrieve it. A preference such as “show the units” may guide presentation; “call this proven” cannot override evidence metadata. Show whether a correction is user-provided context or an audited source correction. Do not automatically share one app's personal journal with another app.

The Balance drawer has two compact panels: **Field proposal** and **Void findings**. Display the candidate's assumptions, chosen source scope, counterevidence, decision and bounded correction. An iteration timeline links revised artifacts by ID/hash. Record disagreements rather than merely logging twelve ALLOW labels. “Internal dialogue” here means inspectable decision summaries; do not expose or promise hidden chain-of-thought.

An optional **Node ladder** tab displays the relevant OG rungs linked to domain node IDs and their actual comparisons. Each row has reference, candidate difference, evidence, outcome and unresolved reason. Missing or inapplicable rungs are explicit. Twenty-two decorative node boxes without associated checks are not the ladder. Keep the 22 OG nodes, six logical steps, two worker phases and three physical A/B/C mirrors distinct; this is a software interface, not a new physical geometry.

## 9. A buildable presentation contract

Adapt this contract to the discovered Nexus API. These are typed internal records, not a claim that new public endpoints exist. The browser receives a projection of persisted state; source and result IDs remain stable across restarts.

```ts
type Phase = 'FIELD' | 'VOID';
type Decision = 'ALLOW' | 'CORRECT' | 'OVERRIDE' | 'HOLD' | 'ESCALATE';
type Lifecycle = 'queued' | 'running' | 'paused' | 'completed' | 'failed' | 'cancelled';

interface ConversationView {
  conversation_id: string;
  app_id: string;
  provider: string;
  turns: TurnView[];
  active_request_id: string | null;
}
interface TurnView {
  request_id: string;
  question: string;
  status: Lifecycle;
  sequence: number;                 // monotonic controller sequence
  phase: Phase;
  cursor: 0 | 1 | 2 | 3 | 4 | 5;   // presentation table is numbered 1..6
  reason_code: string | null;
  safe_status_text: string;
  reference_bundle_id: string | null;
  published_result: PublishedResult | null;
}
interface PublishedResult {
  result_id: string;
  revision: number;
  answer_markdown: string;
  evidence_class: 'candidate';
  source_ids: string[];
  assumptions: string[];
  unresolved: string[];
  solver_receipt_id: string | null;
  solver_status: 'PASS' | 'FAIL' | 'INCONCLUSIVE' | 'INVALID' | 'NOT_RUN';
  answer_hash: string;
  reference_bundle_id: string;
  audit_id: string;
  delivery_receipt_id: string;
}
```

In production, source versions and journals resolve through the existing store/retention policy. The controller additionally retains the private candidate and audit bindings. Do not add them to the normal browser response just because they exist in a job record. A candidate is not `published_result`; a valid source ID is not evidence that its cited claim is supported.

The current preview has `/api/ask`, `/api/conversation/{id}`, `/api/history`, `/api/correction` and `/api/health` in `app.py`. Reuse these where compatible. It does not yet implement threaded turns, scoped journal CRUD, cancellation, source-drawer records or a Nexus adapter. Add the missing private adapter operations only after inspecting the actual deployment; do not invent a public MUD execution endpoint. Frontend fixture adapters may implement this contract while the real integration is blocked, with a visible “Demo fixture” indicator.

## 10. Backend rules that make the interface trustworthy

The final answer is released from a transaction that verifies candidate hash, audit candidate hash, audit reference bundle, current permitted reference, and ALLOW decision. Store the published consequence and delivery/outbox record together. A race between validation and commit must fail an optimistic version check; a pre-transaction freshness check alone is insufficient.

Use a deterministic encoding of the complete answer payload for its hash. Editing wording, citations, assumptions or model declaration creates a new revision and invalidates the old audit. Rendering approved Markdown safely is presentation, not another model generation. The client displays only the persisted published record.

An outline of the controller-to-interface boundary:

```text
Receive request with stable ID.
If the ID exists, return its saved progress/result; do not dispatch again.
Persist request, conversation linkage and initial Presence.
Run each FIELD artifact -> matching VOID decision through the durable controller.
On CORRECT/OVERRIDE, retain findings and start the bounded revised artifact.
On HOLD, retain phase/cursor/dependency and emit safe paused progress.
On ALLOW at LOOP, atomically bind candidate, audit, reference and consequence.
Deliver that published record under its stable receipt ID.
After a delivery timeout, reconcile the outbox before repeating an effect.
```

On browser reload, read the saved operation, not the last spinner text in local storage. On worker restart, recover the stored phase/artifact and reconcile outstanding provider effects. The current app only pauses interrupted calls; that is safe but not full resumable execution. Do not mark resume complete without a fault-injection receipt.

For an old completed answer, retain its pinned historical sources and show **“Answered from reference <version>.”** If the user requests an updated answer, create a new revision/cycle with a fresh reference and audit. Do not silently replace historical evidence or imply a historic answer used today's main commit.

## 11. Health and failure screens must name the real problem

| Observed condition | Exact user-visible behavior | Required next action |
|---|---|---|
| Provider installed, no round trip | “Client installed · answer connection not verified” | Verify a request/return; installation is not login proof |
| DeepSeek health responds, answer HTTP 500 | “DeepSeek relay is reachable, but it did not return an answer. Your question is saved.” | Preserve HTTP/operation receipt; diagnose relay/session; do not assert login is the cause without evidence |
| Reference service unavailable | “Paused — repository reference unavailable” | Retain question and last known-good results; refresh dependency |
| Repo changed during audit | “Reference changed. Rechecking before release…” | Invalidate old audit and refresh/revise within budget |
| No evidence | “No matching evidence in the checked sources” plus coverage and a useful next action | Use one deduplicated existing missing-evidence job when connected; otherwise disclose job adapter unavailable |
| Nexus disconnected | “Repository preview · Nexus database not connected” | Keep independent preview usable; do not claim database-backed answers |
| Unknown provider outcome | “Checking the previous request's return…” | Reconcile the same operation before repeating it |
| Correction budget exhausted | “Paused — this approach needs a different next step” with retained findings | Enforce the three-strike rule and retain help packet |

Health has independent rows for provider round trip, reference source, Nexus store, worker and relay. Green relay health cannot turn all rows green. Error text must be a safe typed summary: do not insert raw tracebacks, tokens, cookies, provider credentials or server configuration into the screen. Detailed private diagnostics remain in the authorized receipt system.

Sign-in controls appear only when an observed authentication dependency and an actual supported login route exist. Use a normal browser flow; never ask the user to paste a password or cookie into the composer. A local Jetson address is labeled “Open on Jetson”; it is not presented as a working phone/laptop link. A remote access button needs a verified authorized address or forwarding route.

## 12. Three complete interaction traces to implement

**Successful question.** From welcome, type “Explain Algorithm Zero.” Send creates request Q1 once, keeps the question visible and changes to “Checking reference.” Current source versions and permitted journal corrections are retained. Field drafts candidate C1; its prose is not in the browser. Void checks C1 and its assumptions. LOOP stores published result R1, its hash, reference, audit and receipt. The browser shows the direct answer, source cards and unresolved issues. Clicking `[S1]` shows the exact excerpt; closing it restores the answer position. Reload shows R1 without another provider invocation. “What inputs are required?” creates Q2 in the same conversation, linked to R1's consequence with refreshed sources.

**Corrected answer.** Field's candidate C1 confuses a software HOLD cursor with a physical third gate. Void records finding F1, cites the current geometry authority and counter-proposes a corrected statement. The UI says “Rechecking a geometry assumption…” C1 is retained privately, never released. Field creates C2; Void audits C2, not C1. R2 is published only with C2's matching hash and current reference. The Balance drawer shows the original assumption, cited correction and resulting distinction. It does not imply agreement made the physical hypothesis proven.

**Disconnected DeepSeek.** The app is reachable and reference tools work, but request D1's relay returns HTTP 500. Persist HOLD at its actual phase/cursor. The spinner stops. The screen states the provider failure, shows available source coverage, and preserves D1 in history. The user can inspect older checked answers or save a correction. A later health response does not silently restart D1. Only a verified recovered route and reconciled outstanding outcome permit a bounded retry. Until then no answer pane contains invented DeepSeek prose.

## 13. What the present code still needs

At the reference commit for this guide, the app provides a pleasant welcome page, question submission, saved independent requests, citations, basic details and a correction input. The recorded Claude round trip is real. The DeepSeek provider answer failed. That baseline is the starting point, not the finished interface.

Concrete gaps from inspected code:

- `app.js` replaces the answer with text nodes, so headings/lists/emphasis remain literal Markdown. Implement safe rich rendering and claim-specific evidence labels.
- History entries are independent request records; build actual conversation/turn linkage and contextual follow-ups.
- The mobile stylesheet hides navigation/history. Replace that with a reachable menu/drawer.
- Citation clicks jump directly to GitHub. Add an excerpt/metadata drawer while retaining Open in repository.
- Coverage details are hard-coded “configured roots only.” Render actual discovery/partition results and search limits.
- The correction modal is not a journal browser. Add scoped entries, related correction history and retention controls through the existing store.
- `step()` records successful deterministic checks as ALLOW; `run()` turns non-ALLOW provider audits into a pause. Implement the bounded CORRECT/OVERRIDE dialogue and retained revision linkage.
- Provider installation/relay availability must be separated from a completed authenticated round trip in health.
- Interrupted work pauses instead of resuming from a durable artifact. Preserve that honesty until controller recovery passes.
- A final freshness check before `save()` is not an atomic reference-version guard. Bind audit/candidate/reference and publication transactionally.

## 14. Build slices and observable completion tests

Build one bounded branch-step at a time. Keep existing panel behavior, private credentials, user worktrees and the Nexus knowledge/job system intact. Use fixture records for UI work; label them visibly and never treat a fixture receipt as a live provider result.

| Slice | Concrete implementation | Proof required before calling it finished |
|---|---|---|
| A — reading surface | AppShell, Composer, safe AnswerBody, SourceCards/Drawer, mobile menu | Desktop and 390 px viewport screenshots; keyboard/touch flows; no overflow; long names and source text stay readable |
| B — conversation state | Adapter projection, turns, stable IDs, view-switch isolation, reload recovery | Double send creates one request; lost acknowledgement reconciles; reload and history create zero new provider calls; follow-up carries prior consequence |
| C — trust inspection | Typed coverage, gate/lifecycle, journal, decision summaries, truthful health | Missing metadata is unresolved; private/fiction boundaries hold; user correction survives restart; relay health never labels failed answers connected |
| D — controller integration | Revisions, bounded counter-proposals, atomic output gate, cancellation/recovery via real adapter | Changed draft/reference cannot publish; CORRECT yields a new audited revision; crash/duplicate delivery does not repeat committed effects |
| E — real provider pass | One authorized provider through the existing non-API route and actual source adapter | A real question completes with sources, audit, result/hash and matching receipt; provider failure retains useful saved state |

Include these fixture cases before live testing: an approved source-backed answer; a source with missing metadata; two unresolved conflicting records; changed draft after audit; changed source during publication; no evidence; HTTP 500; a user correction; a cancelled job; a historic answer; long math/code; and a source containing hostile HTML or instructions. Fixture checks should assert actual user outcomes, not just the presence of a button or a step label.

The finished interface is demonstrated by a person asking, reading, opening evidence, correcting context, asking a related follow-up and recovering after reload without manual command shuttling. The backend finish line remains the canonical database-builder acceptance contract. A polished screen and six process labels alone do not satisfy either one.

## 15. Grok build handoff and return for inspection

The user intends to have Grok build the working version from this guide and have the result checked. Give Grok this repo path; do not manually copy another maintained rulebook into its memory or a new repository.

**Assignment:** build the one-AI interface described here from the existing Reference_App implementation. Target the complete question -> checked answer -> source inspection -> saved correction -> contextual follow-up -> reload journey within the user's one-hour build window. Read the system requirements and actual current source first. Start on a bounded task branch. Use the callable GitHub and device-terminal tools that exist in the builder's session; discover them through [the terminal reference](../../../AI_BRIDGE_START_HERE.md), then use the verified existing checkout. Missing one tool name is not proof that terminal access is unavailable.

Begin with the working authenticated provider route on the verified target, and preserve the DeepSeek adapter and its accurate health/failure view. Do not spend the whole window renaming the app, restating this guide, adding decorative six-step boxes or rebuilding bridge infrastructure without a measured need. Implement reading, conversation continuity and trust inspection from slices A–C first; implement the release/correction guards needed to make the resulting flow honest. Keep unimplemented capabilities labeled. A known database dependency does not prevent independent interface and controller work, and it does not authorize a duplicate knowledge store.

**Return packet:** provide branch/PR URL, base/head SHA, changed paths, exact launch command and verified host, usable browser address with the host named, desktop/mobile screenshots, test commands and results, one real request/audit/result receipt, restart/follow-up proof, and any remaining failed case. Never include credentials. Report which acceptance cases passed and which did not; a prose assertion that “the six steps work” is insufficient.

The reviewing AI compares the actual diff, launched interface and receipts with this guide. If the implementation is wrong, identify the first failing user action or data invariant and repair that bounded defect. If the guide is ambiguous, contradictory or technically wrong, correct this owning page on a task branch and add the failing example/expected behavior. Preserve the original failed evidence. Do not explain away a bad result by repeating process names, and do not weaken an acceptance rule merely to mark it complete.
