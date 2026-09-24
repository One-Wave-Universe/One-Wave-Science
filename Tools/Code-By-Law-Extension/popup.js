"use strict";

const context = document.querySelector("#context");
const message = document.querySelector("#message");
const live = document.querySelector("#live");
const githubRepo = document.querySelector("#githubRepo");
const githubBranch = document.querySelector("#githubBranch");
const referencePaths = document.querySelector("#referencePaths");
const level = document.querySelector("#level");
const stepGoal = document.querySelector("#stepGoal");
const stepChecklist = document.querySelector("#stepChecklist");
const stepResult = document.querySelector("#stepResult");
const checkpoint = document.querySelector("#checkpoint");
const verified = document.querySelector("#verified");

let projectBuild = CodeByLawProject.emptyProjectBuild();

function fillLevel(levelNumber) {
  const n = Number(levelNumber) || 1;
  const step = projectBuild.steps?.[n] || {};
  level.value = String(n);
  stepGoal.value = step.goal || "";
  stepChecklist.value = step.checklist || "";
  stepResult.value = step.result || "";
  checkpoint.value = step.checkpoint || "";
  verified.checked = step.verified === true;
}

async function saveProjectState() {
  await chrome.storage.local.set({
    projectContext: context.value.trim(),
    projectBuild,
    githubRepo: githubRepo.value.trim(),
    githubBranch: githubBranch.value.trim() || "main",
    referencePaths: referencePaths.value.trim()
  });
}

async function refreshGitHubReference() {
  try {
    const result = await chrome.runtime.sendMessage({ type: "CBL_GET_GITHUB_REFERENCE" });
    if (!result?.ok) throw new Error(result?.error || "GitHub reference failed");
    const ref = result.data;
    const missing = (ref.files || []).filter((f) => !f.present).map((f) => f.path);
    live.textContent =
      "GitHub: " + ref.state +
      "\nRepo: " + ref.repo +
      "\nBranch: " + ref.branch +
      "\nHEAD: " + ref.head +
      (missing.length ? "\nMissing refs: " + missing.join(", ") : "\nBuild/journal refs: OK");
  } catch (error) {
    live.textContent = "GitHub reference: HOLD\n" + error.message;
  }
}

async function load() {
  const stored = await chrome.storage.local.get([
    "projectContext", "projectBuild", "githubRepo", "githubBranch", "referencePaths"
  ]);

  context.value = stored.projectContext || "";
  githubRepo.value = stored.githubRepo || "https://github.com/One-Wave-Universe/One-Wave-Science";
  githubBranch.value = stored.githubBranch || "main";
  referencePaths.value = stored.referencePaths ||
    "CURRENT_BUILD_ORDER.md\nAI_CURRENT_PROJECT_JOURNAL.md\nBRANCH_STEP_PROJECT_TEMPLATE.md";
  projectBuild = CodeByLawProject.normalizeProjectBuild(stored.projectBuild);
  fillLevel(projectBuild.currentLevel);
  await saveProjectState();
  await refreshGitHubReference();
}

level.addEventListener("change", () => {
  const target = Number(level.value);
  if (!CodeByLawProject.canEnterLevel(projectBuild, target)) {
    message.textContent = "Bouncer HOLD: verify all previous levels before entering this level.";
    fillLevel(projectBuild.currentLevel);
    return;
  }
  projectBuild.currentLevel = target;
  fillLevel(target);
});

document.querySelector("#saveStep").addEventListener("click", async () => {
  const target = Number(level.value);
  try {
    projectBuild = CodeByLawProject.saveLevel(projectBuild, target, {
      goal: stepGoal.value,
      checklist: stepChecklist.value,
      result: stepResult.value,
      checkpoint: checkpoint.value,
      verified: verified.checked
    });
    projectBuild = CodeByLawProject.addJournalEntry(projectBuild, {
      level: target,
      action: stepChecklist.value,
      result: stepResult.value,
      checker: verified.checked ? "ALLOW / verified" : "PENDING",
      checkpoint: checkpoint.value
    });
    await saveProjectState();
    message.textContent = "Level " + target + " saved with cumulative history and journal entry.";
  } catch (error) {
    message.textContent = "Bouncer HOLD: " + error.message;
  }
});

document.querySelector("#save").addEventListener("click", async () => {
  await saveProjectState();
  await refreshGitHubReference();
  message.textContent = "GitHub project reference saved.";
});

document.querySelector("#inject").addEventListener("click", async () => {
  await saveProjectState();
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) {
    message.textContent = "No active chat tab.";
    return;
  }
  try {
    const result = await chrome.tabs.sendMessage(tab.id, { type: "CBL_INJECT" });
    message.textContent = result?.ok ? "Code by Law loaded into the chat." : (result?.reason || "Could not inject.");
  } catch (_error) {
    message.textContent = "This page is not a supported coding chat yet.";
  }
});

document.querySelector("#rules").addEventListener("click", () => chrome.runtime.openOptionsPage());

load();
