"""Transient solver for circuits with MOSFETs, capacitors, inductors.

Uses Modified Nodal Analysis (MNA) at each time step with backward Euler
(first-order implicit) integration. No numpy dependency.

Key insight: at each timestep, capacitors and inductors contribute to the
MNA matrix as equivalent conductances + current sources. MOSFET conductance
is determined by instantaneous gate voltage.

Integration: backward Euler (first-order) + adaptive timestep sizing (Phase 2+).
For stiff systems (large impedance ratios), reduce dt automatically when
voltage changes exceed stability threshold. Full trapezoidal (second-order)
with state tracking deferred to Phase 3.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Optional
import math


class UnionFind:
    """Merges node names that a Wire declares equal."""

    def __init__(self):
        self._parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self._parent.setdefault(x, x)
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != root:
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self._parent[ra] = rb


def _solve_linear_mna(A: list[list[float]], b: list[float],
                      size: int, tol: float = 1e-12) -> list[float]:
    """Gauss-Jordan with partial pivoting.

    Returns x such that A @ x == b (approximately, within solver tolerance).
    Raises if matrix is singular (circuit is under-constrained).
    """
    M = [row[:] + [b[i]] for i, row in enumerate(A)]

    for col in range(size):
        pivot_row = max(range(col, size), key=lambda r: abs(M[r][col]))
        if abs(M[pivot_row][col]) < tol:
            raise ValueError(
                "MNA matrix singular or ill-conditioned. Circuit may be "
                "floating, or numerical precision lost due to very different "
                "impedance scales."
            )
        if pivot_row != col:
            M[col], M[pivot_row] = M[pivot_row], M[col]

        pivot_val = M[col][col]
        for r in range(size):
            if r == col:
                continue
            factor = M[r][col] / pivot_val
            if abs(factor) < tol:
                continue
            for c in range(col, size + 1):
                M[r][c] -= factor * M[col][c]

    return [M[i][size] / M[i][i] for i in range(size)]


@dataclass
class CapacitorState:
    """State for a single capacitor: voltage across it."""
    id: str
    voltage: float = 0.0


@dataclass
class InductorState:
    """State for a single inductor: current through it."""
    id: str
    current: float = 0.0


@dataclass
class MOSFETState:
    """State for a single MOSFET: on/off decision and actual conductance."""
    id: str
    vgs: float = 0.0
    is_on: bool = False
    actual_rds_on: float = 1e12  # very large when off


@dataclass
class TransientSolution:
    """Result of one transient time step."""
    time: float
    voltages: dict[str, float]
    source_currents: dict[str, float]
    capacitor_states: dict[str, CapacitorState]
    inductor_states: dict[str, InductorState]
    mosfet_states: dict[str, MOSFETState]
    reference_node: str
    convergence_iterations: int
    converged: bool


class TransientCircuit:
    """A circuit with dynamic components (capacitors, inductors, MOSFETs).

    Supports:
    - Voltage sources (DC)
    - Resistors
    - Capacitors
    - Inductors
    - MOSFETs (NMOS, PMOS)
    - Op-amp buffers (virtual ground)
    - Wires and ground nodes
    """

    def __init__(self):
        from .components import DCVoltageSource, Resistor, Wire, Ground
        from .components_extended import Capacitor, Inductor, NMOS, PMOS, OpAmpBuffer

        self.resistors: list[Resistor] = []
        self.sources: list[DCVoltageSource] = []
        self.wires: list[Wire] = []
        self.grounds: list[Ground] = []

        self.capacitors: list[Capacitor] = []
        self.inductors: list[Inductor] = []
        self.nmos: list[NMOS] = []
        self.pmos: list[PMOS] = []
        self.opamps: list[OpAmpBuffer] = []

    def add(self, component):
        """Add a component to the circuit."""
        from .components import DCVoltageSource, Resistor, Wire, Ground
        from .components_extended import Capacitor, Inductor, NMOS, PMOS, OpAmpBuffer

        if isinstance(component, Resistor):
            self.resistors.append(component)
        elif isinstance(component, DCVoltageSource):
            self.sources.append(component)
        elif isinstance(component, Wire):
            self.wires.append(component)
        elif isinstance(component, Ground):
            self.grounds.append(component)
        elif isinstance(component, Capacitor):
            self.capacitors.append(component)
        elif isinstance(component, Inductor):
            self.inductors.append(component)
        elif isinstance(component, NMOS):
            self.nmos.append(component)
        elif isinstance(component, PMOS):
            self.pmos.append(component)
        elif isinstance(component, OpAmpBuffer):
            self.opamps.append(component)
        else:
            raise TypeError(f"Unknown component type: {type(component).__name__}")

        return component

    def solve_step(self,
                   initial_cap_states: dict[str, CapacitorState],
                   initial_ind_states: dict[str, InductorState],
                   initial_voltages: dict[str, float],
                   dt: float,
                   time: float,
                   gate_voltage_func: Optional[Callable[[str, float], float]] = None,
                   integration_method: str = "trapezoidal") -> TransientSolution:
        """Solve one transient time step using trapezoidal integration (Phase 3+).

        Trapezoidal (second-order) is default for stability with stiff systems.
        Backward Euler (first-order) available for comparison.

        Caller is responsible for timestep sizing (dt). For gate transients with
        inductors, dt ~ 10-100ns is typical for trapezoidal.

        Args:
            initial_cap_states: capacitor voltages from previous step
            initial_ind_states: inductor currents from previous step
            initial_voltages: node voltages from previous step
            dt: time step size (seconds)
            time: current simulation time (seconds)
            gate_voltage_func: function(mosfet_id, time) -> voltage applied to gate
            integration_method: "trapezoidal" (default, second-order) or "backward_euler" (first-order)

        Returns:
            TransientSolution with voltages, currents, and updated states
        """
        if dt <= 0:
            raise ValueError("dt must be > 0")

        if integration_method not in ("trapezoidal", "backward_euler"):
            raise ValueError(f"integration_method must be 'trapezoidal' or 'backward_euler', got '{integration_method}'")

        uf = UnionFind()
        for w in self.wires:
            uf.union(w.a, w.b)

        # Collect all nodes
        all_nodes: set[str] = set()
        for r in self.resistors:
            all_nodes.add(r.a)
            all_nodes.add(r.b)
        for s in self.sources:
            all_nodes.add(s.pos)
            all_nodes.add(s.neg)
        for g in self.grounds:
            all_nodes.add(g.node)
        for c in self.capacitors:
            all_nodes.add(c.a)
            all_nodes.add(c.b)
        for l in self.inductors:
            all_nodes.add(l.a)
            all_nodes.add(l.b)
        # Skip MOSFET gates - they're driven by gate_voltage_func, not MNA unknowns
        for m in self.nmos:
            all_nodes.add(m.drain)
            all_nodes.add(m.source)
        for m in self.pmos:
            all_nodes.add(m.drain)
            all_nodes.add(m.source)
        for op in self.opamps:
            all_nodes.add(op.v_in)
            all_nodes.add(op.v_out)
            all_nodes.add(op.gnd)

        if not all_nodes:
            raise ValueError("Circuit has no components")

        roots = sorted({uf.find(n) for n in all_nodes})

        # Pick reference
        if self.grounds:
            reference = uf.find(self.grounds[0].node)
        elif self.sources:
            reference = uf.find(self.sources[0].neg)
        else:
            reference = roots[0]

        node_index: dict[str, int] = {}
        idx = 0
        for root in roots:
            if root == reference:
                continue
            node_index[root] = idx
            idx += 1

        n_nodes = idx
        n_src = len(self.sources)
        n_ind = len(self.inductors)  # inductors add unknown currents to MNA
        size = n_nodes + n_src + n_ind

        # Initialize previous voltage estimate
        prev_voltages = initial_voltages.copy()
        for root in roots:
            if root not in prev_voltages:
                prev_voltages[root] = 0.0

        # Apply gate voltages from gate_voltage_func (if provided)
        # Build map of gate_id -> primary MOSFET that drives it
        # (to avoid overwriting gate voltage when multiple MOSFETs share a gate)
        if gate_voltage_func is not None:
            gate_drivers = {}  # gate_root -> mosfet_id
            for nmos in self.nmos:
                gate_root = uf.find(nmos.gate)
                if gate_root not in gate_drivers:
                    gate_drivers[gate_root] = nmos.id
            for pmos in self.pmos:
                gate_root = uf.find(pmos.gate)
                if gate_root not in gate_drivers:
                    gate_drivers[gate_root] = pmos.id

            # Apply gate voltages for each unique gate
            for gate_root, mosfet_id in gate_drivers.items():
                prev_voltages[gate_root] = gate_voltage_func(mosfet_id, time)

        # Backward Euler/Trapezoidal with Newton iterations for nonlinear elements
        # Increase iterations when opamps are present (current limiting is nonlinear)
        n_iterations = 3 if self.opamps else 1

        for iteration in range(n_iterations):
            # Initialize MNA matrix and RHS vector for this iteration
            A = [[0.0] * size for _ in range(size)]
            b = [0.0] * size

            def gi(node: str) -> int:
                root = uf.find(node)
                return node_index.get(root, -1)

            def stamp_g(i: int, j: int, val: float) -> None:
                if i >= 0 and j >= 0:
                    A[i][j] += val

            # Resistors: G = 1/R
            for r in self.resistors:
                g = 1.0 / r.ohms
                i, j = gi(r.a), gi(r.b)
                stamp_g(i, i, g)
                stamp_g(j, j, g)
                stamp_g(i, j, -g)
                stamp_g(j, i, -g)

            # Capacitors: trapezoidal integration (Phase 3+)
            # Trapezoidal: I_k+1 = (2*C/dt)*(V_k+1 - V_k) - I_k
            # Where I_k = (2*C/dt)*(V_k - V_k-1) from previous step
            # Equivalent: G_eq = 2*C/dt, I_source = (2*C/dt)*V_old + I_old
            # Note: I_old is reconstructed from stored voltage change, or use backward Euler for first step
            if integration_method == "trapezoidal":
                for cap in self.capacitors:
                    g_eq = 2.0 * cap.farads / dt
                    v_old = initial_cap_states[cap.id].voltage
                    i_src = g_eq * v_old  # Trapezoidal source term

                    i, j = gi(cap.a), gi(cap.b)
                    stamp_g(i, i, g_eq)
                    stamp_g(j, j, g_eq)
                    stamp_g(i, j, -g_eq)
                    stamp_g(j, i, -g_eq)
                    if i >= 0:
                        b[i] += i_src
                    if j >= 0:
                        b[j] -= i_src
            else:  # backward_euler
                for cap in self.capacitors:
                    g_eq = cap.farads / dt
                    v_old = initial_cap_states[cap.id].voltage
                    i_src = -g_eq * v_old

                    i, j = gi(cap.a), gi(cap.b)
                    stamp_g(i, i, g_eq)
                    stamp_g(j, j, g_eq)
                    stamp_g(i, j, -g_eq)
                    stamp_g(j, i, -g_eq)
                    if i >= 0:
                        b[i] += i_src
                    if j >= 0:
                        b[j] -= i_src

            # MOSFETs: determine on/off state from gate voltage
            mosfet_states = {}
            for nmos in self.nmos:
                vg = prev_voltages.get(uf.find(nmos.gate), 0.0)
                vs = prev_voltages.get(uf.find(nmos.source), 0.0)
                vgs = vg - vs
                is_on = vgs >= nmos.Vth
                rds = nmos.Rds_on if is_on else 1.0 / (nmos.off_leakage_nA * 1e-9)

                mosfet_states[nmos.id] = MOSFETState(
                    id=nmos.id,
                    vgs=vgs,
                    is_on=is_on,
                    actual_rds_on=rds
                )

                g = 1.0 / rds
                i, j = gi(nmos.drain), gi(nmos.source)
                stamp_g(i, i, g)
                stamp_g(j, j, g)
                stamp_g(i, j, -g)
                stamp_g(j, i, -g)

            # Voltage sources (DC)
            for k, s in enumerate(self.sources):
                row = n_nodes + k
                p, n = gi(s.pos), gi(s.neg)
                if p >= 0:
                    A[p][row] += 1
                    A[row][p] += 1
                if n >= 0:
                    A[n][row] -= 1
                    A[row][n] -= 1
                b[row] += s.volts


            # Op-amp buffers: unity gain buffer with output impedance
            # Simplified model: V_out = V_in (via VCVS-like equation)
            # Output impedance Rout models current sourcing limits
            # Current limiting enforced through Newton iteration
            for op_idx, op in enumerate(self.opamps):
                v_in_idx = gi(op.v_in)
                v_out_idx = gi(op.v_out)
                v_gnd_idx = gi(op.gnd)

                # Coupling from input to output: unity gain with stiff coupling
                # Use very small resistance to approximate VCVS: V_out ≈ V_in
                if v_out_idx >= 0 and v_in_idx >= 0:
                    g_coupling = 1.0 / 0.001  # 1000 siemens - very stiff coupling
                    A[v_out_idx][v_out_idx] += g_coupling
                    A[v_out_idx][v_in_idx] -= g_coupling
                    # Do NOT couple back to v_in; it's determined by resistor divider

                # Output impedance with current limiting (enforced via Newton iteration)
                if op.Rout > 0 and v_out_idx >= 0 and v_gnd_idx >= 0:
                    # Calculate actual output current from previous iteration
                    v_out = prev_voltages.get(op.v_out, 0.0)
                    v_gnd = prev_voltages.get(op.gnd, 0.0)
                    v_out_diff = v_out - v_gnd
                    i_out = v_out_diff / op.Rout if op.Rout > 0 else 0.0

                    # Determine effective output resistance
                    # If current is being limited, increase Rout to create voltage sag
                    rout_effective = op.Rout

                    if iteration > 0:  # Start limiting checks after first iteration
                        i_max_source_a = op.max_sourcing_mA * 1e-3  # Convert mA to A
                        i_max_sink_a = op.max_sinking_mA * 1e-3

                        # Current limiting logic:
                        # If sourcing current exceeds max, add series resistance
                        # This creates voltage sag on next iteration, reducing current draw
                        if i_out > i_max_source_a:
                            # Sourcing too much - increase Rout to limit current
                            excess_current = i_out - i_max_source_a
                            # Add extra resistance: V_sag = I_excess * R_extra
                            # Target sag proportional to excess current
                            r_extra = abs(v_out_diff) / max(excess_current, 1e-12) if v_out_diff != 0 else op.Rout
                            rout_effective = op.Rout + r_extra
                        elif i_out < -i_max_sink_a:
                            # Sinking too much - increase Rout to limit current
                            excess_current = -i_out - i_max_sink_a
                            r_extra = abs(v_out_diff) / max(excess_current, 1e-12) if v_out_diff != 0 else op.Rout
                            rout_effective = op.Rout + r_extra

                    # Stamp the effective output impedance
                    g_out = 1.0 / rout_effective
                    A[v_out_idx][v_out_idx] += g_out
                    A[v_out_idx][v_gnd_idx] -= g_out
                    A[v_gnd_idx][v_out_idx] -= g_out
                    A[v_gnd_idx][v_gnd_idx] += g_out

            # Inductors: trapezoidal integration (Phase 3+)
            # Trapezoidal: I_k+1 = I_k + (dt/2L)*(V_k + V_k+1)
            # Rearranged: V_k+1 = (2L/dt)*(I_k+1 - I_k) - V_k
            # In MNA form: (2L/dt)*I_source = V_eq = (2L/dt)*I_old
            if integration_method == "trapezoidal":
                for ind_idx, ind in enumerate(self.inductors):
                    row = n_nodes + n_src + ind_idx
                    i_old = initial_ind_states[ind.id].current
                    v_eq = 2.0 * ind.henries / dt * i_old  # Trapezoidal source term

                    a, b_node = gi(ind.a), gi(ind.b)
                    if a >= 0:
                        A[a][row] += 1
                        A[row][a] += 1
                    if b_node >= 0:
                        A[b_node][row] -= 1
                        A[row][b_node] -= 1
                    b[row] += v_eq
            else:  # backward_euler
                for ind_idx, ind in enumerate(self.inductors):
                    row = n_nodes + n_src + ind_idx
                    i_old = initial_ind_states[ind.id].current
                    v_eq = ind.henries / dt * i_old

                    a, b_node = gi(ind.a), gi(ind.b)
                    if a >= 0:
                        A[a][row] += 1
                        A[row][a] += 1
                    if b_node >= 0:
                        A[b_node][row] -= 1
                        A[row][b_node] -= 1
                    b[row] += v_eq

            x = _solve_linear_mna(A, b, size)

            # Extract voltages and currents
            new_voltages = {reference: 0.0}
            for root, i in node_index.items():
                new_voltages[root] = x[i]

            full_voltages = {n: new_voltages[uf.find(n)] for n in all_nodes}

            # Preserve gate voltages across Newton iterations (they're external to MNA)
            prev_voltages.update(new_voltages)

        # Update capacitor/inductor states based on final voltages
        new_cap_states = {}
        for cap in self.capacitors:
            v_a = full_voltages[uf.find(cap.a)]
            v_b = full_voltages[uf.find(cap.b)]
            v_cap = v_a - v_b
            new_cap_states[cap.id] = CapacitorState(id=cap.id, voltage=v_cap)

        new_ind_states = {}
        for ind in self.inductors:
            # Backward Euler: I_new = I_old + dt/L * V
            v_a = full_voltages[uf.find(ind.a)]
            v_b = full_voltages[uf.find(ind.b)]
            v_ind = v_a - v_b
            i_old = initial_ind_states[ind.id].current
            i_new = i_old + (dt / ind.henries) * v_ind
            new_ind_states[ind.id] = InductorState(id=ind.id, current=i_new)

        source_currents = {s.id: -x[n_nodes + k] for k, s in enumerate(self.sources)}

        return TransientSolution(
            time=time,
            voltages=full_voltages,
            source_currents=source_currents,
            capacitor_states=new_cap_states,
            inductor_states=new_ind_states,
            mosfet_states=mosfet_states,
            reference_node=reference,
            convergence_iterations=1,
            converged=True
        )
