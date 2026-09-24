# Goblin Folder Holder

A **Goblin Folder Holder** is a supervisory folder that watches a group of child
folders. It is the foreman for that group.

It is NOT the same thing as an individual watched folder.

## Structure

```text
Goblin Folder Holder/
  .goblin-holder/
    holder.json
    group-index.json
    events.jsonl
    HOLD.json
  child-folder-a/
    .owatch/
      folder.json
      index.json
      state.json
      events.jsonl
      HOLD.json
  child-folder-b/
    .owatch/
      ...
```

## Responsibilities

The Holder:

- discovers child OWATCH folders beneath it;
- reads each child's compressed layered index;
- compares authority/reference pointers across children;
- detects cross-folder drift and conflicting edits;
- verifies intended scope before mutation;
- refuses commit if any child is on HOLD;
- checks that references, intention and consequence exist;
- commits approved changes for the supervised group;
- records the commit and propagates refreshed baselines back to children.

## Editing depth

Child watchers provide exact targeting:

```text
holder
  -> watched child folder
  -> subfolder
  -> file
  -> section
  -> sentence/line
  -> word/span
```

The Holder decides whether the requested change is allowed to stay at that
smallest scope or whether a wider coordinated change is explicitly required.

## Anti-drift rule

Unknown state is inspected, never assumed.

A child change without a matching reference chain becomes HOLD.
A conflict between child folder authority maps becomes HOLD.
A change outside the requested group/scope becomes HOLD.
Only a clean Holder may commit.
