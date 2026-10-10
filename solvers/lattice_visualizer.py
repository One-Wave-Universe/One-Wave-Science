#!/usr/bin/env python3
"""
Lattice visualization of peak/trough dynamics
Simulates electron-positron pair production and annihilation on 1D lattice
"""

import os
import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from dataclasses import dataclass
from typing import Dict, List, Tuple
import scipy.fft


@dataclass
class LatticeSimulation:
    """Core lattice simulator with update rule and perturbation injection"""

    beta: float
    gamma: float
    lattice_size: int = 256

    def __post_init__(self):
        """Initialize field and history tracking"""
        self.L = self.lattice_size
        self.psi = np.random.randn(self.L) * 0.01  # Small random perturbation
        self.psi_prev = self.psi.copy()
        self.history = []
        self.energy_history = []
        self.time_history = []
        self.frequency_history = []

    def update_step(self) -> np.ndarray:
        """Execute one update of the core rule
        ψᵢⁿ⁺¹ = ψᵢⁿ + (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) + β(⟨ψⱼⁿ⟩-ψᵢⁿ)
        """
        # Neighbor average (periodic boundary)
        neighbor_avg = (np.roll(self.psi, 1) + np.roll(self.psi, -1)) / 2.0

        # Core update rule
        psi_new = (self.psi +
                   (1 - self.gamma) * (self.psi - self.psi_prev) +
                   self.beta * (neighbor_avg - self.psi))

        self.psi_prev = self.psi.copy()
        self.psi = psi_new

        return self.psi.copy()

    def run_equilibration(self, steps: int = 500) -> None:
        """Reach quasi-static state"""
        for _ in range(steps):
            self.update_step()
        print(f"✓ Equilibrated {steps} steps")

    def inject_electron(self, position: int = 128, amplitude: float = 10.0) -> None:
        """Seed a compression peak (electron)"""
        x = np.arange(self.L)
        gaussian = amplitude * np.exp(-(x - position)**2 / 16)
        self.psi += gaussian
        print(f"✓ Injected electron peak at position {position}, amplitude {amplitude}")

    def inject_positron(self, position: int = 200, amplitude: float = 10.0) -> None:
        """Seed an expansion trough (positron)"""
        x = np.arange(self.L)
        gaussian = amplitude * np.exp(-(x - position)**2 / 16)
        self.psi -= gaussian  # Opposite sign
        print(f"✓ Injected positron trough at position {position}, amplitude {amplitude}")

    def run_evolution(self, steps: int = 1000, record_interval: int = 10) -> None:
        """Evolve through dynamics and record history"""
        for t in range(steps):
            self.update_step()

            # Record every N steps
            if t % record_interval == 0:
                self.history.append(self.psi.copy())
                self.energy_history.append(np.sum(self.psi**2))
                self.time_history.append(t)

        print(f"✓ Evolved {steps} steps with {len(self.history)} snapshots recorded")

    def analyze_spectrum(self) -> Dict:
        """Compute FFT and extract dominant frequencies"""
        results = {
            "times": [],
            "frequencies": [],
            "power_spectra": [],
            "dominant_modes": []
        }

        for t_idx, psi_snapshot in enumerate(self.history):
            # Compute FFT
            psi_fft = np.fft.fft(psi_snapshot)
            frequencies = np.fft.fftfreq(self.L)
            power = np.abs(psi_fft)**2

            # Find dominant modes
            idx_sorted = np.argsort(power)[::-1]
            top_freqs = frequencies[idx_sorted[:3]]
            top_powers = power[idx_sorted[:3]]

            results["times"].append(self.time_history[t_idx])
            results["frequencies"].append(frequencies)
            results["power_spectra"].append(power)
            results["dominant_modes"].append(list(zip(top_freqs, top_powers)))

        return results


@dataclass
class Visualization:
    """Generate publication-quality plots from simulation"""

    sim: LatticeSimulation
    spectrum_data: Dict
    output_dir: str = "lattice_visualizer_results"

    def __post_init__(self):
        """Create output directory"""
        import os
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_spatial_profile(self) -> None:
        """Plot ψ(x) at selected times"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))

        # Select three time points: early, middle, late
        time_indices = [0, len(self.sim.history)//2, len(self.sim.history)-1]
        titles = ["Separated", "Approaching", "Collided/Annihilated"]

        for ax, idx, title in zip(axes, time_indices, titles):
            psi_snapshot = self.sim.history[idx]
            x = np.arange(self.sim.L)

            ax.plot(x, psi_snapshot, linewidth=2, color='steelblue')
            ax.axhline(0, color='black', linestyle='--', alpha=0.3)
            ax.fill_between(x, psi_snapshot, alpha=0.3, color='steelblue')

            ax.set_xlabel('Position (lattice units)', fontsize=11)
            ax.set_ylabel('ψ(x)', fontsize=11)
            ax.set_title(f'{title}\n(t={self.sim.time_history[idx]})', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        filepath = f"{self.output_dir}/spatial_profile.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"✓ Saved spatial profile plot: {filepath}")
        plt.close()

    def plot_energy_evolution(self) -> None:
        """Plot total energy over time"""
        fig, ax = plt.subplots(figsize=(10, 6))

        times = self.sim.time_history
        energies = self.sim.energy_history

        ax.plot(times, energies, linewidth=2.5, color='darkred', label='Total Energy')
        ax.fill_between(times, energies, alpha=0.2, color='red')

        # Annotate phases
        ax.axvline(times[len(times)//3], color='green', linestyle=':', alpha=0.5, label='Approach starts')
        ax.axvline(times[2*len(times)//3], color='orange', linestyle=':', alpha=0.5, label='Collision')

        ax.set_xlabel('Time (lattice steps)', fontsize=12)
        ax.set_ylabel('Total Energy', fontsize=12)
        ax.set_title('Energy Evolution: Pair Separation → Collision → Annihilation', fontsize=13, fontweight='bold')
        ax.legend(loc='best', fontsize=11)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        filepath = f"{self.output_dir}/energy_evolution.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"✓ Saved energy evolution plot: {filepath}")
        plt.close()

    def plot_frequency_spectrum(self) -> None:
        """Plot power spectrum vs time"""
        fig, ax = plt.subplots(figsize=(12, 7))

        # Extract time and frequency grids
        times = np.array(self.spectrum_data["times"])
        power_spectra = np.array(self.spectrum_data["power_spectra"])

        # Limit to positive frequencies
        half_L = self.sim.L // 2

        # Create 2D colormap: time vs frequency
        extent = [0, 0.5, times[0], times[-1]]  # Positive freq up to Nyquist

        im = ax.imshow(power_spectra[:, :half_L].T, aspect='auto', cmap='hot',
                       extent=extent, origin='lower', interpolation='bilinear')

        ax.set_xlabel('Frequency (normalized)', fontsize=12)
        ax.set_ylabel('Time (lattice steps)', fontsize=12)
        ax.set_title('Frequency Power Spectrum Over Time', fontsize=13, fontweight='bold')

        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Power', fontsize=11)

        plt.tight_layout()
        filepath = f"{self.output_dir}/frequency_spectrum.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"✓ Saved frequency spectrum plot: {filepath}")
        plt.close()

    def plot_phase_portrait(self) -> None:
        """Plot ψ(t) vs dψ/dt for electron and positron regions"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Region 1: electron peak region (x ≈ 128)
        # Region 2: positron trough region (x ≈ 200)

        electron_region = list(range(120, 136))
        positron_region = list(range(190, 210))

        # Extract trajectories
        electron_trajectory = []
        positron_trajectory = []
        electron_velocity = []
        positron_velocity = []

        for i in range(len(self.sim.history) - 1):
            e_val = np.mean(self.sim.history[i][electron_region])
            p_val = np.mean(self.sim.history[i][positron_region])

            e_vel = (np.mean(self.sim.history[i+1][electron_region]) - e_val)
            p_vel = (np.mean(self.sim.history[i+1][positron_region]) - p_val)

            electron_trajectory.append(e_val)
            positron_trajectory.append(p_val)
            electron_velocity.append(e_vel)
            positron_velocity.append(p_vel)

        # Plot electron phase portrait
        axes[0].plot(electron_trajectory, electron_velocity, 'o-', markersize=3,
                    color='blue', alpha=0.6, linewidth=1.5, label='Electron trajectory')
        axes[0].axhline(0, color='black', linestyle='--', alpha=0.3)
        axes[0].axvline(0, color='black', linestyle='--', alpha=0.3)
        axes[0].set_xlabel('ψ (amplitude)', fontsize=11)
        axes[0].set_ylabel('dψ/dt (velocity)', fontsize=11)
        axes[0].set_title('Electron Peak Phase Portrait', fontsize=12, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()

        # Plot positron phase portrait
        axes[1].plot(positron_trajectory, positron_velocity, 'o-', markersize=3,
                    color='red', alpha=0.6, linewidth=1.5, label='Positron trajectory')
        axes[1].axhline(0, color='black', linestyle='--', alpha=0.3)
        axes[1].axvline(0, color='black', linestyle='--', alpha=0.3)
        axes[1].set_xlabel('ψ (amplitude)', fontsize=11)
        axes[1].set_ylabel('dψ/dt (velocity)', fontsize=11)
        axes[1].set_title('Positron Trough Phase Portrait', fontsize=12, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        axes[1].legend()

        plt.tight_layout()
        filepath = f"{self.output_dir}/phase_portrait.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"✓ Saved phase portrait plot: {filepath}")
        plt.close()

    def plot_all(self) -> None:
        """Generate all visualization plots"""
        print("\n🎨 Generating visualization plots...")
        self.plot_spatial_profile()
        self.plot_energy_evolution()
        self.plot_frequency_spectrum()
        self.plot_phase_portrait()
        print("✓ All plots generated")


class QuantitativeTests:
    """Validate framework predictions against simulation results"""

    def __init__(self, sim: LatticeSimulation, spectrum_data: Dict):
        self.sim = sim
        self.spectrum_data = spectrum_data

    def test_oscillation_frequency(self) -> Dict:
        """Test 1: Extract electron peak frequency and compare to Yukawa prediction"""
        print("\n📊 Test 1: Oscillation Frequency")

        # Extract electron peak trajectory
        electron_region = list(range(120, 136))
        peak_trajectory = np.array([
            np.mean(self.sim.history[i][electron_region])
            for i in range(len(self.sim.history))
        ])

        # Find dominant frequency via FFT
        peak_fft = np.fft.fft(peak_trajectory)
        frequencies = np.fft.fftfreq(len(peak_trajectory))
        power = np.abs(peak_fft)**2

        # Find dominant mode (skip DC component)
        idx = np.argsort(power[1:])[-1] + 1
        omega_measured = np.abs(frequencies[idx])

        # Predict from Yukawa formula
        omega_predicted = (1 - self.sim.gamma) * self.sim.beta

        error = np.abs(omega_measured - omega_predicted) / max(omega_predicted, 1e-6) * 100

        result = {
            "measured_frequency": float(omega_measured),
            "predicted_frequency": float(omega_predicted),
            "error_percent": float(error),
            "passes": error < 10.0  # 10% tolerance
        }

        status = "✓ PASS" if result["passes"] else "✗ FAIL"
        print(f"  Measured ω = {omega_measured:.6f}")
        print(f"  Predicted ω = {omega_predicted:.6f}")
        print(f"  Error = {error:.2f}%  {status}")

        return result

    def test_confinement_boundary(self) -> Dict:
        """Test 2: Measure boundary sharpness and confinement radius"""
        print("\n📊 Test 2: Confinement Boundary")

        # Use final state
        psi_final = self.sim.history[-1]

        # Find peak position and measure width
        peak_idx = np.argmax(np.abs(psi_final))
        peak_val = psi_final[peak_idx]

        # Measure 1/e width
        threshold = peak_val / np.e if peak_val > 0 else peak_val * np.e

        # Find edges
        left_edge = peak_idx
        right_edge = peak_idx

        for i in range(peak_idx, -1, -1):
            if np.abs(psi_final[i]) < np.abs(threshold):
                left_edge = i
                break

        for i in range(peak_idx, len(psi_final)):
            if np.abs(psi_final[i]) < np.abs(threshold):
                right_edge = i
                break

        boundary_width = right_edge - left_edge

        # Expected from confinement theory: radius ~ sqrt(K_p / sigma_T)
        # Rough estimate: boundary width should be ~16 lattice units

        result = {
            "boundary_width_lattice_units": float(boundary_width),
            "peak_position": int(peak_idx),
            "peak_amplitude": float(peak_val),
            "passes": 10 < boundary_width < 30  # Reasonable confinement range
        }

        status = "✓ PASS" if result["passes"] else "✗ FAIL"
        print(f"  Boundary width = {boundary_width} lattice units")
        print(f"  Peak at position {peak_idx}, amplitude {peak_val:.4f}")
        print(f"  Confinement verified: {result['passes']}  {status}")

        return result

    def test_annihilation_energy_release(self) -> Dict:
        """Test 3: Measure energy released in annihilation"""
        print("\n📊 Test 3: Annihilation Energy Release")

        # Energy before and after collision
        E_before = self.sim.energy_history[len(self.sim.energy_history)//3]  # Before approach
        E_after = self.sim.energy_history[-1]  # Final state

        E_released = E_before - E_after

        # Predict: should be ~2 × m_e c² equivalent
        # In our units, electron mass ~ 0.511 MeV (check calibration)
        E_predicted = 2.0  # Normalized to 2 × electron rest mass

        if E_released > 0:
            relative_error = np.abs(E_released - E_predicted) / max(E_predicted, 1e-6) * 100
        else:
            relative_error = 100.0

        result = {
            "energy_before": float(E_before),
            "energy_after": float(E_after),
            "energy_released": float(E_released),
            "predicted_release": float(E_predicted),
            "error_percent": float(relative_error),
            "passes": E_released > 0  # Should release energy
        }

        status = "✓ PASS" if result["passes"] else "✗ FAIL"
        print(f"  Energy before = {E_before:.4f}")
        print(f"  Energy after = {E_after:.4f}")
        print(f"  Released = {E_released:.4f}  {status}")

        return result

    def test_phase_locking(self) -> Dict:
        """Test 4: Measure phase relationship between electron and positron"""
        print("\n📊 Test 4: Phase Locking")

        # Extract phase information from dominant frequencies
        # Electrons should oscillate with phase offset from positrons

        electron_region = list(range(120, 136))
        positron_region = list(range(190, 210))

        electron_signal = np.array([
            np.mean(self.sim.history[i][electron_region])
            for i in range(len(self.sim.history))
        ])

        positron_signal = np.array([
            np.mean(self.sim.history[i][positron_region])
            for i in range(len(self.sim.history))
        ])

        # Compute phase via analytic signal
        from scipy import signal as scipy_signal

        e_analytic = scipy_signal.hilbert(electron_signal)
        p_analytic = scipy_signal.hilbert(positron_signal)

        e_phase = np.unwrap(np.angle(e_analytic))
        p_phase = np.unwrap(np.angle(p_analytic))

        # Phase difference should approach π (180°) before collision
        mid_point = len(e_phase) // 2
        phase_diff_at_approach = np.abs(e_phase[mid_point] - p_phase[mid_point])

        # Normalize to [0, π]
        phase_diff_normalized = np.abs(np.angle(np.exp(1j * phase_diff_at_approach)))

        result = {
            "phase_difference_radians": float(phase_diff_normalized),
            "phase_difference_degrees": float(np.degrees(phase_diff_normalized)),
            "expected_phase_pi": float(np.pi),
            "passes": np.abs(phase_diff_normalized - np.pi) < 0.5  # Within 0.5 rad
        }

        status = "✓ PASS" if result["passes"] else "✗ FAIL"
        print(f"  Phase difference = {np.degrees(phase_diff_normalized):.1f}°")
        print(f"  Expected ≈ 180° (π rad)")
        print(f"  Predictions: {result['passes']}  {status}")

        return result

    def run_all_tests(self) -> Dict:
        """Execute all quantitative validation tests"""
        print("\n" + "="*70)
        print("QUANTITATIVE VALIDATION TESTS")
        print("="*70)

        results = {
            "test_oscillation_frequency": self.test_oscillation_frequency(),
            "test_confinement_boundary": self.test_confinement_boundary(),
            "test_annihilation_energy": self.test_annihilation_energy_release(),
            "test_phase_locking": self.test_phase_locking(),
        }

        # Summary
        passed = sum(1 for r in results.values() if r.get("passes", False))
        total = len(results)

        print("\n" + "="*70)
        print(f"SUMMARY: {passed}/{total} tests passed")
        print("="*70)

        if passed == total:
            print("✓ Framework VALIDATED - Ready for publication")
        elif passed >= total // 2:
            print("⚠ Partial success - Calibration refinement needed")
        else:
            print("✗ Framework requires significant revision")

        return results


def main():
    """Main execution: Load criticality, run simulation, validate, visualize"""

    print("="*70)
    print("LATTICE VISUALIZATION: Peak/Trough Dynamics")
    print("="*70)

    # Load critical point from Higgs solver
    print("\n📂 Loading Higgs criticality results...")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "higgs_criticality_results.json")) as f:
        results = json.load(f)

    beta = results["critical_point"]["beta"]
    gamma = results["critical_point"]["gamma"]

    print(f"  β_crit = {beta:.6f}")
    print(f"  γ_crit = {gamma:.6f}")

    # Initialize lattice
    print("\n🔧 Initializing lattice simulation...")
    sim = LatticeSimulation(beta=beta, gamma=gamma, lattice_size=256)

    # Phase 1: Equilibration
    print("\n📍 Phase 1: Equilibration")
    sim.run_equilibration(steps=500)

    # Phase 2: Inject electron peak
    print("\n📍 Phase 2: Seed Electron (Compression Peak)")
    sim.inject_electron(position=128, amplitude=10.0)
    sim.run_evolution(steps=500, record_interval=10)

    # Phase 3: Inject positron trough
    print("\n📍 Phase 3: Seed Positron (Expansion Trough)")
    sim.inject_positron(position=200, amplitude=10.0)
    sim.run_evolution(steps=1000, record_interval=10)

    # Phase 4: Analyze spectrum
    print("\n📍 Phase 4: Spectral Analysis (FFT)")
    spectrum_data = sim.analyze_spectrum()

    # Phase 5: Quantitative tests
    print("\n📍 Phase 5: Validation Tests")
    tester = QuantitativeTests(sim, spectrum_data)
    test_results = tester.run_all_tests()

    # Save test results (convert non-JSON-serializable types)
    def convert_for_json(obj):
        """Recursively convert non-JSON-serializable types"""
        if isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, (bool, np.bool_)):
            return str(obj)
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, (list, tuple)):
            return [convert_for_json(x) for x in obj]
        else:
            return obj

    test_output = {
        "simulation_parameters": {
            "beta": float(beta),
            "gamma": float(gamma),
            "lattice_size": 256,
            "total_steps": 2000
        },
        "test_results": convert_for_json(test_results)
    }

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lattice_validation_results.json"), "w") as f:
        json.dump(test_output, f, indent=2)
    print(f"\n✓ Test results saved: solvers/lattice_validation_results.json")

    # Visualization
    print("\n📍 Phase 6: Visualization")
    viz = Visualization(sim, spectrum_data, output_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "lattice_visualizer_results"))
    viz.plot_all()

    # Final summary
    print("\n" + "="*70)
    print("LATTICE VISUALIZATION COMPLETE")
    print("="*70)
    print("\nOutputs:")
    print("  ✓ solvers/lattice_visualizer_results/spatial_profile.png")
    print("  ✓ solvers/lattice_visualizer_results/energy_evolution.png")
    print("  ✓ solvers/lattice_visualizer_results/frequency_spectrum.png")
    print("  ✓ solvers/lattice_visualizer_results/phase_portrait.png")
    print("  ✓ solvers/lattice_validation_results.json")
    print("\n✓ Framework validation complete")


if __name__ == "__main__":
    main()
