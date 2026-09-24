# OWATCH Folder Type

An **OWATCH folder** is an ordinary repository directory that becomes a protected,
layered editing domain when it contains:

```text
.owatch/
  folder.json
```

The directory itself is the watcher unit. Source files remain normal files.

## Folder behavior

An OWATCH folder provides:

- compressed layered map of its own contents;
- local authority/reference pointers;
- subfolder and file-role indexes;
- exact line/sentence/word edit anchors;
- hashes and Git state;
- local HOLD when an unreferenced change appears;
- upward reporting to the higher-level anti-drift checker;
- commit permission only after reference, scope, watcher and checker agree.

## Required marker

`.owatch/folder.json`:

```json
{
  "schema": "one-wave-watched-folder-v1",
  "mode": "fail_closed",
  "editing_granularity": ["word", "sentence", "line", "section", "file"],
  "reference_required": true,
  "intention_required": true,
  "consequence_required": true,
  "source_files_authoritative": true
}
```

## Runtime state

Runtime data stays beside the marker:

```text
.owatch/
  folder.json
  index.json
  state.json
  events.jsonl
  HOLD.json
```

Only `folder.json` is canonical configuration. The others are generated state.

## Layered targeting

AI editing descends only as far as required:

```text
OWATCH folder
  -> child folder
  -> file
  -> heading/section
  -> sentence/line anchor
  -> exact word/span
```

A one-word request must not become a paragraph rewrite. A sentence edit must not
rewrite the file unless a wider scope is explicitly referenced.

## Higher-level checker

Parent/root OWATCH folders aggregate child watcher results. Any child HOLD,
missing reference, scope escape, or authority mismatch blocks mutation/commit.
