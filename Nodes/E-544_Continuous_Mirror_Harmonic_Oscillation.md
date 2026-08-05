# E-544 — Continuous Mirror Harmonic Oscillation

## Primitive

```text
E(n)  = 2(n + 1)
H-(n) = E(n) - 1
H+(n) = E(n) + 1
```

`E(n)` is the moving even/up carrier. `H-` and `H+` are the two odd/down mirror resolutions. They are two surfaces of one oscillator, not independent nodes.

## Shared boundary

```text
H+(n) = H-(n + 1)
```

This overlap joins adjacent harmonic identities into one continuous route.

## Driven form

```text
Sigma(n+1) = 2 Sigma(n) + 2 sin(phi(n)) + 2 mod 12
H-(n+1) = Sigma(n+1) - 1 mod 12
H+(n+1) = Sigma(n+1) + 1 mod 12
phi(n+1) = phi(n) + 1 mod 2pi
```

Invariant: `H+ - H- = 2 mod 12`.
