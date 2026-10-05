# ONE-WAVE FRAMEWORK
## Book 1 — Micro
## Chapter 18: Excitations, Measurements and Solver Evidence

Version: 1.0  
Date: October 4, 2026  
Class: B — Applied laboratory bridge  
Status: YELLOW (physical closure open; finite candidate calculations tested)  
Framework author: Mark Wright Adlard

Dependencies: A-112 Persistent Mode, A-117 Dimensional Integrity, C-318 Four-Interaction Mass-Effect Response, C-322 Mirror-Gate Coupling, D-409 Native 3D Geometry, E-525 Measurement Operator.

## What particle language measures

A One-Wave particle description starts with a field excitation and the response obtained when it is measured. The excitation evolves in the lattice; a detector samples or couples to it; the resulting signature is classified. The model does not insert an independent bead to stand in for the field dynamics.

This gives Chapter 1's persistent-mode interpretation an operational task. Construct an excitation, evolve it, measure the response and show which properties persist across detector windows and interventions. A familiar label becomes meaningful only after that calculation.

## Two working laboratories

The [One-Wave Science Laboratory companion book](../One_Wave_Science_Laboratory/README.md) explains the executable evidence in detail.

Its [first chapter](../One_Wave_Science_Laboratory/Ch01_The_Joint_Response_Laboratory.md) follows a coupled linear fixture. Knot, electrical-shell, Mirror and weave coordinates participate in one operator. The implementation checks exact discrete energy, passive coupling, boundary inertia and carried-profile energy curvature. Its enclosing reflecting cavity makes it a response control, not proof of self-confinement.

Its [second chapter](../One_Wave_Science_Laboratory/Ch02_Localized_Excitations_and_Measurements.md) follows a nonlinear periodic-bulk hypothesis. It produces a finite-time localized branch without an enclosing wall, evolves perturbations and obtains coherent detector amplitudes and intensities from the same state. It also publishes a spreading linear control, domain and spacing changes, and a coupling-off branch that remains localized.

These are different candidate laws. A localized solution of the bulk hypothesis cannot be inserted into the linear fixture and automatically called a canonical mass derivation. Their constitutive bridge is the next scientific task.

## Measurement and recurrence

A stable density image does not imply a frozen field. A stationary excitation may evolve in phase while keeping its spatial profile. Recurrence therefore needs an explicit allowed phase, rotation or translation alignment and a measured full-state error.

A detector response depends on its window and coupling. Two detectors can sample different amounts of one excitation. Tracking the excitation peak and holding a detector fixed are also different measurements. The bulk report keeps them separate.

This clarifies the relation to Chapter 9: the current software demonstrates passive sampling of an evolving field. It has not reproduced a physical detector's backreaction, quantum counting statistics or Bell correlations. Those require additional forward models and controls.

## Relation to Chapters 14 and 15

Chapter 14 asks how the complete recurrence resists acceleration. Frequency, localization and conserved norm are useful measurements, but none alone establishes the Mass-Effect tensor. The force/acceleration experiment must independently agree with the carried-profile energy curvature under the same fixed update.

Chapter 15 asks for boundary coupling and measured outgoing response. The Mirror relation supplies coupling and phase shift without a forced geometric penetration path. A collider invariant-mass comparator is not a supplied crossing threshold or an automatic conversion of a cavity frequency into mass.

## Evidence and the next derivation

The [third laboratory chapter](../One_Wave_Science_Laboratory/Ch03_From_Candidate_to_Canonical_Derivation.md) writes the remaining work as acceptance tests. It begins from the actual second-order memory recurrence and requires a derived constitutive response, explicit native 3D geometry, interaction ablations, translation, conserved work, detector closure and numerical convergence.

The numerical evidence is owned by the [joint result packet](../../solvers/joint_response_results.json) and [bulk result packet](../../solvers/bulk_excitation_results.json). The book does not create another result database. Passing controls establish their scoped candidate behavior; the coupling-off and refinement limitations remain constraints on every next model.

## Yellow audit

Resolved at numerical candidate scope: response/accounting control; a finite localized bulk branch; measured detector amplitude, intensity and phase; explicit failures and refinement controls.

Open at physical scope: canonical origin of the nonlinear law, the four-interaction necessity test, native vortex/knot topology, norm selection, continuum convergence, free translation, force/acceleration response, independent units and a calibrated coupled detector.

A productive solver leaves both a result and a consequence. Here the result is executable excitation and response evidence. The consequence is a precise next derivation, with the previous controls kept intact.
