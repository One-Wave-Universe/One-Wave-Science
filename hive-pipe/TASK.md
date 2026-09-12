# Hive Pipe v1 branch-step

- **MAIN GOAL:** provide a reliable, bounded route from a queued request to a
  Jetson terminal result.
- **CURRENT STEP:** implement and verify the local queue protocol.
- **HARD START:** verified One-Wave-Science repository; separate branch; clean
  starting state.
- **ALLOWED FILES:** `hive-pipe/**` only.
- **PROTECTED:** `Virtual_Breadboard/**`, Android/control files, external drives,
  mounts, partitions, filesystems, credentials, and user data.
- **ACTION:** accept only named read-only actions; produce deterministic JSON
  results; reject malformed or unknown jobs.
- **SUCCESS:** self-test passes; drive inventory runs without write operations;
  one job produces one result and one archived request.
- **HARD STOP:** stop after the local queue loop is proven. Remote transport is
  a separate branch-step.

