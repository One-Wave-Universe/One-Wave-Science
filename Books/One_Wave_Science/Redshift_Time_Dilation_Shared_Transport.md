# Chapter Work — Redshift and Time Dilation as One Transport Problem

The cosmology program has a sharper target now. Redshift and time dilation should not be treated as two phenomena that receive two independent fitted equations. If One-Wave attributes both to propagation through a physical medium, the medium must do both jobs through the same local dynamics.

The starting point is the exact A-114 recurrence. Its characteristic roots separate naturally into a magnitude and a phase. The magnitude is controlled by the damping structure, while the phase gives the dispersion relation. That is useful, but it also exposes a limitation: a static linear homogeneous recurrence does not automatically turn a monochromatic carrier into a progressively lower temporal frequency merely because the carrier has propagated farther. It can attenuate it, delay it, and disperse a packet. Those are not the same operation as cumulative carrier-frequency translation.

That makes E-528's law,

```
d nu / d ell = -kappa_gamma nu,
```

a derivation target rather than a consequence already supplied by the lattice equation. The distinction matters. If the redshift law is inserted independently, the framework can imitate a desired redshift-distance curve without explaining why the lattice produces it.

The productive route is therefore to search for the smallest physical extension that actually permits frequency exchange: state-dependent transport, nonlinear coupling, or a locally evolving reference/update state. Whichever mechanism survives must identify what changes in the medium, where the exchanged energy goes, and why the effect remains coherent enough to preserve the observed signal structure.

Time dilation then becomes a second output of the same calculation. Let the derived interaction accumulate as

```
K = integral kappa_gamma d ell.
```

If the spectral channel yields

```
1 + z = exp(K),
```

the strongest version of the theory asks whether the same operator predicts

```
Delta t_obs / Delta t_emit = exp(K).
```

That equality is not assumed true. It is deliberately made difficult to escape. If separate free functions are needed for frequency and duration, the proposed shared-medium explanation has lost much of its explanatory power.

This produces a clean scientific workflow. Derive the local operator first. Derive its frequency and envelope transformations second. Freeze its parameters. Only then compare against supernova observations and distance/covariance data. Finally carry the frozen model into an independent geometric test such as BAO/AP. A failure there is information, not something to tune away.

The immediate proof problem is consequently smaller than "prove cosmology." It is: **can the One-Wave update mechanics generate genuine frequency conversion while simultaneously fixing the envelope-time transformation?** If not, the current redshift/time-dilation implementation must change. If so, the resulting shared law becomes a concrete, falsifiable cosmological model.

See `Nodes/E-534_Redshift_Time_Dilation_Shared_Transport_No_Go.md` for the formal derivation target and failure gates.
