from pathlib import Path

from One_Wave_Bench.agent_host.shared_loop_mvp import (
    AdminDecision,
    LoopStep,
    M4Host,
    SharedState,
    ToolAction,
)


def test_shared_state_survives_complete_loop(tmp_path: Path) -> None:
    workspace = tmp_path / "repo"
    workspace.mkdir()
    target = workspace / "demo.txt"
    target.write_text("old\n", encoding="utf-8")

    host = M4Host(SharedState(root_reference="demo.txt must contain new"), workspace)
    host.begin("demo.txt currently contains old")
    assert host.state.step is LoopStep.BUILD_1

    read = host.dream_tool(ToolAction(kind="read", path="demo.txt"))
    assert read.ok and "old" in read.output
    assert host.state.step is LoopStep.BUILD_1

    write = host.dream_tool(ToolAction(kind="write", path="demo.txt", content="new\n"))
    assert write.ok and write.changed
    assert host.state.step is LoopStep.HOLD

    host.hold(
        "demo.txt now contains new",
        AdminDecision(
            direction="+",
            relation="measured file moved toward reference",
            dimensional_view="next build sees target satisfied",
            oversight="aligned",
        ),
    )
    assert host.state.step is LoopStep.BUILD_2

    # Second BUILD makes one real refinement, then BREAK measures it.
    host.dream_tool(ToolAction(kind="write", path="note.txt", content="receipt\n"))
    assert host.state.step is LoopStep.BREAK

    host.break_step(
        "target remains satisfied after refinement",
        AdminDecision(
            direction="0",
            relation="reference preserved",
            dimensional_view="safe to compress",
            oversight="no override needed",
        ),
    )
    assert host.state.step is LoopStep.LOOP

    host.complete_loop("demo target satisfied; note receipt added", unresolved=[])
    assert host.state.step is LoopStep.BEGIN
    assert host.state.cycle == 2
    assert host.state.inherited_state[-1] == "demo target satisfied; note receipt added"

    restored = SharedState.load(workspace / ".onewave" / "shared_state.json")
    assert restored.root_reference == "demo.txt must contain new"
    assert restored.cycle == 2
    assert restored.inherited_state[-1] == "demo target satisfied; note receipt added"


def test_dream_cannot_edit_during_hold(tmp_path: Path) -> None:
    workspace = tmp_path / "repo"
    workspace.mkdir()
    host = M4Host(SharedState(root_reference="keep reference"), workspace)
    host.begin("start")
    host.dream_tool(ToolAction(kind="write", path="a.txt", content="x"))
    assert host.state.step is LoopStep.HOLD

    try:
        host.dream_tool(ToolAction(kind="write", path="b.txt", content="y"))
    except RuntimeError as exc:
        assert "only available in BUILD" in str(exc)
    else:
        raise AssertionError("Dream edit should be blocked during HOLD")
