import numpy as np


class WaveComputingNode:
    """
    Experimental software primitive for the working One-Wave multi-radix cycle:

        BC-DC -> TC-AC -> 4 Actions -> 4 Views -> TC Return -> BC Closure

    This is a simulation model, not evidence that a physical circuit will
    automatically realize the same behavior.
    """

    ACTION_NAMES = ("Inward", "Outward", "Across", "Over")
    VIEW_NAMES = ("Direction", "Phase", "Strength", "Reference")

    def __init__(
        self,
        scale_id,
        bias_asymmetry=0.15,
        ternary_threshold=0.30,
        return_threshold=0.10,
        reference_alpha=0.18,
        phase=0.0,
    ):
        self.scale_id = scale_id
        self.bias = float(bias_asymmetry)
        self.ternary_threshold = float(ternary_threshold)
        self.return_threshold = float(return_threshold)
        self.reference_alpha = float(reference_alpha)

        self.phase = float(phase)
        self.reference = 0.0

        self.state_bc_seed = 0          # -1 or +1
        self.state_tc_forward = 0       # -1, 0, +1
        self.state_action = 0           # 0..3
        self.state_view = 0             # 0..3
        self.state_tc_return = 0        # -1, 0, +1
        self.state_bc_closure = 0       # -1, 0(HOLD), +1

        self.last_differential = 0.0
        self.last_output = 0.0

    @staticmethod
    def _ternary(value, threshold):
        if value > threshold:
            return 1
        if value < -threshold:
            return -1
        return 0

    @staticmethod
    def _scalarize(input_vector):
        arr = np.asarray(input_vector, dtype=float).reshape(-1)
        if arr.size == 0:
            return 0.0
        # Preserve signed imbalance rather than using an unsigned magnitude.
        weights = np.linspace(1.0, 0.5, arr.size)
        return float(np.dot(arr, weights) / np.sum(np.abs(weights)))

    def step(self, input_vector, phase_shift_delta=np.pi / 4):
        # Local differential against this scale's own moving reference.
        incoming = self._scalarize(input_vector)
        differential = incoming - self.reference
        self.last_differential = differential

        # 1) BC-DC: binary directional seed.
        self.state_bc_seed = 1 if differential >= 0.0 else -1

        # 2) TC-AC: ternary oscillatory motion with a small asymmetric lean.
        raw_forward = (
            self.state_bc_seed * np.cos(self.phase)
            + self.bias
            + 0.35 * differential
        )
        self.state_tc_forward = self._ternary(
            raw_forward, self.ternary_threshold
        )

        # 3) Four Actions.
        # Ternary sign is preserved: + advances, - reverses, 0 holds.
        action_step = self.state_tc_forward
        if self.state_bc_seed < 0:
            action_step *= -1
        self.state_action = (self.state_action + action_step) % 4

        # 4) Four Views.
        # The view is a separate quadratic state derived from phase,
        # local action, and reference side.
        phase_quadrant = int(
            np.floor((self.phase % (2 * np.pi)) / (np.pi / 2))
        ) % 4
        reference_side = 1 if self.reference >= 0 else -1
        self.state_view = (
            phase_quadrant
            + self.state_action
            + (1 if reference_side < 0 else 0)
        ) % 4

        # Advance phase before evaluating the mirrored/return consequence.
        self.phase = (self.phase + phase_shift_delta) % (2 * np.pi)

        # Forward consequence. Action and View contribute differently,
        # so the 4x4 layer is not collapsed into one integer.
        action_projection = (self.state_action - 1.5) / 1.5
        view_projection = (self.state_view - 1.5) / 1.5
        oscillatory = self.state_tc_forward * np.sin(self.phase)

        consequence = (
            0.52 * oscillatory
            + 0.18 * action_projection
            + 0.14 * view_projection
            + 0.22 * differential
            + self.bias
        )

        # 5) TC Return: evaluate consequence against the same local reference.
        return_delta = consequence - self.reference
        self.state_tc_return = self._ternary(
            return_delta, self.return_threshold
        )

        # 6) BC Closure.
        # Binary remains binary. A ternary HOLD means "do not engage closure",
        # represented here by 0 as gate inactivity, not a third binary state.
        if self.state_tc_return == 0:
            self.state_bc_closure = 0
        else:
            # Seed supplies orientation; return supplies evaluation.
            self.state_bc_closure = (
                self.state_bc_seed * self.state_tc_return
            )

        # Bounded signed output for the next scale.
        closure_gain = 0.0 if self.state_bc_closure == 0 else self.state_bc_closure
        output = (
            0.55 * return_delta
            + 0.25 * self.state_tc_return
            + 0.12 * closure_gain
            + 0.08 * differential
        )
        output = float(np.tanh(output))

        # Update local memory/reference only after evaluation.
        self.reference = (
            (1.0 - self.reference_alpha) * self.reference
            + self.reference_alpha * consequence
        )
        self.last_output = output
        return output

    def snapshot(self):
        return {
            "scale": self.scale_id,
            "differential": self.last_differential,
            "bc_seed": self.state_bc_seed,
            "tc_forward": self.state_tc_forward,
            "action": self.state_action,
            "action_name": self.ACTION_NAMES[self.state_action],
            "view": self.state_view,
            "view_name": self.VIEW_NAMES[self.state_view],
            "tc_return": self.state_tc_return,
            "bc_closure": self.state_bc_closure,
            "reference": self.reference,
            "output": self.last_output,
        }


def run_demo(steps=12):
    octaves = [
        WaveComputingNode(scale_id=0, bias_asymmetry=0.15, phase=0.00),
        WaveComputingNode(scale_id=1, bias_asymmetry=0.12, phase=0.35),
        WaveComputingNode(scale_id=2, bias_asymmetry=0.09, phase=0.70),
    ]

    signal_flow = np.array([1.0, -1.0, 0.5], dtype=float)

    print("Running Full Multi-Radix Octave Simulation")
    print("Cycle: BC-DC -> TC-AC -> 4 Actions -> 4 Views -> TC Return -> BC Closure")
    print()

    history = []

    for step_idx in range(steps):
        current_signal = signal_flow.copy()
        row = []

        for octave in octaves:
            diff_out = octave.step(
                current_signal,
                phase_shift_delta=np.pi / 4,
            )
            snap = octave.snapshot()
            row.append(snap)

            closure_text = (
                "HOLD" if snap["bc_closure"] == 0
                else f"{snap['bc_closure']:+d}"
            )

            print(
                f"Step {step_idx:02d} | Scale {snap['scale']} | "
                f"Δ:{snap['differential']:+.3f} | "
                f"BC:{snap['bc_seed']:+d} "
                f"TC:{snap['tc_forward']:+d} | "
                f"A{snap['action']}:{snap['action_name']:<7} | "
                f"V{snap['view']}:{snap['view_name']:<9} | "
                f"TCr:{snap['tc_return']:+d} | "
                f"BCc:{closure_text:>4} | "
                f"Ref:{snap['reference']:+.3f} | "
                f"Out:{snap['output']:+.3f}"
            )

            # Signed differential packet for the next octave.
            current_signal = np.array(
                [
                    diff_out,
                    -0.70 * diff_out,
                    0.35 * diff_out + 0.15 * snap["differential"],
                ],
                dtype=float,
            )

        history.append(row)
        print("-" * 132)

    return history


if __name__ == "__main__":
    run_demo()
