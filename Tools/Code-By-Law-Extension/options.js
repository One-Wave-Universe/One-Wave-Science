"use strict";

const defaultsHost = document.querySelector("#defaults");
const customHost = document.querySelector("#custom");
const template = document.querySelector("#rule-template");
const message = document.querySelector("#message");

let defaultRules = [];
let customRules = [];

function uid() {
  return "rule-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 7);
}

function makeReadonlyRule(rule) {
  const article = template.content.firstElementChild.cloneNode(true);
  article.classList.add("readonly");
  article.querySelector(".id").value = rule.id;
  article.querySelector(".title").value = rule.title;
  article.querySelector(".phase").value = rule.phase;
  article.querySelector(".priority").value = rule.priority;
  article.querySelector(".enabled").checked = rule.enabled !== false;
  article.querySelector(".text").value = rule.text;

  article.querySelectorAll("input, textarea, button").forEach((el) => el.disabled = true);
  return article;
}

function makeEditableRule(rule) {
  const article = template.content.firstElementChild.cloneNode(true);
  article.dataset.originalId = rule.id;

  const id = article.querySelector(".id");
  const title = article.querySelector(".title");
  const phase = article.querySelector(".phase");
  const priority = article.querySelector(".priority");
  const enabled = article.querySelector(".enabled");
  const text = article.querySelector(".text");

  id.value = rule.id;
  title.value = rule.title;
  phase.value = rule.phase;
  priority.value = rule.priority;
  enabled.checked = rule.enabled !== false;
  text.value = rule.text;

  article.querySelector(".save").addEventListener("click", async () => {
    const next = CodeByLawRules.normalizeRule({
      id: id.value || uid(),
      title: title.value,
      phase: phase.value,
      priority: priority.value,
      enabled: enabled.checked,
      text: text.value
    });

    const originalId = article.dataset.originalId;
    customRules = customRules.filter((item) => item.id !== originalId && item.id !== next.id);
    customRules.push(next);
    await persist("Rule saved.");
  });

  article.querySelector(".delete").addEventListener("click", async () => {
    customRules = customRules.filter((item) => item.id !== article.dataset.originalId);
    await persist("Rule deleted.");
  });

  return article;
}

function render() {
  defaultsHost.replaceChildren(...defaultRules.map(makeReadonlyRule));
  customHost.replaceChildren(...customRules
    .slice()
    .sort((a, b) => Number(a.priority) - Number(b.priority))
    .map(makeEditableRule));

  if (!customRules.length) {
    const empty = document.createElement("p");
    empty.className = "hint";
    empty.textContent = "No custom rules yet.";
    customHost.appendChild(empty);
  }
}

async function persist(status) {
  await chrome.storage.local.set({ customRules });
  render();
  message.textContent = status;
}

document.querySelector("#add").addEventListener("click", () => {
  customRules.push({
    id: uid(),
    title: "New rule",
    phase: "GENERAL",
    priority: 100,
    enabled: true,
    text: ""
  });
  render();
  customHost.lastElementChild?.scrollIntoView({ behavior: "smooth", block: "center" });
});

document.querySelector("#export").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(customRules, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "code-by-law-custom-rules.json";
  a.click();
  URL.revokeObjectURL(url);
});

document.querySelector("#import").addEventListener("change", async (event) => {
  const [file] = event.target.files || [];
  if (!file) return;
  try {
    const parsed = JSON.parse(await file.text());
    if (!Array.isArray(parsed)) throw new Error("Expected an array of rules.");
    customRules = parsed.map(CodeByLawRules.normalizeRule).filter((rule) => rule.id);
    await persist("Rules imported.");
  } catch (error) {
    message.textContent = "Import failed: " + error.message;
  } finally {
    event.target.value = "";
  }
});

async function init() {
  defaultRules = await fetch(chrome.runtime.getURL("rules/default-rules.json")).then((r) => r.json());
  const stored = await chrome.storage.local.get(["customRules"]);
  customRules = Array.isArray(stored.customRules) ? stored.customRules : [];
  render();
}

init();
