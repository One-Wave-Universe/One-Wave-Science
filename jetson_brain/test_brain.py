import tempfile
from pathlib import Path
from brain import M4Loop

repo = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    a = M4Loop(root, repo_root=repo)

    for q in ("what is two plus two?", "what is 2+2?", "2 + 2 equals what?", "please calculate two plus two"):
        r = a.cycle(q)
        assert r["answer"] == "4", (q, r["answer"], r["evidence"])
        assert r["evidence"]["source"] == "arithmetic"
        assert r["void"]["response"] == "CONFIRM"

    unknown = a.cycle("remember the blue motor balance test")
    assert unknown["void"]["response"] == "DEFER"
    remembered = a.cycle("what did I say about motor balance?")
    assert remembered["evidence"]["source"] == "memory", remembered
    assert "blue motor balance test" in remembered["answer"].lower()

    canon = a.cycle("what are the three moves?")
    assert canon["evidence"]["source"] == "canon", canon
    assert all(word in canon["answer"].upper() for word in ("DOWN", "HOLD", "UP")), canon["answer"]

    row = a.memory.conn.execute("SELECT * FROM receipts ORDER BY id ASC LIMIT 1").fetchone()
    assert row["pre_reference"] == "GROUND / LOCAL REFERENCE", row["pre_reference"]
    assert row["post_reference"] == "4", row["post_reference"]

    expected = dict(a.state.__dict__)
    b = M4Loop(root, repo_root=repo)
    assert dict(b.state.__dict__) == expected

    (root / "state.json").unlink()
    c = M4Loop(root, repo_root=repo)
    assert c.state.cycle == expected["cycle"]
    assert c.state.reference == expected["reference"]
    assert c.state.last_choice == expected["last_choice"]
    assert c.state.last_move == expected["last_move"]
    assert c.state.last_void == expected["last_void"]
    assert c.state.last_result == expected["last_result"]

print("PASS deterministic-answer/recall/rebuild")
