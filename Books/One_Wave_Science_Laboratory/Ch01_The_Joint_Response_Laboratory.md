# Chapter 1 — The Joint Response Laboratory

**Status:** explanatory chapter; numerical candidate scope is tested, physical identification remains open.  
Canonical owners: C-318, C-322, A-115, C-317 and D-409.  
[Contents](README.md) · [Next chapter](Ch02_Localized_Excitations_and_Measurements.md)

## The question behind the calculation

If a recurrence is held together by knot structure, electrical-shell response, the Mirror relation and the weave, moving or exciting one part changes the others. Four independent formulas cannot account for that shared response. The useful calculation must start from a joint state and preserve its couplings through the energy and response measurements.

The implemented fixture asks a bounded numerical question: can one declared four-coordinate operator produce an energy-conserving update, passive boundary coupling and calculable carried-profile curvature? It does. That is the working foundation to extend. It does not establish that the four numerical coordinates are already the derived microscopic physical fields.

## Native geometry and the operator

Each site carries q=(K,E,M,T). Sites use D-409's native three-dimensional FCC twelve-neighbor shell, not two pasted sixfold planes. The finite graph removes exterior bonds and therefore imposes a reflecting cavity. That boundary is appropriate for an accounting control; it cannot establish self-confinement.

Let L be the graph Laplacian and R the four-coordinate cycle Laplacian. The declared joint stiffness H combines spatial coupling and relative-phase response. The positive work metric W converts state velocity into the fixture's energy. Their exact construction and input coefficients are in [the canonical derivation](../../solvers/JOINT_RESPONSE_DERIVATION.md).

The undamped update is

\[
W\frac{q_{n+1}-2q_n+q_{n-1}}{\Delta t^2}+Hq_n=0.
\]

This is a coupled second-order recurrence. At each step, H acts on the whole state. Its cross terms are retained during evolution, rather than added to a result after separate calculations.

## Why the energy ledger matters

A simulation can appear stable because numerical errors inject energy at the same rate another part loses it. An exact ledger prevents that compensation from being mistaken for a physical recurrence.

For midpoint m=(q_n+q_{n-1})/2 and velocity v=(q_n-q_{n-1})/Δt, the fixture conserves

\[
E_{n-1/2}=\frac12v^T\left(W-\frac{\Delta t^2}{4}H\right)v+\frac12m^THm.
\]

The timestep must make the velocity metric positive. A timestep outside the declared stability interval is rejected, not repaired by hidden damping. The published 500-step control has relative drift below 9.38×10⁻¹⁴. This verifies the chosen discrete equation and ledger; it does not calibrate their energy in joules.

## The Mirror relation: coupling and phase

The boundary rule is reflection, deflection, tangential roll-off or scattering. The Mirror relation permits coupling and phase shift. A path forced geometrically through the boundary is not this model.

The fixture represents four interaction-coordinate ports at one boundary site. If B selects those channels and Γ is nonnegative internal damping, its frequency-domain operator is

\[
D(\omega)=H-\omega^2W-i\omega(BB^T+\Gamma),\qquad
S(\omega)=I+2i\omega B^TD(\omega)^{-1}B.
\]

For incoming amplitude a and internal response q=D⁻¹Ba,

\[
\|a\|^2-\|Sa\|^2=4\omega^2q^\dagger\Gamma q.
\]

With no loss, outgoing power equals incoming power. With passive loss, the missing power is accounted for in Γ. The response includes phase and redistribution across coordinates; gain cannot be explained away as reinjection.

These abstract ports are not yet an angular radiation model. The fixture has not simulated a wave packet bouncing off a geometric shell or rolling along its surface. Those measurements require spatial incoming and outgoing channels and the actual shell state. The present calculation verifies the algebra those channels must respect.

## Two different inertia questions

Boundary-coordinate inertia asks how the rest of the state follows a selected boundary displacement. Eliminating internal coordinates produces an effective stiffness and work metric. Differentiating the mechanical Schur complement of H−zW with respect to z=ω² gives the effective boundary inertia. The published finite difference agrees with the independent work-metric construction.

Carried-profile resistance asks how much energy changes when a specified spatial pattern is carried at a small velocity. Its energy Hessian is

\[
\mathcal M_{jk}=\left.\frac{\partial^2\overline E}{\partial v_j\partial v_k}\right|_{v=0}.
\]

The fixture evaluates this for cavity eigenprofiles and checks it against an independent velocity sweep of the actual discrete ledger. This demonstrates how to measure a curvature, not how to assign a measured particle mass to that profile. A cavity eigenmode is not automatically a self-held material excitation.

The distinction is experimentally useful. An internal uniform phase mode can oscillate at nonzero frequency while its spatial gradient, and therefore the fixture's carried-profile tensor, vanishes. Frequency alone does not establish translational inertia.

## What the controls teach

The [full result packet](../../solvers/joint_response_results.json) owns the eigenfrequency groups, matrices and complete fixed-window response samples. Grouping degenerate modes prevents an arbitrary eigenvector basis from being mistaken for physical anisotropy.

Removing cross and phase couplings eliminates off-diagonal port transfer in this fixture. Scaling the common work unit scales fixed-coordinate boundary inertia while preserving the dimensionless spectrum. Absolute units therefore require independent calibration. Selecting a frequency because it resembles a desired mass would bypass that requirement.

Spatial refinement changes the first spatial frequency substantially. More sites improve the question but do not make a precise physical prediction by themselves. The next chapter addresses a different missing condition: can the field support a localized excitation without the reflecting cavity holding it in place?

## Run and judge

```sh
python solvers/test_joint_boundary_response.py
python solvers/run_joint_response.py > solvers/joint_response_results.json
```

Reject an unbalanced ledger, a gain-producing passive response, a singular solve silently regularized with damping, or a mass claim obtained by relabeling a cavity frequency. Keep valid numerical response evidence and physical identification separate. That separation makes the next calculation possible without discarding what already works.
