(() => {
  "use strict";

  async function loadState() {
    const defaults = await fetch(chrome.runtime.getURL("rules/default-rules.json")).then((r) => r.json());
    const stored = await chrome.storage.local.get([
      "customRules", "projectContext", "projectBuild",
      "githubRepo", "githubBranch", "referencePaths"
    ]);
    return {
      rules: CodeByLawRules.mergeRules(defaults, stored.customRules || []),
      projectContext: stored.projectContext || "",
      projectBuild: CodeByLawProject.normalizeProjectBuild(stored.projectBuild),
      githubRepo: stored.githubRepo || "",
      githubBranch: stored.githubBranch || "main",
      referencePaths: stored.referencePaths || ""
    };
  }

  async function loadGitHubReference() {
    try {
      const result = await chrome.runtime.sendMessage({ type: "CBL_GET_GITHUB_REFERENCE" });
      if (!result?.ok) throw new Error(result?.error || "GitHub reference failed");
      return { ok: true, data: result.data };
    } catch (error) {
      return {
        ok: false,
        data: { state: "HOLD", error: error.message, files: [] }
      };
    }
  }

  function formatGitHubReference(ref) {
    const lines = [
      "CODE BY LAW — GITHUB REFERENCE",
      "State: " + (ref.state || "HOLD"),
      "Repo: " + (ref.repo || "unknown"),
      "Branch: " + (ref.branch || "unknown"),
      "HEAD: " + (ref.head || "unknown"),
      "Rule: GitHub is the external source of truth. Before every project action, compare this reference with the cumulative project build and journal. Use the chatbot's authorized GitHub access for repository reads/writes; do not invent repo state."
    ];

    if (ref.error) lines.push("Reference error: " + ref.error);

    for (const file of ref.files || []) {
      lines.push("", "REFERENCE FILE: " + file.path);
      if (!file.present) {
        lines.push("MISSING — Bouncer HOLD if this file is required for the current step.");
      } else {
        lines.push(file.text);
      }
    }

    return lines.join("\n");
  }

  function findEditor() {
    return [...document.querySelectorAll("textarea, [contenteditable='true']")]
      .filter((el) => {
        const rect = el.getBoundingClientRect();
        return rect.width > 80 && rect.height > 20 && !el.disabled;
      })
      .at(-1) || null;
  }

  function setEditorText(editor, text) {
    if (!editor) return false;
    if ("value" in editor) {
      const proto = Object.getPrototypeOf(editor);
      const setter = Object.getOwnPropertyDescriptor(proto, "value")?.set;
      if (setter) setter.call(editor, text);
      else editor.value = text;
      editor.dispatchEvent(new Event("input", { bubbles: true }));
      editor.focus();
      return true;
    }
    editor.focus();
    editor.textContent = text;
    editor.dispatchEvent(new InputEvent("input", {
      bubbles: true,
      inputType: "insertText",
      data: text
    }));
    return true;
  }

  async function injectGovernedTurn() {
    const editor = findEditor();
    if (!editor) return { ok: false, reason: "No editable chat box found." };

    const state = await loadState();
    const github = await loadGitHubReference();
    const lawPacket = CodeByLawRules.compileRules(state.rules, state.projectContext);
    const projectPacket = CodeByLawProject.compileProjectPacket(state.projectBuild);
    const githubPacket = formatGitHubReference(github.data);
    const packet = lawPacket + "\n\n" + githubPacket + "\n\n" + projectPacket;

    const existing = String(editor.value ?? editor.textContent ?? "").trim();
    const combined = existing
      ? packet + "\n\nUSER TASK\n" + existing
      : packet + "\n\nUSER TASK\n";

    return setEditorText(editor, combined)
      ? { ok: true, liveReference: github.ok }
      : { ok: false, reason: "Could not write to the chat box." };
  }

  chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
    if (message?.type === "CBL_INJECT") {
      injectGovernedTurn().then(sendResponse);
      return true;
    }
  });

  const badge = document.createElement("button");
  badge.id = "cbl-badge";
  badge.type = "button";
  badge.textContent = "Code by Law";
  badge.title = "Inject Code by Law + GitHub project reference";
  badge.addEventListener("click", async () => {
    const result = await injectGovernedTurn();
    badge.textContent = result.ok
      ? (result.liveReference ? "Law + GitHub ✓" : "Law loaded / ref HOLD")
      : "No chat box";
    setTimeout(() => { badge.textContent = "Code by Law"; }, 1800);
  });

  document.documentElement.appendChild(badge);
})();
