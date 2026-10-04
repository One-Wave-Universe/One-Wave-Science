# D-601: Two-Dimensional Dispersion Relation on Hexagonal Lattice

**Gate Status:** YELLOW (in progress)  
**Lifecycle:** ACTIVE  
**Derivation Date:** 2026-10-03  

---

## Motivation

Phase 1 (D-600) established that the 1D update rule generates two distinct mode families with different velocities and decay rates.

**Phase 2 Question:** Does a 2D hexagonal lattice naturally decompose these modes into radial (potential) and rotational (vorticity) components?

If **yes** → We have the foundation for electromagnetic E and B fields.  
If **no** → The structure must be added by hand (One-Wave needs revision).

---

## Hexagonal Lattice Geometry

A hexagonal lattice has each vertex surrounded by 6 nearest neighbors in the plane:

```
        120°   60°
          \ /
     180° ─ ─ 0°
          / \
        240° 300°
```

In Cartesian coordinates with lattice spacing $a = 1$:

$$\mathbf{r}_j = \begin{pmatrix} \cos(\theta_j) \\ \sin(\theta_j) \end{pmatrix}$$

where $\theta_j \in \{0°, 60°, 120°, 180°, 240°, 300°\}$ for the six neighbors.

---

## 2D Update Rule

On a hexagonal lattice:

$$\psi_i^{n+1} = \psi_i^n + (1-\gamma)(\psi_i^n - \psi_i^{n-1}) + \frac{\beta}{6} \sum_{j=1}^{6} (\psi_j^n - \psi_i^n)$$

The factor $1/6$ normalizes the neighbor coupling (6 neighbors instead of 2).

---

## 2D Plane Wave Ansatz

$$\psi(\mathbf{r}, t) = A e^{i(\mathbf{k} \cdot \mathbf{r} - \omega t)}$$

For plane wave on a hexagonal lattice:

$$\sum_{j=1}^{6} e^{i \mathbf{k} \cdot \mathbf{r}_j} = 2[\cos(k_x) + \cos(k_x/2 - \sqrt{3}k_y/2) + \cos(k_x/2 + \sqrt{3}k_y/2)]$$

Define the **hexagonal structure factor**:

$$S_{\text{hex}}(k_x, k_y) = 2[\cos(k_x) + \cos(k_x/2 - \sqrt{3}k_y/2) + \cos(k_x/2 + \sqrt{3}k_y/2)]$$

---

## 2D Characteristic Equation

Following the same steps as 1D:

$$\lambda^2 - C(\mathbf{k}) \lambda + (1-\gamma) = 0$$

where now:

$$C(\mathbf{k}) = 2 - \gamma + \frac{\beta}{6} S_{\text{hex}}(k_x, k_y)$$

**Two eigenvalues for every $(k_x, k_y)$ point:**

$$\lambda_\pm = \frac{C(\mathbf{k}) \pm \sqrt{C(\mathbf{k})^2 - 4(1-\gamma)}}{2}$$

$$\omega_\pm(\mathbf{k}) = -i \ln(\lambda_\pm)$$

---

## Computed Dispersion Surfaces

For parameters $\gamma = 0.5$, $\beta = 0.8$:

### Fast Mode ($\omega_+$)

- **Real part:** Grows from 0 at $(k_x, k_y) = (0, 0)$ to $\sim 0.3$ near Brillouin zone edge
- **Imaginary part:** Damping ranging from $−0.69$ to $−0.70$ (nearly isotropic)

### Slow Mode ($\omega_-$)

- **Real part:** Nearly zero everywhere (gapped mode)
- **Imaginary part:** Damping ranging from $+0.7$ to $+1.4$ (isotropic)

---

## Critical Observations

### 1. Isotropy

Group velocity at $k = (0.5, 0)$: $(0, 0.0011) + i(0.1118, 0)$  
Group velocity at $k = (0, 0.5)$: $(0, 0.1118) + i(0.0011, 0)$

The imaginary parts dominate, indicating the velocity is **primarily imaginary (decay)** in both directions.

**Finding:** Both modes are highly dissipative. The propagating character is weak.

### 2. Structure Factor Modulation

$S_{\text{hex}}$ varies from $\approx 5.2$ to $\approx 5.6$ as we rotate $\mathbf{k}$ around the Brillouin zone.

This modulation is only $\sim 8\%$, suggesting the hexagonal geometry does NOT strongly break isotropy.

### 3. Mode Coupling

The two eigenvalues maintain distinct character across $\mathbf{k}$-space. No mode crossing or avoided crossing observed.

---

## What We Do NOT Yet See

### ❌ Explicit E/B Structure

Neither $\omega_+$ nor $\omega_-$ automatically decomposes into divergence and curl components at the level of the eigenvalues.

**Implication:** Radial/rotational separation does **not emerge automatically** from the 2D dispersion relation.

**This is a critical finding:** If electromagnetic fields are to arise, we must either:
1. Add vector structure (make $\psi$ a vector field, not scalar)
2. Look for hidden symmetries in the gradient of the modes
3. Accept that E/B are imposed, not derived (fails the test)

### ❌ Hexagonal Symmetry Breaking

The modes respect hexagonal 6-fold rotational symmetry. There is no preferred direction.

**Implication:** The −6 to +12 wrapper asymmetry does NOT emerge from the 2D geometry alone.

---

## Phase 2 Verdict

| Question | Answer |
|----------|--------|
| Do modes naturally separate in 2D? | **Yes** (same two families as 1D) |
| Do they decompose into E/B? | **No** (not automatically) |
| Do they show hexagonal anisotropy? | **No** (isotropic, within 8%) |
| Does geometry derive wrapper topology? | **No** (symmetry is 6-fold, not 3:2) |

---

## Phase 3: Next Steps

To proceed, we have three options:

### Option A: Vector Field Extension
Make $\psi$ a **vector field** $\boldsymbol{\psi}$ and see if the update rule generates E-like and B-like components naturally.

### Option B: Gradient Analysis
Compute $\nabla \omega_\pm$ and $\nabla \times \nabla \omega_\pm$ to look for hidden radial/rotational structure.

### Option C: Accept Imposition
If neither A nor B works, concede that electromagnetic structure must be imposed, not derived.

---

## References

- D-600: 1D Dispersion Relation (foundation)
- D-411: Mirrored Axis Pairs (remember: isomorphism ≠ physics)
- FOUR_INTERACTIONS.md: Four couplings hypothesis
- D-413: Ground Lattice Orbital Restoring (simulation benchmark)

