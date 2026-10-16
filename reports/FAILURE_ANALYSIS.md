# Failure and abstention analysis

## Reproduced v11 findings

- The ten author-controlled mutation families were all detected. One family did not receive an automatic repair; the included vertical-datum mismatch is explicitly left unrepaired because changing a label would not transform coordinates.
- In the frozen 180-case subset, 112 cases were REFUTED. The bounded conservative repair search returned a repair for 47 and no successful repair for 65. Those 65 are **not necessarily system failures**: some may be unrepairable with the current candidate library, require multiple edits beyond the search budget, or need evidence unavailable to the system. The current results do not independently adjudicate these explanations.
- All 47 proposed repairs passed the same verifier after editing. This is a useful consistency check but does not establish the repairs' scientific correctness.
- The per-case file records first diagnostic code, repair status/cost, and generated-reference agreement. The current summary does not by itself explain every unrepaired case; inspect `per_case.csv` and full certificates in the original v11 archive for case-level review.

## Required follow-up

Classify unrepaired cases by reason: no candidate, search budget exhaustion, conflicting findings, missing external evidence, unsafe/unsupported edit, or implementation error. Independently review every repair proposal for semantic correctness and side effects. Add multi-fault cases and measure proposal coverage, correct proposal rate, false repair rate, refusal, cost, and re-verification separately.
