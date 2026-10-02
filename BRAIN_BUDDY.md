# Brain Buddy — CANONICAL ENTRY

There is one Brain Buddy architecture.

```text
Mark = human operator
ChatGPT = origin / return AI
Gemini = peer AI
DeepSeek = peer AI

ChatGPT -> Brain Buddy Council -> Gemini <-> DeepSeek -> ChatGPT
```

Canonical implementation:

- `scripts/brain_buddy_council.py`
- launcher: `scripts/brain_buddy_council.sh`
- behavior contract: `BRAIN_BUDDY_COUNCIL.md`

Historical recovery anchor:

- original unified Council commit: `a2d0a09bc77dd8f3bdb742b6a4c4eba20f6c9654`

Run:

```bash
bash scripts/brain_buddy_council.sh discussion "question" --rounds 3 --save
```

The Python council owns orchestration and cumulative handoff. `scripts/gemini_min.sh` and `scripts/deepseek_min.sh` are transports/workers only; they are not alternate Brain Buddy implementations.

Do not create a second Brain Buddy, replacement Brain Buddy, Gemini-only Brain Buddy, or branch-specific Brain Buddy. Changes must copy/branch from the canonical council, preserve the last working version, test the new branch, and promote it only after verified return-path receipts.

For science work, each peer follows the repository reference contract before external research and returns findings to the exact repo claim/test.

If anything conflicts with this file about which Brain Buddy is canonical, this file wins.
