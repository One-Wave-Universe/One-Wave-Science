"use strict";

require("../lib/project.js");

const P = globalThis.CodeByLawProject;

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

let build = P.emptyProjectBuild();

build = P.saveLevel(build, 1, {
  goal: "first",
  checklist: "check 1",
  result: "done 1",
  verified: true,
  checkpoint: "c1"
});

build = P.saveLevel(build, 2, {
  goal: "second",
  checklist: "check 2",
  result: "done 2",
  verified: true,
  checkpoint: "c2"
});

build = P.saveLevel(build, 3, {
  goal: "third",
  checklist: "check 3",
  result: "done 3",
  verified: false,
  checkpoint: "c3"
});

const cumulative = P.cumulativeSteps(build, 3);
assert(cumulative.length === 3, "Level 3 must carry Levels 1, 2, and 3.");
assert(cumulative.map((x) => x.level).join(",") === "1,2,3", "Cumulative order must be 1,2,3.");

const packet = P.compileProjectPacket(build);
assert(packet.includes("LEVEL 1 — Action"), "Packet must include Level 1.");
assert(packet.includes("LEVEL 2 — Step"), "Packet must include Level 2.");
assert(packet.includes("LEVEL 3 — Layer"), "Packet must include Level 3.");

let blocked = false;
let incomplete = P.emptyProjectBuild();
incomplete = P.saveLevel(incomplete, 1, {
  goal: "one",
  checklist: "one",
  result: "one",
  verified: true,
  checkpoint: "x1"
});
incomplete = P.saveLevel(incomplete, 2, {
  goal: "two",
  checklist: "two",
  result: "two",
  verified: false,
  checkpoint: "x2"
});

try {
  P.saveLevel(incomplete, 3, {
    goal: "must block",
    checklist: "must block",
    result: "",
    verified: false,
    checkpoint: ""
  });
} catch (_error) {
  blocked = true;
}

assert(blocked, "Bouncer must block Level 3 while Level 2 is unverified.");

build = P.addJournalEntry(build, {
  level: 3,
  action: "third action",
  result: "pending check",
  checker: "PENDING",
  checkpoint: "c3"
});

const journalPacket = P.compileProjectPacket(build);
assert(journalPacket.includes("PROJECT JOURNAL HISTORY"), "Packet must include journal history.");
assert(journalPacket.includes("third action"), "Packet must include recorded journal action.");

console.log("PROJECT_TEST_PASS");
