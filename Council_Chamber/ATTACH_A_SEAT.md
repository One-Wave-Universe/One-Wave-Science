# Copy-paste this to another AI to attach its own Council Chamber seat

Paste everything in the code block below into ChatGPT, Gemini, Grok,
DeepSeek, or another Claude session's chat window. It only needs to
write one Python file's contents back to you — you then save that
content into this repo yourself (that other AI's chat window has no
direct access to this filesystem).

Fill in `<PROVIDER_KEY>` (lowercase, e.g. `chatgpt`, `grok`, `deepseek`)
and `<Display Name>` (e.g. `ChatGPT`, `Grok`, `DeepSeek`) before sending.

---

```
I'm attaching a seat to a local multi-AI project called the One-Wave
Council Chamber. I need you to write ONE Python file for me. Give me
only the file's contents, nothing else.

The file must define:

1. A factory function:

   def make_<PROVIDER_KEY>_client(model: str = "<a sensible default model
   name for your own API>", api_key: str | None = None):
       ...

   It should read `api_key`, or if that's None, read it from an
   environment variable named <PROVIDER_KEY_UPPERCASE>_API_KEY. If
   neither is set, raise a clearly-named exception (e.g.
   <Provider>NotConfiguredError(RuntimeError)) explaining what env var
   to set -- never fall back to a fake reply.

   It must return a callable with this exact signature:

       def client(context: list) -> tuple[str, dict] | str:
           ...

   `context` is a list of message objects, each with `.sender_seat_id`
   (str or None for the user) and `.content` (str) attributes. Build a
   prompt from them (e.g. join "{sender}: {content}" lines) and send it
   to your own real API using your provider's real REST endpoint or
   SDK.

   On success, return either just the reply text, or a
   (reply_text, usage_dict) tuple where usage_dict has whichever of
   these keys your API actually reports: input_tokens, output_tokens,
   requests, estimated_price_usd, context_window_used. Only include keys
   you can honestly report -- never invent a token count.

   On a real API failure (bad key, quota, network error), raise a
   clearly-named exception (e.g. <Provider>APIError(RuntimeError)) with
   the provider's own error message. Do not catch it and return a fake
   "sorry, something went wrong" reply -- let it raise.

2. At the bottom of the file, exactly these two lines:

   from council_chamber.client_registry import register_client
   register_client("<PROVIDER_KEY>", "<Display Name>", make_<PROVIDER_KEY>_client)

Use only your provider's own standard library HTTP approach or official
SDK -- whichever is simplest and most reliable for your own API. Model
the whole file's shape after this working example for a different
provider (Gemini), if it helps:

[paste the contents of Council_Chamber/python/council_chamber/seats/gemini_client.py here if you want to give it a concrete reference]

Give me the complete file contents now.
```

---

## What you do with the answer

1. Save what it gives you as:
   `Council_Chamber/python/council_chamber/seats/<PROVIDER_KEY>_client.py`
2. Set the API key it asked for: `export <PROVIDER_KEY_UPPERCASE>_API_KEY=...`
3. From `Council_Chamber/python`, run:
   ```bash
   python3 -m council_chamber.tui
   ```
   then type `open <PROVIDER_KEY>` — if the file is correct, that seat
   now answers for real. If something's wrong, the TUI shows the exact
   Python exception, not a silent failure — paste that back to whichever
   AI wrote the file and ask it to fix it.

No other file in this repo needs to change. This is exactly the same
mechanism `gemini_client.py` uses — see `client_registry.py` for the
full contract, and `README.md`'s "Attaching your own seat" section.
