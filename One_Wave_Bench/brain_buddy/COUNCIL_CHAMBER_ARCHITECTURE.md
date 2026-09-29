# Council Chamber Architecture

**Branch:** owatch-logic-kernel

## Purpose

A multi-agent programming and science bench for discussion, simulation, review, and experiments.

The Council Chamber is not an authority engine. It is a controlled workspace where different paths meet only through receipts.

## Baseline Zero

Every session begins from:

- current repo state
- current project goals
- current receipts
- known limits

Baseline Zero is a starting reference, not automatic truth.

## Three-Way Discussion

Participants:

- ChatGPT
- Gemini
- DeepSeek

Flow:

```
Baseline Zero
      |
      v
Independent responses
      |
      v
Visible discussion
      |
      v
Critique and comparison
      |
      v
Receipt
```

Private model processing is not the artifact. The shared artifact is:

- claims
- references
- objections
- uncertainty
- tests
- receipts

## Floor Token

The discussion uses a speaker token.

- lightbulb = request to speak
- green light = current speaker
- current speaker acknowledges transfer
- green light passes to next speaker

This prevents uncontrolled overlap.

## Reference Cycling

The chamber periodically returns to Baseline Zero to prevent drift.

```
Discussion
   |
Reference check
   |
Drift review
   |
Rebuild working context
   |
Continue
```

## Work Tables

```
Science Table
- hypotheses
- research
- equations
- literature review

Physics Engine Table
- modular solvers
- simulations
- failure analysis
- receipts

Build Table
- prototypes
- hardware tests
- measurements
```

## Walls

```
Simulation != hardware
Proposal != canon
AI output != authority
Memory != truth
Derived != source
```

## Receipt Output

Each session records:

- participants
- references used
- agreements
- disagreements
- unknowns
- next tests
- human decision state

The Council Chamber exists to make work visible, revisable, and testable.
