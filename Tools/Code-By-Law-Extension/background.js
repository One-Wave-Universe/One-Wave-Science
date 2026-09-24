"use strict";

function parseRepo(value) {
  const raw = String(value || "").trim().replace(/\/$/, "");
  const m = raw.match(/github\.com\/([^/]+)\/([^/]+)$/i);
  if (!m) throw new Error("Use a GitHub repo URL like https://github.com/owner/repo");
  return { owner: m[1], repo: m[2].replace(/\.git$/i, "") };
}

async function githubJson(url) {
  const response = await fetch(url, {
    cache: "no-store",
    headers: { Accept: "application/vnd.github+json" }
  });
  if (!response.ok) throw new Error("GitHub HTTP " + response.status);
  return response.json();
}

async function githubText(url) {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) throw new Error("GitHub HTTP " + response.status);
  return response.text();
}

async function fetchGitHubReference() {
  const stored = await chrome.storage.local.get(["githubRepo", "githubBranch", "referencePaths"]);
  const { owner, repo } = parseRepo(stored.githubRepo || "https://github.com/One-Wave-Universe/One-Wave-Science");
  const branch = String(stored.githubBranch || "main").trim() || "main";
  const branchInfo = await githubJson(
    "https://api.github.com/repos/" + encodeURIComponent(owner) + "/" + encodeURIComponent(repo) +
    "/branches/" + encodeURIComponent(branch)
  );

  const paths = String(stored.referencePaths || "")
    .split(/\r?\n/)
    .map((x) => x.trim())
    .filter(Boolean);

  const files = [];
  for (const path of paths) {
    const rawUrl = "https://raw.githubusercontent.com/" +
      encodeURIComponent(owner) + "/" + encodeURIComponent(repo) + "/" +
      encodeURIComponent(branch) + "/" + path.split("/").map(encodeURIComponent).join("/");
    try {
      const text = await githubText(rawUrl);
      files.push({ path, present: true, text: text.slice(0, 12000) });
    } catch (error) {
      files.push({ path, present: false, error: error.message });
    }
  }

  return {
    state: "ACTIVE",
    repo: "https://github.com/" + owner + "/" + repo,
    branch,
    head: branchInfo.commit?.sha || "unknown",
    files
  };
}

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message?.type === "CBL_GET_GITHUB_REFERENCE") {
    fetchGitHubReference()
      .then((data) => sendResponse({ ok: true, data }))
      .catch((error) => sendResponse({ ok: false, error: error.message }));
    return true;
  }
});
