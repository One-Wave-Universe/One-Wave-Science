# ONE-WAVE FRAMEWORK
## Book 2 — Small
## Chapter 2: Membranes, Gradients, and Transport

**Status:** GRAY reference / YELLOW One-Wave comparison  
**Dependencies:** A-103 Differential, A-104 Gradient, A-108 Local Stability  

---

## Gray

A living cell survives by maintaining differences between inside and outside. Those differences include ion concentration, pH, electrical potential, metabolites, and macromolecules. A membrane is therefore not just a wall; it is a controlled interface across which flux occurs.

For a species with concentration $c$, diffusion follows a concentration gradient. The simplest constitutive law is Fick's first law:

$$
\mathbf J=-D\nabla c.
$$

Conservation gives

$$
\frac{\partial c}{\partial t}=-\nabla\cdot\mathbf J+R(c,\ldots),
$$

so with constant $D$,

$$
\frac{\partial c}{\partial t}=D\nabla^2c+R.
$$

$R$ represents production or consumption by reactions. This is the control model. Any One-Wave cellular model has to reproduce these ordinary transport limits before claiming a deeper description.

## 2D

Represent the membrane as a closed curve dividing two state regions. Let $c_{in}$ and $c_{out}$ be concentrations sampled immediately on opposite sides. A simple permeability approximation is

$$
J_m=P_m(c_{out}-c_{in}).
$$

For a six-neighbor lattice, a discrete diffusion step can be written

$$
c_i^{n+1}=c_i^n+\lambda\sum_{j\in N(i)}(c_j^n-c_i^n)+\Delta t\,R_i^n.
$$

This is useful because it makes the bookkeeping visible: local state, neighbor differences, update, repeat. It is not uniquely One-Wave mathematics; it is a standard discrete approximation whose behavior can be checked.

## 3D

A real membrane is a surface. Flux through a closed boundary is summarized by

$$
\frac{d}{dt}\int_V c\,dV=-\oint_{\partial V}\mathbf J\cdot d\mathbf A+\int_VR\,dV.
$$

That equation is a clean bridge between local transport and whole-cell inventory. If Book 2 uses words such as compression, expression, intake, output, or balance, those words must ultimately map onto terms that can be measured in an equation like this.

## Mathematics — electrochemical gradients

For ions, concentration is not the whole story. Electrical potential also matters. The Nernst equilibrium potential for an ion of valence $z$ is

$$
E=\frac{RT}{zF}\ln\frac{[ion]_{out}}{[ion]_{in}}.
$$

A membrane current can be represented generically as

$$
I=g(V_m-E),
$$

where $g$ is conductance and $E$ is the relevant reversal potential. Multiple channel types give multiple currents. This is deliberately kept at control-model level; Book 2 should not replace electrophysiology vocabulary with One-Wave vocabulary unless a quantitative mapping adds predictive value.

## One-Wave comparison

A-104 Gradient is a natural language match for a spatial difference. That match is meaningful only at the level of **structure** until parameters are identified. A proposed mapping is:

- measured concentration or voltage difference → candidate differential state;
- spatial derivative → candidate gradient;
- membrane permeability/conductance → coupling strength;
- restoration toward a viable operating region → candidate local-stability response.

The mapping should be rejected if it merely renames $D$, $P_m$, or $g$ without reducing assumptions or predicting something new.

## Graph requirement

Every transport claim used downstream should be accompanied by at least one of these plots:

1. concentration vs distance at several times;
2. membrane flux vs concentration difference;
3. current vs membrane voltage;
4. residuals: standard control model vs proposed extension.

A graph without raw points or defined simulated parameters is illustration, not evidence.

## Predictions / tests

1. Run the discrete lattice model at decreasing $\Delta x$ and $\Delta t$ and verify convergence toward the diffusion equation.
2. Compare square, hexagonal, and irregular meshes under the same continuum diffusion coefficient. Geometry-specific claims require a difference that survives resolution changes.
3. Fit permeability data with the linear membrane law first. Only then test nonlinear alternatives.
4. Record conservation error. A transport simulation that creates or destroys inventory without an explicit source term fails before interpretation begins.

## Yellow Audit

- Gradient language is compatible with standard transport mathematics but not uniquely validated by it.
- A membrane is not evidence for a universal lattice boundary.
- No biological transport coefficient has yet been derived from One-Wave primitives.
- Geometry cannot be promoted from drawing to mechanism without controlled comparison.

## Future Work

Build one reproducible diffusion benchmark with CSV output and four plots: initial field, final field, conserved inventory, and residual against the analytic/control solution.

## Closing Thoughts

The membrane gives Book 2 a strong test case because the physics is measurable. Inside and outside differ; flux responds; the cell spends energy maintaining useful gradients. A proposed universal framework should make that accounting clearer, not blur it.
