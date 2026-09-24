(function (global) {
  "use strict";

  const LEVELS = [
    { level: 1, name: "Action" },
    { level: 2, name: "Step" },
    { level: 3, name: "Layer" },
    { level: 4, name: "Build Phase" },
    { level: 5, name: "Project State" },
    { level: 6, name: "Project Loop" }
  ];

  function emptyProjectBuild() {
    return {
      currentLevel: 1,
      steps: {},
      journal: []
    };
  }

  function normalizeProjectBuild(input) {
    const base = emptyProjectBuild();
    const source = input && typeof input === "object" ? input : {};
    const currentLevel = Math.min(6, Math.max(1, Number(source.currentLevel) || 1));
    const steps = {};

    for (const item of LEVELS) {
      const raw = source.steps?.[item.level];
      if (!raw) continue;
      steps[item.level] = {
        level: item.level,
        name: item.name,
        goal: String(raw.goal || "").trim(),
        checklist: String(raw.checklist || "").trim(),
        result: String(raw.result || "").trim(),
        verified: raw.verified === true,
        checkpoint: String(raw.checkpoint || "").trim()
      };
    }

    return {
      currentLevel,
      steps,
      journal: Array.isArray(source.journal) ? source.journal : base.journal
    };
  }

  function cumulativeSteps(build, level) {
    const normalized = normalizeProjectBuild(build);
    const maxLevel = Math.min(6, Math.max(1, Number(level) || normalized.currentLevel));
    const result = [];
    for (let n = 1; n <= maxLevel; n += 1) {
      if (normalized.steps[n]) result.push(normalized.steps[n]);
    }
    return result;
  }

  function canEnterLevel(build, level) {
    const normalized = normalizeProjectBuild(build);
    const target = Math.min(6, Math.max(1, Number(level) || 1));
    if (target === 1) return true;
    for (let n = 1; n < target; n += 1) {
      if (!normalized.steps[n]?.verified) return false;
    }
    return true;
  }

  function saveLevel(build, level, fields) {
    const normalized = normalizeProjectBuild(build);
    const target = Math.min(6, Math.max(1, Number(level) || 1));
    if (!canEnterLevel(normalized, target)) {
      throw new Error("All previous Code by Law levels must be verified before this level can advance.");
    }

    normalized.steps[target] = {
      level: target,
      name: LEVELS[target - 1].name,
      goal: String(fields.goal || "").trim(),
      checklist: String(fields.checklist || "").trim(),
      result: String(fields.result || "").trim(),
      verified: fields.verified === true,
      checkpoint: String(fields.checkpoint || "").trim()
    };
    normalized.currentLevel = target;
    return normalized;
  }

  function addJournalEntry(build, entry) {
    const normalized = normalizeProjectBuild(build);
    normalized.journal.unshift({
      timestamp: new Date().toISOString(),
      level: Number(entry.level) || normalized.currentLevel,
      action: String(entry.action || "").trim(),
      result: String(entry.result || "").trim(),
      checker: String(entry.checker || "").trim(),
      checkpoint: String(entry.checkpoint || "").trim()
    });
    return normalized;
  }

  function compileProjectPacket(build) {
    const normalized = normalizeProjectBuild(build);
    const lines = [
      "CODE BY LAW — PROJECT BUILD REFERENCE",
      "Reference requirement: use this project build state and its journal together with the live repo/source reference before every step.",
      "Current level: " + normalized.currentLevel + " — " + LEVELS[normalized.currentLevel - 1].name,
      "Rule: every higher level contains the complete verified record of all previous levels."
    ];

    for (const step of cumulativeSteps(normalized, normalized.currentLevel)) {
      lines.push(
        "",
        "LEVEL " + step.level + " — " + step.name,
        "Goal: " + (step.goal || "UNSET"),
        "Checklist: " + (step.checklist || "UNSET"),
        "Result: " + (step.result || "PENDING"),
        "Verified: " + (step.verified ? "YES" : "NO"),
        "Checkpoint: " + (step.checkpoint || "NONE")
      );
    }

    if (normalized.journal.length) {
      lines.push("", "PROJECT JOURNAL HISTORY");
      for (const entry of normalized.journal.slice(0, 12)) {
        lines.push(
          "",
          "Journal — " + entry.timestamp,
          "Level: " + entry.level,
          "Action: " + (entry.action || "UNSET"),
          "Result: " + (entry.result || "UNSET"),
          "Checker: " + (entry.checker || "UNSET"),
          "Checkpoint: " + (entry.checkpoint || "NONE")
        );
      }
    } else {
      lines.push("", "PROJECT JOURNAL HISTORY", "No journal entries recorded — HOLD if prior project work is expected.");
    }

    return lines.join("\n");
  }

  global.CodeByLawProject = {
    LEVELS,
    emptyProjectBuild,
    normalizeProjectBuild,
    cumulativeSteps,
    canEnterLevel,
    saveLevel,
    addJournalEntry,
    compileProjectPacket
  };
})(globalThis);
