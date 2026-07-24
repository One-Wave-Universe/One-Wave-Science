---
node_id: "A-111"
canonical_name: "Recursion"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Foundation Primitive / Extension"
claim_gate_detail: "YELLOW"
metadata_standard: "I-06"
---

# Node A-111: Recursion

**Dependencies:**  
Upstream: A-109, A-110  
Downstream: A-112, E-520 Recursive Self-Modeling Levels (hexagonal application), E-523 Circle Pit Vortex Transition (real published-physics structural parallel), G-719 Neural System Functional Analogy Map (Five Mind grounding, neighbor-average term)

### Definition

Recursion is a closed update cycle where the output of one step becomes the input of the next. Memory alone is not recursion. Recursion requires both memory and a feedback rule [1].

$$
\psi_{n+1} = f(\psi_n, \psi_{n-1})
$$

$$
\text{Memory} + \text{Feedback Rule} \Rightarrow \text{Recursion}
$$

### Mathematics

Full One-Wave update rule:

$$
\psi_i^{n+1} = \psi_i^n + (1-\gamma)(\psi_i^n - \psi_i^{n-1}) + \beta_i(\langle \psi_j^n \rangle - \psi_i^n)
$$

Closed update cycle:

$$
f^k(\psi) = \psi \quad \text{for integer } k
$$

### Locality Rule

Nearest-neighbor coupling is confirmed through $$\beta_i(\langle \psi_j^n \rangle - \psi_i^n)$$. Whether additional nonlocal effects beyond nearest-neighbor exist remains open [1].

Oscillation is not required for recursion [1].

### Operational Chain

$$
\text{Oscillation} + \text{Memory} + \text{Feedback Rule} \Rightarrow \text{Recursion} \Rightarrow \text{Persistent Mode}
$$

### Metadata and Wave Layer

Metadata is the compressed description of a wave configuration. Wave data is metadata that has entered an active update cycle.

A wave state is represented as:

$$
\Psi = (A, f, \phi, x, t, m)
$$

where:

- $$A$$ = amplitude.
- $$f$$ = frequency.
- $$\phi$$ = phase.
- $$x$$ = position.
- $$t$$ = time.
- $$m$$ = metadata state.

Recursive wave update:

$$
\Psi_{n+1} = F(\Psi_n, \Psi_{n-1}, M)
$$

where:

- $$\Psi_n$$ = current wave state.
- $$\Psi_{n-1}$$ = memory state.
- $$M$$ = metadata constraints.

Metadata describes the state. Wave data is metadata expressed as an active update process. Conversion requires state identity, coupling rule, timing relationship, and propagation behavior.

### Interference Layer

For oscillating systems:

$$
\psi(t) = A\sin(2\pi f t + \phi)
$$

Multiple waves combine as:

$$
\Psi(t) = \sum_{k=1}^{N} A_k\sin(2\pi f_k t + \phi_k)
$$

Measure reinforcement, cancellation, harmonic overlap, and phase alignment.

Beat frequency:

$$
f_b = |f_1 - f_2|
$$

### Harmonic Mapping

For guitar/frequency systems:

$$
f_n = f_0(2^{n/12})
$$

Track root distance, octave position, interval ratio, and oscillation width.

Relative frequency:

$$
R = \frac{f_2}{f_1}
$$

A chord is not the final model. It is a label for wave relationships.

### Four Harmonic Behavior Axes

Primary character:

Major $$\leftrightarrow$$ Minor

Movement:

Forward $$\leftrightarrow$$ Backward

Result:

1. Major / Forward.
2. Major / Backward.
3. Minor / Forward.
4. Minor / Backward.

### Stability Measurement Layer

Persistence is not defined as lack of movement. A persistent pattern may oscillate while preserving its structure.

#### State Difference

$$
D_n = \|\Psi_n - \Psi_{n-1}\|
$$

Used to measure local change.

#### Structural Stability

$$
S_R = 1 - \frac{|R_n - R_{n-1}|}{R_{max}}
$$

where:

- $$R_n$$ = relationship state at time $$n$$.
- $$R_{max}$$ = maximum allowed relational change.

A wave remains stable when its internal relationships remain consistent.

#### Combined Stability Score

$$
S_{total}
=
w_R S_R
+
w_f S_f
+
w_\phi S_\phi
+
w_A S_A
$$

where:

- $$S_R$$ = relational stability.
- $$S_f$$ = frequency stability.
- $$S_\phi$$ = phase stability.
- $$S_A$$ = amplitude stability.
- $$w$$ = weighting factors.

### Phase Lock Criterion

A recursive wave enters a locked state when:

$$
|\Delta \phi| < \theta
$$

and:

$$
|\Delta f| < \delta
$$

over an observation window.

### Harmonic Selection Rule

A pattern is selected when:

$$
D_n < \epsilon
$$

or when:

$$
S_{total} > S_{threshold}
$$

with bounded energy:

$$
E_{total} < E_{limit}
$$

Selection requires:

- Coherent relationship.
- Stable recurrence.
- Bounded interference.
- Repeatable structure.

### Persistence Test

A recursive wave enters persistent mode when:

$$
\|\Psi_{n+k} - \Psi_n\| < \epsilon
$$

for a defined tolerance.

Possible outcomes:

- Fixed recursion.
- Periodic recursion.
- Chaotic recursion.

A recursive system is stable when the wave state remains measurable, bounded, and repeatable under its own update rule.

### Yellow Audit
