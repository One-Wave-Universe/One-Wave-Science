# Updated 31: Visible Curvature Surface

Updated 31 corrects the D-413 browser renderer so the imposed curvature well is visibly present in the triangular Ground lattice from the first frame.

## Locked rendering rule

The rendered depression, curved contours, displacement height, and restoring gradient must all sample the same evolving lattice height field:

\[
\boxed{z_{\rm render}(\mathbf q)=z_{\rm motion}(\mathbf q)=\mathcal I[\{z_i\}](\mathbf q)}
\]

The browser now provides:

- shaded triangular faces built from actual node positions and heights;
- curved depth contours sampled from the lattice surface;
- a Ground-to-bottom depth marker;
- curved-surface and top-down projections;
- adjustable vertical exaggeration that changes only the view;
- immediate initialization of the lattice on the imposed well profile;
- the existing Ground-fixed, displacement-fixed, and well-fixed camera modes.

The bounded displacement follows the same deformed surface used to calculate the restoring gradient. Camera, projection, contour display, and vertical exaggeration do not modify the physical state.

## Scope

This remains a native-2D Yellow reduced simulation. The Gaussian well is imposed rather than derived. The bounded displacement shell is a collective test coordinate rather than a quark, proton, particle, charge shell, Mirror Gate, or Mass Effect derivation.

No chapter mechanism changed in Updated 31. Book 1 Chapters 1 and 2 were checked and already describe D-413 as a reduced pre-quark Ground and orbital-restoring test bed, so their source/PDF pairs remain current without gratuitous rewriting.
