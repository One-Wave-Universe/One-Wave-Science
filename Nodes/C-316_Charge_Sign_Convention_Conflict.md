---
node_id: "C-316"
canonical_name: "Charge-Sign and Direction Conflation Inside Book 1 Chapter 11"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Resolved Conflict Record / Formalization Target"
claim_gate_detail: "YELLOW — TEXTUAL CONFLICT RESOLVED; FORMAL CHARGE MAP OPEN"
metadata_standard: "I-06"
---

# Node C-316: Charge-Sign and Direction Conflation Inside Book 1 Chapter 11

Dependencies:
Upstream: Book 1 Ch4 (The Electron), Book 1 Ch11 (No Antimatter),
C-311 Electric-Magnetic Duality, B-203 Expression, B-204 Compression,
A-104 Gradient
Downstream: future repo-wide charge-sign specification and audit

Definition:
The original conflict was initially described as Ch4 versus Ch11. Direct
inspection showed a sharper result: Ch11 contradicted itself internally.

Ch4 and Ch11's prose agree:
- the electron is associated with a negative boundary-pressure sign;
- the electron shell boundary has an outward-pointing pressure gradient.

Ch11's later pair-production and annihilation math instead labeled the
electron "compression-dominant, inward." That assignment contradicted the
same chapter's earlier prose three paragraphs above it.

Resolution:
The "compression-dominant, inward" electron labels were unsupported local
errors. They were corrected in Book 1 Chapter 11. The correction does not
claim that every negative signed mode must point outward. It separates two
quantities that the old wording had conflated:

1. signed boundary-pressure orientation;
2. spatial pressure-gradient direction.

Mathematics:
Define the signed boundary-pressure value as

    P_q = s_q P_c

where

    s_q ∈ {-1,+1}

and define the spatial gradient separately:

    G_q = ∇P_q

The sign s_q and the direction of G_q are not synonyms. A negative signed
boundary mode can have an outward-pointing shell-boundary gradient. Whole-mode
Compression/Expression classification, if later retained, is a third quantity
and must also be defined separately rather than inferred from either sign or
gradient direction.

Corrected Chapter 11 statements:

Pair production:
- one mode with positive boundary-pressure sign: positron;
- one mode with negative boundary-pressure sign: electron.

Annihilation:
- e+ pressure: +P_c, positive boundary-pressure sign; outward-propagating
  release;
- e- pressure: -P_c, negative boundary-pressure sign; outward-pointing
  shell-boundary gradient;
- combined signed pressure: +P_c + (-P_c) = 0.

Resolution Record:
- RESOLVED: this was not a live Ch4-versus-Ch11 physics fork.
- RESOLVED: Ch4 and Ch11's prose already agreed.
- RESOLVED: the conflicting Ch11 pair-production and annihilation labels were
  corrected directly rather than leaving this node as a substitute.
- NOT ADOPTED: a new "compression-dominant whole electron with outward local
  gradient" mechanism was not invented merely to save the old wording.

Yellow Audit:
- The sign-versus-gradient distinction is now explicit.
- The proportionality and units connecting P_q, G_q, and measurable electric
  charge remain underived.
- C-311 and every charge-mapping node must be checked for the same conflation.
- Whole-mode dominance remains undefined and must not be inferred from sign.

Future Work:
1. Audit C-311 and all Book 1 charge passages for sign/direction conflation.
2. Define the mapping from s_q and G_q to measured charge and electric-field
   direction.
3. State boundary orientation explicitly in every future charge equation.
4. Preserve this node as the resolved correction record even after the formal
   charge map is completed.

---
