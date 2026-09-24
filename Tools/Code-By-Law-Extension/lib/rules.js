(function (global) {
  "use strict";

  function normalizeRule(rule) {
    return {
      id: String(rule.id || "").trim(),
      title: String(rule.title || "Untitled rule").trim(),
      phase: String(rule.phase || "GENERAL").trim().toUpperCase(),
      priority: Number.isFinite(Number(rule.priority)) ? Number(rule.priority) : 100,
      enabled: rule.enabled !== false,
      text: String(rule.text || "").trim()
    };
  }

  function mergeRules(defaultRules, customRules) {
    const byId = new Map();
    for (const rule of defaultRules || []) {
      const normalized = normalizeRule(rule);
      if (normalized.id) byId.set(normalized.id, normalized);
    }
    for (const rule of customRules || []) {
      const normalized = normalizeRule(rule);
      if (normalized.id) byId.set(normalized.id, normalized);
    }
    return [...byId.values()]
      .filter((rule) => rule.enabled && rule.text)
      .sort((a, b) => a.priority - b.priority || a.title.localeCompare(b.title));
  }

  function compileRules(rules, projectContext) {
    const lines = [
      "CODE BY LAW — GOVERNED TURN",
      "",
      "Follow the Code by Law cycle in order: Think Before You Speak, Parser Goblin, Reference Every Step, Project Build Step + Checklist, Bouncer Goblin, act, Checker Goblin, Journal Entry, checkpoint, then re-reference."
    ];

    if (projectContext && String(projectContext).trim()) {
      lines.push("", "CURRENT PROJECT CONTEXT", String(projectContext).trim());
    }

    for (const rule of rules || []) {
      lines.push("", "[" + rule.phase + "] " + rule.title, rule.text);
    }

    lines.push(
      "",
      "REQUIRED RESPONSE BEHAVIOR",
      "Follow Code by Law: think before speaking; parse the exact task; reference before every step; work only the current project build step and checklist; require Bouncer approval before advancing; use authorized tools directly when needed; verify with the Checker; write the journal entry; checkpoint; then re-reference before the next step."
    );
    return lines.join("\n");
  }

  global.CodeByLawRules = { normalizeRule, mergeRules, compileRules };
})(globalThis);
