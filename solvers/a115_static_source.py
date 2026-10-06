"""A-115 static spherical source diagnostic, V_b=0; dimensionless, not a fit."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.linalg import solve_banded

def solve(cells=256, outer_radius=4., stiffness=2., alpha=1.):
    if (not isinstance(cells, int) or cells < 8 or
        not np.isfinite([outer_radius, stiffness, alpha]).all() or
        outer_radius <= 1 or stiffness <= 0):
        raise ValueError("Require integer cells >=8, outer radius >1 and positive K_chi+S_u")
    edges = np.linspace(0., outer_radius, cells+1)
    dr = outer_radius/cells
    radius = (edges[:-1]+edges[1:])/2
    # Compact smooth radial vector source J_r = r(1-r^2)^2, r<1.
    source = np.where(edges < 1., edges*(1.-edges**2)**2, 0.)
    flux = edges**2*source/stiffness
    weights = edges**2/dr
    weights[-1] *= 2 # Dirichlet chi(R)=0, center-to-boundary half cell.
    band = np.zeros((3, cells))
    band[1] = -(weights[:-1]+weights[1:])
    band[0, 1:] = weights[1:-1]
    band[2, :-1] = weights[1:-1]
    compression = solve_banded((1,1), band, np.diff(flux))
    gradient = np.zeros(cells+1)
    gradient[1:-1] = np.diff(compression)/dr
    gradient[-1] = -compression[-1]/(dr/2)
    acceleration = -alpha*gradient
    exact_chi = np.where(radius < 1., -(1.-radius**2)**3/(6*stiffness), 0.)
    # Reconstruct regular displacement: r^2 u_r = -integral_0^r chi(s)s^2 ds.
    volumes = np.diff(edges**3)/3
    displacement = np.zeros(cells+1)
    displacement[1:] = -np.cumsum(compression*volumes)/edges[1:]**2
    reconstructed_chi = -np.diff(edges**2*displacement)/volumes
    residual = np.diff(edges**2*gradient-flux)
    return dict(cells=cells, outer_radius=outer_radius, stiffness=stiffness, alpha=alpha,
                max_compression_error=float(np.max(np.abs(compression-exact_chi))),
                max_flux_balance_residual=float(np.max(np.abs(residual))),
                max_displacement_identity_error=float(np.max(np.abs(reconstructed_chi-compression))),
                max_exterior_acceleration=float(np.max(np.abs(acceleration[edges>1.]))),
                max_acceleration_gradient_error=float(np.max(np.abs(acceleration+alpha*source/stiffness))),
                center_compression=float(compression[0]),
                radial_source_flux_at_outer_boundary=float(flux[-1]))

def report():
    root = Path(__file__).resolve().parents[1]
    sources = ["Nodes/A-115_Unified_Compression_Field.md",
               "Nodes/C-320_Magnetic_Compression_Path_Coupling.md"]
    return dict(schema_version=1,
        scope="Static spherical A-115; V_b=0; constant K_chi+S_u; K_L=I; regular origin; chi(4)=0",
        units="dimensionless; no physical calibration or galaxy fitting",
        equation="(K_chi+S_u) laplacian(chi)=div(J); chi'=J_r/(K_chi+S_u)",
        source="J_r=r(1-r^2)^2 for r<1, otherwise zero",
        reference_commit="87ad3af06c86498bd6d4f868b73540346e1934d2",
        authority_sha256={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in sources},
        solver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        runs=[solve(n) for n in (64,128,256,512)],
        conclusion="This restricted compact vector-source branch has zero exterior acceleration; it does not recover inverse-square gravity.",
        limits=["Nonzero V_b, dynamics, nonlocal sources and nonregular boundaries are not tested",
                "No general no-go theorem for all One-Wave source laws",
                "Tensor path weighting cannot create acceleration where grad(chi)=0"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = report()
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    for run in result["runs"]:
        print(run)
