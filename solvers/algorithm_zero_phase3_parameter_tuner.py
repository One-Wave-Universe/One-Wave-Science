"""
Phase 3 Parameter Tuning: Systematic exploration of coupling parameters.

Goal: Find parameter combinations that produce:
- Inner gradient: 30+ km/s per kpc
- Outer plateau: ±25 km/s variation max
- Full velocity range: 100-250 km/s

Key tunable parameters:
- initial_amplitude: controls wake strength
- saturation_amplitude: controls maximum pressure growth
- gradient_response_strength: controls asymmetric coupling sensitivity
- equilibration_steps: number of steps before measurement
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict
from solvers.algorithm_zero_phase3_pressure_tensor import PressureTensorLattice

@dataclass
class TuningResult:
    """Result of one tuning trial."""
    initial_amplitude: float
    saturation_amplitude: float
    gradient_response_strength: float
    equilibration_steps: int

    # Measured outcomes
    initial_velocity: float
    final_velocity: float
    velocity_range: float
    mean_velocity: float
    max_gradient: float  # maximum radial velocity change per kpc
    outer_plateau_width: float  # width of constant-velocity region
    outer_plateau_variation: float  # ±variation in outer plateau

    # Quality score (lower is better if target-aligned)
    score: float = 0.0

    def compute_score(self, target_vmin=100, target_vmax=250):
        """
        Compute quality score based on success criteria.
        Lower score = closer to target.
        """
        # Range check: target 100-250 km/s
        if self.velocity_range < target_vmin or self.velocity_range > target_vmax:
            range_penalty = abs(self.velocity_range - (target_vmax + target_vmin) / 2) / 100.0
        else:
            range_penalty = 0

        # Gradient check: want 30+ km/s per kpc
        gradient_penalty = max(0, 30 - self.max_gradient) / 10.0

        # Plateau variation check: want ±25 km/s or less
        plateau_penalty = max(0, self.outer_plateau_variation - 25) / 10.0

        self.score = range_penalty + gradient_penalty + plateau_penalty
        return self.score


class ParameterTuner:
    """Systematic parameter tuning for Phase 3 pressure tensor."""

    def __init__(self, base_lattice_params: Dict = None):
        """Initialize tuner with base lattice parameters."""
        self.base_lattice_params = base_lattice_params or {
            'n_r': 32, 'n_theta': 48, 'n_z': 16,
            'r_disk': 1.0, 'z_height': 0.1,
            'rho_0': 1.0, 'gamma': 0.05, 'beta': 0.15
        }
        self.results: List[TuningResult] = []

    def run_trial(self,
                  initial_amplitude: float,
                  saturation_amplitude: float,
                  gradient_response_strength: float,
                  equilibration_steps: int = 50,
                  evolution_steps: int = 100) -> TuningResult:
        """
        Run one tuning trial with given parameters.

        Args:
            initial_amplitude: strength of initial pressure wake
            saturation_amplitude: Ψ_max for saturation cutoff
            gradient_response_strength: coupling to ∇ρ
            equilibration_steps: steps before measuring
            evolution_steps: steps after equilibration

        Returns:
            TuningResult with measured outcomes
        """
        # Create lattice
        lattice = PressureTensorLattice(**self.base_lattice_params)

        # Initialize with specific amplitude
        lattice.inject_pressure_wake(amplitude=initial_amplitude)

        # Enable features with specific parameters
        lattice.enable_nonlinear_saturation(saturation_amplitude=saturation_amplitude)
        lattice.enable_asymmetric_mass_coupling(
            gradient_response_strength=gradient_response_strength
        )

        # Measure initial state
        initial_curve = lattice.measure_rotation_velocity()
        initial_v = np.mean(initial_curve[initial_curve > 0]) if np.any(initial_curve > 0) else 0.0

        # Equilibration phase
        lattice.run_equilibration(n_steps=equilibration_steps)

        # Evolution phase
        lattice.run_evolution(n_steps=evolution_steps)

        # Measure final state
        final_curve = lattice.measure_rotation_velocity()
        final_v = np.mean(final_curve[final_curve > 0]) if np.any(final_curve > 0) else 0.0

        # Compute statistics
        stats = lattice.measure_pressure_statistics()
        velocity_range = np.ptp(final_curve[final_curve > 0]) if np.any(final_curve > 0) else 0.0
        mean_velocity = np.mean(final_curve[final_curve > 0]) if np.any(final_curve > 0) else 0.0

        # Estimate inner gradient
        # (radial velocity gradient near bulge region, r ~ 0.1-0.2)
        inner_indices = (lattice.radii > 0.05) & (lattice.radii < 0.25)
        if np.any(inner_indices):
            inner_curve = final_curve[inner_indices]
            inner_r = lattice.radii[inner_indices]
            if len(inner_r) > 1:
                max_gradient = np.max(np.abs(np.gradient(inner_curve, inner_r)))
            else:
                max_gradient = 0.0
        else:
            max_gradient = 0.0

        # Estimate outer plateau width and variation
        # (regions where velocity is approximately constant, r > 0.5)
        outer_indices = lattice.radii > 0.5
        if np.any(outer_indices):
            outer_curve = final_curve[outer_indices]
            outer_r = lattice.radii[outer_indices]
            outer_plateau_width = np.ptp(outer_r)
            outer_plateau_variation = np.std(outer_curve[outer_curve > 0]) if np.any(outer_curve > 0) else 0.0
        else:
            outer_plateau_width = 0.0
            outer_plateau_variation = 0.0

        result = TuningResult(
            initial_amplitude=initial_amplitude,
            saturation_amplitude=saturation_amplitude,
            gradient_response_strength=gradient_response_strength,
            equilibration_steps=equilibration_steps,
            initial_velocity=initial_v,
            final_velocity=final_v,
            velocity_range=velocity_range,
            mean_velocity=mean_velocity,
            max_gradient=max_gradient,
            outer_plateau_width=outer_plateau_width,
            outer_plateau_variation=outer_plateau_variation
        )

        result.compute_score()
        self.results.append(result)

        return result

    def grid_search(self,
                   initial_amplitudes: List[float],
                   saturation_amplitudes: List[float],
                   gradient_responses: List[float],
                   equilibration_steps: int = 50,
                   evolution_steps: int = 100) -> List[TuningResult]:
        """
        Perform grid search over parameter space.

        Args:
            initial_amplitudes: values to try for wake amplitude
            saturation_amplitudes: values to try for saturation cutoff
            gradient_responses: values to try for gradient coupling
            equilibration_steps: steps before measurement
            evolution_steps: steps for evolution

        Returns:
            List of TuningResult objects, sorted by score
        """
        total_trials = (len(initial_amplitudes) * len(saturation_amplitudes) *
                       len(gradient_responses))
        trial_count = 0

        for init_amp in initial_amplitudes:
            for sat_amp in saturation_amplitudes:
                for grad_resp in gradient_responses:
                    trial_count += 1
                    print(f"\nTrial {trial_count}/{total_trials}")
                    print(f"  initial_amplitude={init_amp:.2f}")
                    print(f"  saturation_amplitude={sat_amp:.2f}")
                    print(f"  gradient_response_strength={grad_resp:.2f}")

                    try:
                        result = self.run_trial(
                            initial_amplitude=init_amp,
                            saturation_amplitude=sat_amp,
                            gradient_response_strength=grad_resp,
                            equilibration_steps=equilibration_steps,
                            evolution_steps=evolution_steps
                        )

                        print(f"  Result:")
                        print(f"    velocity_range: {result.velocity_range:.1f} km/s")
                        print(f"    mean_velocity: {result.mean_velocity:.1f} km/s")
                        print(f"    max_gradient: {result.max_gradient:.1f} km/s/kpc")
                        print(f"    outer_plateau_variation: ±{result.outer_plateau_variation:.1f} km/s")
                        print(f"    score: {result.score:.3f}")

                    except Exception as e:
                        print(f"  FAILED: {e}")

        # Sort by score (lower is better)
        self.results.sort(key=lambda r: r.score)
        return self.results

    def report_best(self, n_best: int = 5) -> None:
        """Print report of best tuning results."""
        if not self.results:
            print("No results yet")
            return

        print("\n" + "="*80)
        print("PHASE 3 PARAMETER TUNING RESULTS")
        print("="*80)

        print(f"\nTop {min(n_best, len(self.results))} Results:")
        print("-" * 80)

        for rank, result in enumerate(self.results[:n_best], 1):
            print(f"\n#{rank} (score={result.score:.3f})")
            print(f"  Parameters:")
            print(f"    initial_amplitude={result.initial_amplitude:.2f}")
            print(f"    saturation_amplitude={result.saturation_amplitude:.2f}")
            print(f"    gradient_response_strength={result.gradient_response_strength:.2f}")
            print(f"  Measured:")
            print(f"    velocity_range: {result.velocity_range:.1f} km/s")
            print(f"    mean_velocity: {result.mean_velocity:.1f} km/s")
            print(f"    max_gradient: {result.max_gradient:.1f} km/s/kpc")
            print(f"    outer_plateau_variation: ±{result.outer_plateau_variation:.1f} km/s")

        print("\n" + "="*80)


def main():
    """Example: grid search over parameter space."""

    tuner = ParameterTuner()

    # Grid search parameters
    # Start with moderate ranges, expand based on results
    initial_amplitudes = [0.5, 1.0, 1.5, 2.0]
    saturation_amplitudes = [1.5, 2.0, 2.5, 3.0]
    gradient_responses = [0.1, 0.2, 0.3, 0.5]

    print("Starting Phase 3 parameter tuning grid search...")
    print(f"Parameter space: {len(initial_amplitudes)} × {len(saturation_amplitudes)} × {len(gradient_responses)} = "
          f"{len(initial_amplitudes)*len(saturation_amplitudes)*len(gradient_responses)} trials")

    results = tuner.grid_search(
        initial_amplitudes=initial_amplitudes,
        saturation_amplitudes=saturation_amplitudes,
        gradient_responses=gradient_responses,
        equilibration_steps=50,
        evolution_steps=100
    )

    tuner.report_best(n_best=10)


if __name__ == "__main__":
    main()
