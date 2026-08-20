"""Branch 15 canonical Field state-kernel verification.

Run from repository root:
    python3 Field_Coder/tests/test_state_kernel.py
"""

from pathlib import Path
import sys

FIELD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIELD_ROOT))

from field.state_kernel import (
    CycleStep,
    FieldChoice,
    FieldMachineState,
    Gate,
    Modulation,
    MotionMode,
    Move,
    Operator,
    ScaleBand,
    View,
    gate_sequence,
    move_from_differential,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(len(CycleStep) == 6, "cycle must expose exactly 6 steps")
    require(len(ScaleBand) == 5, "scale must expose exactly 5 bands")
    require(len(View) == 4, "view must expose exactly 4 states")
    require(len(Operator) == 4, "operator must expose exactly 4 states")
    require(len(Move) == 3, "move must expose exactly 3 states")
    require(len(FieldChoice) == 2, "Field choice must expose exactly 2 states")
    require(len(Gate) == 6, "gate machine must expose exactly 6 gates")
    require(len(MotionMode) == 3, "motion must expose Point/Path/Field Rotation")
    require(len(Modulation) == 3, "modulation must expose Carrier/Breathing/Phase")
    print("PASS: canonical primitive counts")

    require(Gate.MIRROR_4.boundary_alias == 0, "Gate 4 must alias mirror boundary 0")
    require(
        [int(gate) for gate in gate_sequence(1)] == [1, 2, 3, 4, 5, 6],
        "forward gate order changed",
    )
    require(
        [int(gate) for gate in gate_sequence(-1)] == [6, 5, 4, 3, 2, 1],
        "reverse gate order changed",
    )
    print("PASS: mirror alias and bidirectional gate order")

    require(move_from_differential(2.0) is Move.EXPAND, "positive differential must expand")
    require(move_from_differential(0.0) is Move.HOLD, "zero differential must hold")
    require(move_from_differential(-2.0) is Move.COMPRESS, "negative differential must compress")
    require(move_from_differential(0.05, epsilon=0.1) is Move.HOLD, "epsilon hold band failed")
    print("PASS: ternary differential movement")

    state = FieldMachineState(
        active_field="coding:state-kernel",
        reference=0.25,
        differential=-0.5,
        cycle_step=CycleStep.BEGIN,
        scale=ScaleBand.MEDIUM_MID,
        view=View.ACROSS,
        operator=Operator.MINUS,
        move=Move.COMPRESS,
        choice=FieldChoice.POSITIVE,
        gate=Gate.MIRROR_4,
        motion=MotionMode.FIELD_ROTATION,
        modulation=Modulation.PHASE,
        history=("branch15-hard-start",),
    )
    state.validate()
    require(state.reference == 0.25, "reference not preserved")
    require(state.differential == -0.5, "differential not preserved")
    require(state.gate.boundary_alias == 0, "state lost mirror boundary")
    require(state.motion is MotionMode.FIELD_ROTATION, "motion not preserved")
    require(state.modulation is Modulation.PHASE, "modulation not preserved")
    require(state.history == ("branch15-hard-start",), "history not preserved")

    moved = state.with_differential(0.75)
    require(moved.move is Move.EXPAND, "state differential did not update move")
    require(moved.differential == 0.75, "state differential not updated")

    forward = state.advance(1)
    reverse = state.advance(-1)
    require(forward.gate is Gate.GATE_5, "mirror forward step must reach Gate 5")
    require(reverse.gate is Gate.GATE_3, "mirror reverse step must reach Gate 3")
    print("PASS: valid Field machine state preserves canonical state")

    try:
        invalid = FieldMachineState(
            active_field="   ",
            reference=0.0,
            differential=0.0,
            cycle_step=CycleStep.HOLD,
            scale=ScaleBand.MICRO_FLOOR,
            view=View.INWARD,
            operator=Operator.PLUS,
            move=Move.HOLD,
            choice=FieldChoice.NEGATIVE,
            gate=Gate.GATE_1,
            motion=MotionMode.POINT,
            modulation=Modulation.CARRIER,
        )
        invalid.validate()
    except ValueError:
        print("PASS: empty active-field identity rejected")
    else:
        raise AssertionError("empty active-field identity was accepted")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
