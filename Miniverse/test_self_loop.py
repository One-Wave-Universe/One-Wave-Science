#!/usr/bin/env python3
from self_loop import Event, Route, SelfLoop, demo_stream


def test_no_permission_ask_and_filters_firehose():
    loop = SelfLoop()
    out = loop.run(demo_stream())
    assert out["asked_permission"] is False
    assert out["baseline_generation_unchanged"] is True
    routes = [r["route"] for r in out["receipts"]]
    assert routes.count("DROP") >= 1
    assert routes.count("LOCAL") >= 1
    assert routes.count("FORWARD") == 1
    assert routes.count("HOLD") == 1
    fwd = out["escalations"][0]
    assert fwd["why_forward"]
    assert "body_state_refs" in fwd
    assert loop.body.generation == 0


def test_low_confidence_never_forwards():
    loop = SelfLoop()
    rec = loop.tick(Event("speech.command", 0.2, 0.2, 0.9, "maybe"))
    assert rec["route"] == Route.DROP.value
    assert rec["why_forward"] is None
    assert loop.body.forwards == 0


if __name__ == "__main__":
    test_no_permission_ask_and_filters_firehose()
    test_low_confidence_never_forwards()
    print("ok")
