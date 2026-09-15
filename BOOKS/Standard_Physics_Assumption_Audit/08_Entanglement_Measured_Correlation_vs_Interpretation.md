# CHAPTER 8 — ENTANGLEMENT: MEASURED CORRELATION VS INTERPRETATION

Status: YELLOW — measured Bell correlations are fixed targets; ontology remains under audit

CORE-RULES-PRE:
- Preserve the measured correlations and Bell/CHSH mathematics.
- Separate what the experiment records from verbal stories such as "instant communication" or "spooky action."
- Do not claim a local shared-phase model works if it only reaches the Bell bound.
- Relevant rules: 1, 2, 3, 5, 7, 10, 12, 15, 16, 17, 18.

## 1. What is actually measured

Entanglement experiments record paired detector outcomes under independently chosen measurement settings.

For binary outcomes

$$
A,B\in\{-1,+1\},
$$

and settings $a,b$, the experimental correlation is estimated from repeated trials as

$$
E(a,b)=\langle AB\rangle
=\sum_{A,B} AB\,P(A,B|a,b).
$$

The data are coincidence counts and their setting-dependent correlations.

That is the measurement layer.

## 2. Bell/CHSH constraint

For a local factorized hidden-variable model with hidden state $\lambda$,

$$
P(A,B|a,b,\lambda)
=
P(A|a,\lambda)P(B|b,\lambda),
$$

and with the usual measurement-independence assumptions, define

$$
S
=
E(a,b)+E(a,b')+E(a',b)-E(a',b').
$$

Then

$$
|S|\le2.
$$

Quantum mechanics predicts settings for which

$$
|S|=2\sqrt2.
$$

Bell-test experiments have observed violations of Bell inequalities consistent with quantum predictions.

This experimental constraint does not disappear because a competing ontology uses waves instead of particles.

## 3. What interpretation gets added

The measured fact is stronger-than-Bell-local correlation.

Interpretive language may then say:

- the particles are nonlocally connected;
- measurement on one "instantly affects" the other;
- the pair is one nonseparable quantum state;
- outcomes were not locally predetermined;
- the state is updated globally after measurement.

These statements are not all equivalent.

The book must ask exactly which claim follows from the experiment and which depends on the chosen interpretation or assumptions entering Bell's theorem.

## 4. What Bell does rule out

A simple preloaded local instruction model cannot reproduce all observed correlations while keeping the standard Bell assumptions.

For One-Wave this matters directly.

Suppose a shared source phase is

$$
\lambda\in[0,2\pi),
$$

and local analyzer outputs are

$$
A(a,\lambda)=\operatorname{sgn}[\cos 2(\lambda-a)],
$$

$$
B(b,\lambda)=-\operatorname{sgn}[\cos 2(\lambda-b)].
$$

Then for angular separation $\Delta=|a-b|$ over the relevant range,

$$
E_{\mathrm{sign}}(\Delta)
=-1+\frac{4\Delta}{\pi}.
$$

At the standard CHSH settings this reaches

$$
|S|=2,
$$

not

$$
2\sqrt2.
$$

That failed result is part of the protected math backbone and must remain visible.

## 5. The quantum target

For the polarization singlet-like target used in the recovered One-Wave audit, an idealized binary joint distribution can be written

$$
P(r_A,r_B|a,b)
=\frac14\left[1-r_A r_B\cos2(a-b)\right],
$$

where

$$
r_A,r_B\in\{-1,+1\}.
$$

This gives

$$
E(a,b)
=\sum_{r_A,r_B}r_A r_B P(r_A,r_B|a,b)
=-\cos2(a-b).
$$

The local marginals remain

$$
P(r_A=\pm1|a,b)=\frac12,
$$

$$
P(r_B=\pm1|a,b)=\frac12,
$$

so the correlation does not provide controllable faster-than-light signaling.

## 6. The interpretation audit

The experiment establishes the correlation structure and violation of Bell inequalities.

It does not, by itself, force one everyday-language picture such as a signal physically shooting from detector A to detector B.

But neither does it permit a model to simply say "the source wave already knew both answers" if that model remains Bell-local and measurement-independent.

Any alternative must state which mathematical assumption changes and then survive experiment.

## 7. One-Wave challenge

The useful One-Wave starting claim is not

> entanglement is fake.

The useful claim to test is

> the experiment may be sampling one globally related wave/state rather than two fundamentally independent particle objects.

That idea still must derive the measured joint distribution.

A candidate global-boundary formulation could schematically be

$$
\mathcal L[W]=0
$$

subject to source boundary data and detector boundary settings $a,b$.

Detector outcomes would then be functionals

$$
r_A=F_A[W;a],
\qquad
r_B=F_B[W;b].
$$

If the global solution $W$ depends jointly on the full boundary-value problem, Bell factorization may fail. But that is only a mathematical direction until the dynamics, causality structure, and settings dependence are explicitly derived.

## 8. Kill tests

A One-Wave entanglement account must:

1. reproduce measured $E(a,b)$;
2. violate CHSH by the observed amount where appropriate;
3. preserve no-signaling marginals;
4. handle delayed/random setting choices;
5. avoid hidden per-experiment tuning;
6. identify exactly which Bell assumption is not satisfied if the model is not Bell-local;
7. produce new distinguishing predictions if it claims more than reinterpretation.

## 9. Audit result

MEASURED:
- setting-dependent paired correlations;
- Bell-inequality violations.

NOT ESTABLISHED BY THE DATA ALONE:
- a literal faster-than-light message travels between detectors;
- consciousness creates the correlation;
- one particular ontology is uniquely forced.

FAILED ONE-WAVE PATH PRESERVED:
- simple independent local sign threshold with shared phase gives $S=2$.

OPEN:
- derive the full One-Wave joint probability law from field and detector dynamics rather than inserting the quantum answer.

CORE-RULES-POST:
- Bell data preserved as non-negotiable target.
- Interpretation separated from detector counts and correlations.
- Failed local shared-phase calculation retained.
- One-Wave claim remains YELLOW pending explicit derivation.

Reference anchor: Nobel Prize in Physics 2022 materials on experiments with entangled photons and violation of Bell inequalities.
