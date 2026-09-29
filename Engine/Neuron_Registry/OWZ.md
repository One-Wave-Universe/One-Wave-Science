# .owz

One-Wave zip. Same DEFLATE as zip. New part is the **contract**, not the bytes.

Must contain `MANIFEST.json` with `format: owz-1`.
Must not contain `.git` or a write-copy of `Nodes/`.
Seats named `0`, `±1…±5`, `6` only.

Open: `unzip file.owz` or `python3 owz.py`.
This is the download package. Not a clone. Not Flathub.
