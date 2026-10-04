"""
Track B: Discrete Differential Operators on Hexagonal Lattice
==============================================================

Implement discrete curl, divergence, and gradient on 2D hexagonal lattice.

The lattice has 6 neighbors per site at equal distances, arranged at 60° intervals:
  Neighbor offsets: (1,0), (0,1), (-1,1), (-1,0), (0,-1), (1,-1)

  These correspond to directions:
    0°:   (1, 0)
    60°:  (0, 1)
    120°: (-1, 1)
    180°: (-1, 0)
    240°: (0, -1)
    300°: (1, -1)

Key properties we must preserve:
  1. ∇·(∇×F) ≡ 0  (no monopoles)
  2. Symmetry under 60° rotations
  3. Convergence to continuum limit as lattice spacing a → 0
"""

import math
from typing import Dict, List, Sequence, Tuple
import sys

# Assuming hex_lattice_graph is in the same directory or importable
try:
    from hex_lattice_graph import (
        Site, NEIGHBOR_OFFSETS, AXIS_PAIRS, neighbor, adjacency, site_xy
    )
except ImportError:
    # Fallback definitions if import fails
    Site = Tuple[int, int]
    NEIGHBOR_OFFSETS = (
        (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1),
    )
    AXIS_PAIRS = (
        ((1, 0), (-1, 0)),
        ((0, 1), (0, -1)),
        ((-1, 1), (1, -1)),
    )

    def neighbor(site: Site, offset: Site) -> Site:
        return (site[0] + offset[0], site[1] + offset[1])

    def adjacency(sites: Sequence[Site]) -> Dict[Site, List[Site]]:
        present = set(sites)
        adj: Dict[Site, List[Site]] = {}
        for site in sites:
            nbrs = [neighbor(site, off) for off in NEIGHBOR_OFFSETS
                   if neighbor(site, off) in present]
            adj[site] = nbrs
        return adj

    def site_xy(site: Site, a: float = 1.0) -> Tuple[float, float]:
        A1 = (1.0, 0.0)
        A2 = (0.5, math.sqrt(3.0) / 2.0)
        m, n = site
        return (a * (m * A1[0] + n * A2[0]), a * (m * A1[1] + n * A2[1]))


# ============================================================================
# PART 1: Neighbor Direction Vectors (Physical)
# ============================================================================

def neighbor_directions(a: float = 1.0) -> List[Tuple[float, float]]:
    """
    Return the physical (x, y) vectors pointing from origin to each of 6 neighbors.

    For hexagonal lattice with lattice constant a, these are unit vectors
    at 60° intervals.
    """
    dirs = []
    for offset in NEIGHBOR_OFFSETS:
        x, y = site_xy(offset, a=a)
        # Normalize to unit vectors
        r = math.sqrt(x*x + y*y)
        dirs.append((x/r, y/r))
    return dirs


def neighbor_outward_normals(a: float = 1.0) -> List[Tuple[float, float]]:
    """
    For a hexagon centered at origin, get the outward normal vector for each edge.

    The normal is perpendicular to the edge direction, pointing outward.
    For edge j to neighbor j, the normal is rotated 90° counterclockwise from
    the direction to the neighbor.
    """
    dirs = neighbor_directions(a)
    normals = []
    for dx, dy in dirs:
        # Rotate 90° counterclockwise: (x, y) -> (-y, x)
        nx, ny = -dy, dx
        normals.append((nx, ny))
    return normals


# ============================================================================
# PART 2: Discrete Divergence
# ============================================================================

def discrete_divergence(
    vector_field: Dict[Site, Tuple[float, float]],
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, float]:
    """
    Compute discrete divergence ∇·F at each site.

    For hexagonal lattice:
      ∇·F(i) ≈ (1/A_cell) ∑_{neighbors j} F_{ij} · n̂_{ij}

    where:
      - A_cell = area of Voronoi cell
      - F_{ij} = value of field at edge midpoint between i and j
      - n̂_{ij} = outward normal from cell

    On hexagonal lattice with unit spacing (a=1):
      A_cell = (3√3)/2 ≈ 2.598

    For simplicity, we approximate F_{ij} ≈ (F_j + F_i)/2 (average).
    """
    adj = adjacency(sites)
    normals = neighbor_outward_normals(a)
    a_hex = (3.0 * math.sqrt(3.0) / 2.0) * (a ** 2)  # Area of hexagonal cell

    div = {}
    for site in sites:
        if site not in vector_field:
            div[site] = 0.0
            continue

        f_i = vector_field[site]
        flux = 0.0

        for j, offset in enumerate(NEIGHBOR_OFFSETS):
            nbr = neighbor(site, offset)
            if nbr in vector_field:
                f_j = vector_field[nbr]
                # Average field at edge
                f_edge = ((f_i[0] + f_j[0])/2.0, (f_i[1] + f_j[1])/2.0)
                # Dot with outward normal
                n = normals[j]
                flux += f_edge[0] * n[0] + f_edge[1] * n[1]

        div[site] = flux / a_hex

    return div


# ============================================================================
# PART 3: Discrete Curl
# ============================================================================

def discrete_curl_z(
    vector_field: Dict[Site, Tuple[float, float]],
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, float]:
    """
    Compute discrete curl (z-component) ∇×F|_z at each site.

    For 2D vector field F = (F_x, F_y), the curl is a scalar:
      (∇×F)_z ≈ (∂F_y/∂x - ∂F_x/∂y)

    On hexagonal lattice:
      (∇×F)_z(i) ≈ (1/A_cell) ∮ F·t̂ dl

    where the integral is around the hexagon, and t̂ is tangential direction.

    We approximate this as:
      (1/A_cell) ∑_{neighbors j} F_{ij} · t̂_{ij} · (edge length)

    The tangential direction at edge j is perpendicular to the outward normal,
    rotated 90° clockwise: n̂ -> (n_y, -n_x).
    """
    adj = adjacency(sites)
    normals = neighbor_outward_normals(a)
    a_hex = (3.0 * math.sqrt(3.0) / 2.0) * (a ** 2)
    edge_length = a  # Distance to neighbor on hexagonal lattice

    curl = {}
    for site in sites:
        if site not in vector_field:
            curl[site] = 0.0
            continue

        f_i = vector_field[site]
        circulation = 0.0

        for j, offset in enumerate(NEIGHBOR_OFFSETS):
            nbr = neighbor(site, offset)
            if nbr in vector_field:
                f_j = vector_field[nbr]
                # Average field at edge
                f_edge = ((f_i[0] + f_j[0])/2.0, (f_i[1] + f_j[1])/2.0)

                # Tangential direction: rotate normal 90° clockwise
                n = normals[j]
                t = (n[1], -n[0])  # Clockwise rotation

                circulation += (f_edge[0] * t[0] + f_edge[1] * t[1]) * edge_length

        curl[site] = circulation / a_hex

    return curl


# ============================================================================
# PART 4: Discrete Gradient
# ============================================================================

def discrete_gradient(
    scalar_field: Dict[Site, float],
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, Tuple[float, float]]:
    """
    Compute discrete gradient ∇φ at each site.

    For scalar field φ:
      ∇φ(i) ≈ (1/A_cell) ∑_{neighbors j} φ_j · n̂_{ij}

    where n̂_{ij} is the outward normal on the hexagon cell.
    """
    adj = adjacency(sites)
    normals = neighbor_outward_normals(a)
    a_hex = (3.0 * math.sqrt(3.0) / 2.0) * (a ** 2)

    grad = {}
    for site in sites:
        if site not in scalar_field:
            grad[site] = (0.0, 0.0)
            continue

        grad_x, grad_y = 0.0, 0.0

        for j, offset in enumerate(NEIGHBOR_OFFSETS):
            nbr = neighbor(site, offset)
            if nbr in scalar_field:
                phi_j = scalar_field[nbr]
                n = normals[j]
                grad_x += phi_j * n[0]
                grad_y += phi_j * n[1]

        grad[site] = (grad_x / a_hex, grad_y / a_hex)

    return grad


# ============================================================================
# PART 5: Vector Laplacian (∇²F = ∇(∇·F) - ∇×(∇×F))
# ============================================================================

def discrete_laplacian_vector(
    vector_field: Dict[Site, Tuple[float, float]],
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, Tuple[float, float]]:
    """
    Compute vector Laplacian: ∇²F = ∇(∇·F) - ∇×(∇×F)

    This is the Helmholtz decomposition: decomposes into potential part (∇·F)
    and solenoidal part (∇×F).
    """
    # Compute divergence
    div_f = discrete_divergence(vector_field, sites, a)

    # Compute curl
    curl_f = discrete_curl_z(vector_field, sites, a)

    # Compute gradient of divergence
    grad_div = discrete_gradient(div_f, sites, a)

    # Convert curl_z to 2D "curl vector" (0, 0, curl_z) for Helmholtz
    # The solenoidal part from curl is: ∇×(curl_z k̂) = (∂curl_z/∂y, -∂curl_z/∂x)
    curl_2d = {site: (curl_f[site], 0.0) for site in sites}  # temp holder

    # Actually, for 2D: ∇×(F_z k̂) = (∂F_z/∂y, -∂F_z/∂x)
    # We need gradient of curl_z
    grad_curl = discrete_gradient(curl_f, sites, a)

    # Curl of 2D field: ∇×F = (∂F_y/∂x - ∂F_x/∂y) -> gives scalar
    # Curl of scalar: ∇×(φ k̂) in 2D is more subtle; we want ∇×∇×F
    # which is -(∇²F) for solenoidal F.

    # For Helmholtz: ∇²F = ∇(∇·F) - ∇×(∇×F)
    # The solenoidal part is: -∇×(curl_z k̂) = (-∂curl_z/∂y, ∂curl_z/∂x)

    laplacian = {}
    for site in sites:
        gd = grad_div.get(site, (0.0, 0.0))
        gc = grad_curl.get(site, (0.0, 0.0))

        # ∇×∇×F for 2D vector field:
        # The curl of (0, 0, curl_z) gives (-∂curl_z/∂y, ∂curl_z/∂x, 0)
        sol_part = (-gc[1], gc[0])  # Solenoidal part

        laplacian[site] = (gd[0] - sol_part[0], gd[1] - sol_part[1])

    return laplacian


# ============================================================================
# PART 6: Identity Verification: ∇·(∇×F) ≡ 0
# ============================================================================

def verify_no_monopole_property(
    vector_field: Dict[Site, Tuple[float, float]],
    sites: Sequence[Site],
    a: float = 1.0,
    tolerance: float = 1e-10
) -> bool:
    """
    Verify that ∇·(∇×F) = 0 exactly (within numerical tolerance).

    This tests that the discrete curl operator produces a solenoidal field.
    """
    # Compute curl
    curl_f = discrete_curl_z(vector_field, sites, a)

    # Convert curl_z to 2D "curl vector" for divergence computation
    # ∇×F_2d gives F_z, and ∇×(F_z k̂) gives (-∂F_z/∂y, ∂F_z/∂x)
    curl_field = {}
    grad_curl = discrete_gradient(curl_f, sites, a)
    for site in sites:
        gc = grad_curl.get(site, (0.0, 0.0))
        curl_field[site] = (-gc[1], gc[0])  # ∇×(curl_z k̂)

    # Compute divergence of curl
    div_curl = discrete_divergence(curl_field, sites, a)

    # Check all divergences are close to zero
    max_div = max(abs(d) for d in div_curl.values()) if div_curl else 0.0

    if max_div > tolerance:
        print(f"Warning: max(∇·(∇×F)) = {max_div:.2e} > {tolerance:.2e}")
        return False

    return True


# ============================================================================
# MAIN: Test the operators
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TRACK B: DISCRETE HEXAGONAL LATTICE OPERATORS")
    print("=" * 80)
    print()

    # Import from hex_lattice_graph
    from hex_lattice_graph import seven_cell, disk_sites

    # Test on seven-cell domain
    sites = seven_cell()
    print(f"Testing on {len(sites)}-site seven-cell domain")
    print()

    # Create a test vector field: simple tangential circulation
    # This should have zero divergence and non-zero curl
    test_field = {}
    for site in sites:
        x, y = site_xy(site)
        # Counterclockwise circulation: F = (-y, x)
        test_field[site] = (-y, x)

    print("Test 1: Circulation field F = (-y, x)")
    print("-" * 60)
    div_f = discrete_divergence(test_field, sites)
    curl_f = discrete_curl_z(test_field, sites)

    print("Divergence at each site:")
    for site in sorted(sites):
        print(f"  {site}: div = {div_f[site]:8.4f}")

    print()
    print("Curl (z-component) at each site:")
    for site in sorted(sites):
        print(f"  {site}: curl_z = {curl_f[site]:8.4f}")

    max_div = max(abs(d) for d in div_f.values())
    max_curl = max(abs(c) for c in curl_f.values())
    print()
    print(f"Max divergence: {max_div:.4e}")
    print(f"Max curl: {max_curl:.4f}")
    print()

    # Test no-monopole property
    print("Test 2: No-monopole property ∇·(∇×F) ≡ 0")
    print("-" * 60)
    is_solenoidal = verify_no_monopole_property(test_field, sites)
    print(f"No-monopole property verified: {is_solenoidal}")
    print()

    print("=" * 80)
    print("TRACK B: INITIALIZATION COMPLETE")
    print("=" * 80)
