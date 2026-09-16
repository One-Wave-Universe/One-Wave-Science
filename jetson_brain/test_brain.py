import tempfile
from pathlib import Path
from brain import M4Loop

with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    a = M4Loop(root)
    r1 = a.cycle("remember the blue motor balance test")
    assert r1["cycle"] == 1
    r2 = a.cycle("what about the motor balance")
    assert r2["cycle"] == 2
    assert r2["recall"], "recall should return prior receipts"
    b = M4Loop(root)
    assert b.state.cycle == 2, b.state
    assert b.state.last_result == r2["result"]
    assert (root / "memory.sqlite3").exists()
    assert (root / "state.json").exists()
print("PASS recall/rebuild")
