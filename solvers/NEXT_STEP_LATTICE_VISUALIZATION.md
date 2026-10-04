# Next Implementation: Lattice Visualization of Peak/Trough Dynamics

## Objective

Visualize the actual dynamics of the displacement field ψ as it forms:
1. **Compression peaks** (electrons)
2. **Expansion troughs** (positrons)
3. **Pair production** (photon deformation → dipole creation)
4. **Annihilation** (peak + trough overlap → phase cancellation)

## Implementation Plan

### Step 1: Initialize 1D Lattice with Higgs Parameters

```python
# From higgs_criticality_solver.py results:
beta = 0.891379
gamma = 0.096552
lattice_size = 256  # Points
time_steps = 1000   # Iterations

# Initialize field
psi = np.random.randn(lattice_size) * 0.01  # Small random perturbation

# Run the core update rule
for t in range(time_steps):
    psi_new = psi + (1 - gamma) * (psi - psi_prev) + beta * (neighbor_avg - psi)
    psi_prev = psi
    psi = psi_new
    
    # Record every 10th step
    if t % 10 == 0:
        history[t//10] = psi.copy()
```

### Step 2: Inject Perturbation to Seed Electron Formation

```python
# After reaching quasi-static state, inject a compression peak
# at position i=128
energy = 10.0  # Perturbation amplitude

psi[128] += energy * np.exp(-(np.arange(lattice_size) - 128)**2 / 16)

# Evolve and observe: Does a stable bounded knot form?
for t in range(time_steps):
    # Standard update + record
    ...
```

**Expected outcome:**
- Peak remains localized at center
- Boundary develops sharp transition (surface tension)
- Oscillates with frequency ω ≈ (1-γ)β^(1/1) [from Yukawa solver]

### Step 3: Inject Opposing Perturbation to Create Positron

```python
# Create expansion trough at i=200 (opposite side)
psi[200] -= energy * np.exp(-(np.arange(lattice_size) - 200)**2 / 16)

# Evolve with both peak and trough present
for t in range(time_steps):
    # Record separated evolution, then approach
    ...
```

**Expected outcome:**
- Two bounded knots exist separately
- Phase-locking energy κ_T slightly couples them
- Can observe "phase separation" (preferred distance)

### Step 4: Collision Dynamics

```python
# After both knots stabilize, force them to approach
# by modifying the external potential
for t in range(approach_steps):
    # Gradually move peak leftward, trough rightward
    external_force = collision_strength * np.tanh((t - t_mid) / collision_width)
    psi_new = update_with_external_force(psi, external_force)
    
# Continue evolution as they collide
for t in range(collision_steps):
    psi = standard_update(psi)
    
    # Track: total energy, overlap integral, oscillation frequency
    energy[t] = compute_total_energy(psi)
    overlap[t] = np.dot(psi[peak_region], psi[trough_region])
```

**Expected outcome:**
- Peak and trough approach
- Overlap increases
- Total energy released
- Final state: nearly cancelled field at collision site
- Gamma ray (high-frequency oscillation) propagates away

### Step 5: Harmonic Mode Analysis

```python
# Compute Fourier transform at each time step
import scipy.fft

psi_fft = scipy.fft.fft(psi, axis=1)
frequencies = scipy.fft.fftfreq(lattice_size)

# Track which modes are excited
for t in range(time_steps):
    power_spectrum[t] = np.abs(psi_fft[t])**2
    
# Plot: time vs frequency vs power
# Look for:
# - Fundamental mode (ℓ=0) — localized
# - Dipole mode (ℓ=1) — oscillating
# - Radiation modes — traveling away
```

**Expected outcome:**
- Electron shows dominant oscillation at fundamental frequency
- Positron shows same frequency (same knot size/damping)
- Collision excites high-frequency modes (gamma radiation)

## Visualization Outputs

### Plot 1: Spatial Profile Over Time
```
ψ(x) at selected times
    |
  +1|        ╱╲              ╱╲
    |       ╱  ╲            ╱  ╲
    |   ───╱    ╲──────────╱    ╲──
  0 |─────────────────────────────
    |              ╲      ╱
 -1|               ╲╱╲  ╱╲
    |                ╱╲╱
    └──────────────────────→ x

Time: 0 (separated)     Time: 500 (approaching)    Time: 1000 (collided)
```

### Plot 2: Energy Evolution
```
Total E
  |      ╱╲
  |     ╱  ╲────┐
  |    ╱        ├─ Released energy
  |   ╱         │  ↓ Gamma rays
  |──╱──────────┴──────
  └─────────────────→ time
    sep  approach  collision  propagation
```

### Plot 3: Frequency Spectrum
```
Power spectrum P(ω,t)

Frequency
  |  ☆ High freq (gamma ray, appears at collision)
  |  ★ Fundamental (electron/positron oscillation)
  |  ⋮ Harmonics (coupling modes)
  |
  └─────────────────→ time
```

### Plot 4: Phase Space
```
ψ(t) vs dψ/dt for each particle
    
    dψ/dt
     |    Electron peak
     |     •→•→•
     |      ╲ ╱
    0├────•─╳─•──── ψ
     |  ╱  ╲•╱  ╲
     | •    ╳    • Positron trough
     |  ╲  ╱ ╲  ╱
    -|   ╲•←•←•
     |
     └────────────→ ψ
     
Closed loops = oscillating modes
X = collision point
```

## Code Structure

```
solvers/
├── lattice_visualizer.py
│   ├── class LatticeSimulation
│   │   ├── initialize(beta, gamma, lattice_size)
│   │   ├── update_step()
│   │   ├── inject_perturbation(position, amplitude)
│   │   ├── run_collision(steps)
│   │   └── analyze_spectrum()
│   │
│   ├── class Visualization
│   │   ├── plot_spatial_profile(times)
│   │   ├── plot_energy_evolution()
│   │   ├── plot_frequency_spectrum()
│   │   ├── animate_collision()
│   │   └── save_frames(output_dir)
│   │
│   └── main()
│       ├── Load (β, γ) from higgs_criticality_results.json
│       ├── Initialize lattice
│       ├── Seed electron (compression peak)
│       ├── Seed positron (expansion trough)
│       ├── Run collision
│       ├── Analyze and plot
│       └── Save all outputs
│
└── lattice_visualizer_results/
    ├── collision_history.npy  (full time evolution)
    ├── frequency_spectrum.png
    ├── energy_plot.png
    ├── phase_portrait.png
    ├── collision_animation.mp4
    └── README.md (interpretation)
```

## Quantitative Tests

### Test 1: Oscillation Frequency
```python
# Extract electron peak frequency
peak_trajectory = psi[:, peak_region].mean(axis=1)
freqs = compute_dominant_frequency(peak_trajectory)

# Predict from Yukawa formula
omega_predicted = (1 - gamma) * beta ** 1.0
omega_from_mass = electron_mass / (0.511 MeV)  # Convert

assert np.abs(freqs[0] - omega_predicted) < 0.01, "Frequency mismatch"
```

**Prediction:** ω_electron ≈ 0.903 × 0.891 ≈ 0.805 (in lattice units)

### Test 2: Confinement Boundary
```python
# Measure boundary sharpness
boundary_width = compute_knot_radius()  # Where ψ drops by 1/e

# Predict from surface tension
radius_predicted = np.sqrt(K_p / (sigma_T))  # Geometry

assert np.abs(boundary_width - radius_predicted) < 0.1 fm
```

**Prediction:** Electron radius ≈ 0.8 fm (classical electron radius ≈ 2.8e-15 m)

### Test 3: Annihilation Energy Release
```python
# Total energy before collision
E_before = E_electron + E_positron

# Total energy after collision (should be nearly zero field)
E_after = sum(ψ_final**2) / lattice_size

# Energy released = radiated as gamma rays
E_released = E_before - E_after

# Predict from mass formula
E_predicted = 2 * electron_mass * c**2  # = 2 × 0.511 MeV

assert np.abs(E_released - E_predicted) < 0.1 MeV
```

**Prediction:** γ-ray energy ≈ 1.022 MeV

### Test 4: Phase Locking
```python
# Measure phase relationship between electron and positron before collision
phase_electron = np.angle(np.fft.fft(psi_electron))
phase_positron = np.angle(np.fft.fft(psi_positron))
phase_difference = np.abs(phase_electron - phase_positron)

# Predict: Should be π (opposite phases)
assert np.abs(phase_difference[0] - np.pi) < 0.1
```

**Prediction:** Electron and positron oscillate 180° out of phase

## Expected Discoveries

1. **Peak/Trough Dynamics Visualized**
   - Shows particles as field excitations, not point objects
   - Boundary formation visible (confinement geometry)
   - Oscillation pattern reveals internal structure

2. **Quantitative Confirmation**
   - Frequency matches Yukawa predictions ✓ or ✗
   - Boundary radius matches hadron geometry ✓ or ✗
   - Annihilation energy matches 2m_e c² ✓ or ✗

3. **Refinement Targets**
   - If frequencies off: adjust MASS_SCALE_FACTOR in Yukawa solver
   - If radius off: recalibrate surface tension σ_T
   - If energy off: check four-interaction hold accounting

4. **New Predictions**
   - Gamma ray spectrum (should show Bremsstrahlung profile)
   - Neutral particle creation (pions?) from collision
   - Pair production threshold confirmation (E > 2m_e c²)

## Timeline

- **Phase 1 (week 1):** Implement basic lattice update + visualization
- **Phase 2 (week 2):** Single particle formation + frequency confirmation
- **Phase 3 (week 3):** Pair production + collision dynamics
- **Phase 4 (week 4):** Spectral analysis + publication-quality plots
- **Phase 5 (week 5):** Compare all predictions to data + refine solvers

## Success Criteria

✓ Oscillating peak/trough patterns observed  
✓ Frequencies match Yukawa predictions (within 10%)  
✓ Confinement boundary matches hadron geometry  
✓ Annihilation energy ≈ 2m_e c²  
✓ Gamma radiation spectrum calculable from first principles  
✓ Pair production threshold confirmed  

**If all succeed:** Framework validated. Ready for publication.  
**If some fail:** Clear direction for refining (β, γ), K_p, σ_T calibration.

---

## Code Skeleton (Ready to Implement)

```python
#!/usr/bin/env python3
"""Lattice visualization of peak/trough dynamics"""

import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class LatticeSimulation:
    def __init__(self, beta, gamma, lattice_size=256):
        self.beta = beta
        self.gamma = gamma
        self.L = lattice_size
        self.psi = np.random.randn(lattice_size) * 0.01
        self.psi_prev = self.psi.copy()
        self.history = []
        self.energy_history = []
        
    def update_step(self):
        """Execute one update of the core rule"""
        neighbor_avg = np.roll(self.psi, 1) + np.roll(self.psi, -1)
        neighbor_avg /= 2
        
        psi_new = (self.psi + 
                   (1 - self.gamma) * (self.psi - self.psi_prev) + 
                   self.beta * (neighbor_avg - self.psi))
        
        self.psi_prev = self.psi.copy()
        self.psi = psi_new
        
        return self.psi.copy()
    
    def run_equilibration(self, steps=500):
        """Reach quasi-static state"""
        for _ in range(steps):
            self.update_step()
    
    def inject_electron(self, position=128, amplitude=10.0):
        """Seed a compression peak"""
        x = np.arange(self.L)
        gaussian = amplitude * np.exp(-(x - position)**2 / 16)
        self.psi += gaussian
    
    def inject_positron(self, position=200, amplitude=10.0):
        """Seed an expansion trough"""
        x = np.arange(self.L)
        gaussian = amplitude * np.exp(-(x - position)**2 / 16)
        self.psi -= gaussian  # Opposite sign
    
    def run_collision(self, steps=1000):
        """Evolve through collision"""
        for t in range(steps):
            self.update_step()
            self.history.append(self.psi.copy())
            self.energy_history.append(np.sum(self.psi**2))
    
    def visualize(self):
        """Generate all plots"""
        # [Plotting code here]
        pass

# Main execution
if __name__ == "__main__":
    # Load critical point
    with open("solvers/higgs_criticality_results.json") as f:
        results = json.load(f)
    
    beta = results["critical_point"]["beta"]
    gamma = results["critical_point"]["gamma"]
    
    # Run simulation
    sim = LatticeSimulation(beta, gamma)
    sim.run_equilibration()
    sim.inject_electron()
    sim.inject_positron()
    sim.run_collision()
    sim.visualize()
    
    print("✓ Lattice visualization complete")
```

This is the immediate next step to validate the framework.
